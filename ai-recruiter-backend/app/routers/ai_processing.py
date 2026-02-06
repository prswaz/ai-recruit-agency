from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Dict, Any
import sys
import os
import json

# Add project root to sys path to allow importing 'agents'
# Current: .../ai-recruiter-backend/app/routers/applications_processing.py
# Root: .../ai-recruiter-agency/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

try:
    from agents.orchestrator import OrchestratorAgent
except ImportError:
    print("Warning: Could not import OrchestratorAgent. Agents might not be available.")
    OrchestratorAgent = None

from ..utils_pdf import extract_text_from_pdf
from ..routers.auth import get_current_user
from ..services.database import db

router = APIRouter(
    prefix="/ai-processing",
    tags=["ai-processing"]
)


@router.post("/process-resume")
async def process_resume_and_apply(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a resume (PDF), extract text, and run the AI Orchestrator
    to analyze, match, screen, and recommend.
    """

    if not OrchestratorAgent:
        raise HTTPException(status_code=500, detail="AI Agents not available")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    text = await extract_text_from_pdf(content)

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    orchestrator = OrchestratorAgent()

    resume_data = {
        "text": text,
        "candidate_id": current_user["id"],
        "candidate_email": current_user["email"],
        "filename": file.filename
    }

    try:
        # ================= AI ORCHESTRATION =================
        result = await orchestrator.process_application(resume_data)
        print(f"DEBUG: Agent raw result: {result}")

        # ================= CONSOLIDATED REPORT =================
        raw_rec = result.get("final_recommendation") or {}

        consolidated_report = {
            "analysis_results": result.get("analysis_results", {}),
            "job_matches": result.get("job_matches", {}),
            "screening_results": result.get("screening_results", {}),
            "summary": "Analysis completed. Review your strengths and matches below."
        }

        # ---------- Parse final recommendation summary ----------
        try:
            inner_rec_str = raw_rec.get("final_recommendation")
            if isinstance(inner_rec_str, str):
                inner_rec_json = json.loads(inner_rec_str)
                recs = inner_rec_json.get("final_recommendations", [])
                if recs and isinstance(recs, list):
                    consolidated_report["summary"] = recs[0].get(
                        "description", consolidated_report["summary"]
                    )
        except Exception as e:
            print(f"[WARN] Could not parse final recommendation JSON: {e}")

        # ================= SKILLS EXTRACTION =================
        extracted = result.get("extracted_data") or {}
        extracted_data = extracted if isinstance(extracted, dict) else {}

        skills = extracted_data.get("skills", [])

        if not skills:
            try:
                struct_data_str = extracted_data.get("structured_data")
                if isinstance(struct_data_str, str):
                    struct_json = json.loads(struct_data_str)
                    skills = (
                        struct_json.get("Technical Skills")
                        or struct_json.get("skills")
                        or struct_json.get("Skills")
                        or []
                    )
                    if not isinstance(skills, list):
                        skills = []
            except Exception as e:
                print(f"[WARN] Could not extract skills from structured data: {e}")

        # ================= MAP STRENGTHS & TECH SKILLS =================
        try:
            ar = consolidated_report.get("analysis_results", {})
            sa = ar.get("skills_analysis", {})

            if "strengths" not in ar:
                ar["strengths"] = sa.get("key_achievements", [])

            if not sa.get("technical_skills") and skills:
                sa["technical_skills"] = skills

        except Exception as e:
            print(f"[WARN] Strengths/skills mapping failed: {e}")

        # ================= DATABASE UPDATE =================
        candidate = db.get_candidate_by_user_id(current_user["id"])

        if candidate:
            candidate_dict = dict(candidate)

            try:
                db.update_candidate_analysis(
                    candidate_dict["id"],
                    consolidated_report,
                    skills
                )
            except Exception as e:
                print(f"[WARN] Failed to update candidate analysis: {e}")

            # ================= JOB MATCHING =================
            exp_level = (
                consolidated_report
                .get("analysis_results", {})
                .get("skills_analysis", {})
                .get("experience_level")
                or candidate_dict.get("experience_level")
            )

            print(f"Looking for matches with skills: {skills}")
            matches = db.find_matching_jobs(skills, exp_level)
            print(f"Found {len(matches)} matches")

            for job in matches:
                try:
                    job_reqs = set(job.get("requirements", []))
                    user_skills = set(skills)

                    if not job_reqs:
                        score = 0.5
                    else:
                        overlap = len(job_reqs.intersection(user_skills))
                        score = overlap / len(job_reqs)

                    if score > 0:
                        db.save_recommendation(
                            job["id"],
                            candidate_dict["id"],
                            score,
                            f"Matched based on skills: {', '.join(user_skills & job_reqs)}"
                        )

                except Exception as e:
                    print(f"[WARN] Job matching failed for job {job.get('id')}: {e}")

        return consolidated_report

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"AI processing failed: {str(e)}"
        )
