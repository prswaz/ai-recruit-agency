from typing import Dict, Any
import time
from asgiref.sync import sync_to_async

from agents.orchestrator import OrchestratorAgent 
from .models import AIAgent, AILog

class AgentManager:
    """Central management for interacting with AI agents.
    This class is not a Django model and only implements the application logic.
    """

    def __init__(self):
        self.orchestrator = OrchestratorAgent()
      
        # record from async code.
        self.agent_record = None

    async def ensure_agent(self):
        """Asynchronously ensure the AIAgent DB record exists and cache it.

        This uses sync_to_async to run the synchronous ORM call in a thread so
        it is safe to call from async contexts.
        """
        if self.agent_record is not None:
            return self.agent_record

        self.agent_record, _ = await sync_to_async(
            AIAgent.objects.get_or_create, thread_sensitive=True
        )(
            name="Orchestrator",
            defaults={
                "version": "1.0",
                "function": "orchestrator",
                "description": "Main workflow coordinator"
            }
        )
        return self.agent_record

    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        start_time = time.time()

        try:
            
            result = await self.orchestrator.process_application(
                {"resume_text": resume_text}
            )

          
            if self.agent_record is None:
                # best-effort: if ensure_agent wasn't called earlier, create now
                await self.ensure_agent()

            await sync_to_async(AILog.objects.create, thread_sensitive=True)(
                agent=self.agent_record,
                action_type="ResumeAnalysis",
                input_data={"resume_text_length": len(resume_text)},
                output_data=result,
                execution_time_ms=int((time.time() - start_time) * 1000)
            )

            return result

        except Exception as e:
         
            if self.agent_record is None:
                await self.ensure_agent()

            await sync_to_async(AILog.objects.create, thread_sensitive=True)(
                agent=self.agent_record,
                action_type="ResumeAnalysis_Failed",
                input_data={
                    "resume_text_length": len(resume_text),
                    "error": str(e)
                },
                execution_time_ms=int((time.time() - start_time) * 1000)
            )
            raise RuntimeError(f"AgentManager: {e}")