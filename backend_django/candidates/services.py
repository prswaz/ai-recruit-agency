import os
import json
import asyncio
from typing import Dict, Any, List
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from .models import Candidate, ResumeAnalysis, Recommendation
from core.models import Skill, Job
from utils_pdf import extract_text_from_pdf
from ai_engine.agent_manager import AgentManager

class ResumeAnalysisService:
    @staticmethod
    async def process_resume_upload(user: Any, resume_file: UploadedFile) -> Dict[str, Any]:
        # 1. Save file locally
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, resume_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in resume_file.chunks():
                destination.write(chunk)
                
        # 2. Extract Text
        with open(file_path, 'rb') as f:
            file_content = f.read()
        resume_text = await extract_text_from_pdf(file_content)

        # 3. AI Analysis via AgentManager
        agent_manager = AgentManager()
        # ensure DB-backed agent record exists (async)
        await agent_manager.ensure_agent()
        result = await agent_manager.analyze_resume(resume_text)

        analysis_data = result.get('analysis_results', {})
        detected_skills = ResumeAnalysisService._extract_skills(result, analysis_data)

        final_report = {
            "summary": result.get('final_recommendation', {}).get('summary', 'Analysis complete.'),
            "analysis_results": {
                "strengths": analysis_data.get('strengths', []),
                "gaps": analysis_data.get('gaps', []) or analysis_data.get('weaknesses', [])
            },
            "skills": detected_skills,
            "job_matches": result.get('job_matches', {})
        }

        # 4. Persistence (perform ORM ops in thread to be safe in async context)
        candidate, _ = await sync_to_async(Candidate.objects.get_or_create, thread_sensitive=True)(
            user=user,
            defaults={'email': user.email, 'full_name': f"{user.first_name} {user.last_name}"}
        )

        candidate.resume_url = f"/media/uploads/{resume_file.name}"
        candidate.analysis_report = final_report

        # Skill Normalization
        skill_objs = []
        for s_name in detected_skills:
            skill_obj, _ = await sync_to_async(Skill.objects.get_or_create, thread_sensitive=True)(
                name=s_name.strip().title()
            )
            skill_objs.append(skill_obj)

        # set many-to-many via thread
        await sync_to_async(candidate.skills.set, thread_sensitive=True)(skill_objs)
        await sync_to_async(candidate.save, thread_sensitive=True)()

        # History Table
        await sync_to_async(ResumeAnalysis.objects.create, thread_sensitive=True)(
            candidate=candidate,
            resume_url=candidate.resume_url,
            extracted_skills=detected_skills,
            experience_level=result.get('extracted_data', {}).get('experience_level', 'Mid-level'),
            strengths=analysis_data.get('strengths', []),
            gaps=analysis_data.get('gaps', []) or analysis_data.get('weaknesses', []),
            summary=final_report['summary'],
            job_matches=final_report['job_matches']
        )

        # 5. Recommendation Logic
        # run update_or_create in thread for each job
        await sync_to_async(ResumeAnalysisService._generate_recommendations, thread_sensitive=True)(candidate, detected_skills)

        return {
            "report": final_report,
            "candidate": candidate,
            "skills_count": len(detected_skills)
        }

    @staticmethod
    def _extract_skills(result: Dict[str, Any], analysis_data: Dict[str, Any]) -> List[str]:
        detected_skills = []
        if 'extracted_data' in result:
            skills_from_extracted = result['extracted_data'].get('skills', [])
            if isinstance(skills_from_extracted, str):
                try:
                    detected_skills = json.loads(skills_from_extracted)
                except:
                    detected_skills = [s.strip() for s in skills_from_extracted.split(',') if s.strip()]
            elif isinstance(skills_from_extracted, list):
                detected_skills = skills_from_extracted
        
        if not detected_skills and 'skills_analysis' in analysis_data:
            skills_analysis = analysis_data.get('skills_analysis', {})
            if isinstance(skills_analysis, dict):
                detected_skills = skills_analysis.get('technical_skills', [])
        
        return [s for s in detected_skills if isinstance(s, str)]

    @staticmethod
    def _generate_recommendations(candidate: Candidate, detected_skills: List[str]):
        jobs = Job.objects.all()[:20]
        user_skills = set(detected_skills)
        
        for job in jobs:
            job_reqs = job.requirements if isinstance(job.requirements, list) else []
            job_reqs_set = set(job_reqs)
            
            if not job_reqs_set:
                score = 0
            else:
                score = len(job_reqs_set.intersection(user_skills)) / len(job_reqs_set)
            
            if score > 0.2:
                Recommendation.objects.update_or_create(
                    candidate=candidate,
                    job=job,
                    defaults={
                        'match_score': score, 
                        'explanation': f"Match based on skills: {', '.join(user_skills.intersection(job_reqs_set)) or 'general fit'}"
                    }
                )
