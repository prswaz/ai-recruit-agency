from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..services.database import db
from ..models.candidates import CandidateResponse, ApplicationCreate, ApplicationResponse, CandidateCreate
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"]
)

@router.get("/me", response_model=CandidateResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's candidate profile"""
    try:
        if current_user["role"] != "candidate":
            raise HTTPException(status_code=403, detail="Not a candidate account")
            
        candidate = db.get_candidate_by_user_id(current_user["id"])
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")
            
        # Enrich with user info
        data = dict(candidate)
        data["email"] = current_user["email"]
        
        # Parse skills if it's a string
        if isinstance(data.get("skills"), str):
            import json
            try:
                data["skills"] = json.loads(data["skills"])
            except json.JSONDecodeError:
                data["skills"] = []
                
        # Parse analysis_report if it exists
        if data.get("analysis_report") and isinstance(data.get("analysis_report"), str):
             import json
             try:
                 data["analysis_report"] = json.loads(data["analysis_report"])
             except json.JSONDecodeError:
                 data["analysis_report"] = None

        return data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/me", response_model=CandidateResponse)
async def update_my_profile(profile_update: CandidateCreate, current_user: dict = Depends(get_current_user)):
    """Update current user's profile"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Not a candidate account")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    
    success = db.update_candidate(
        candidate["id"],
        full_name=profile_update.full_name,
        phone=profile_update.phone,
        location=profile_update.location,
        experience_level=profile_update.experience_level,
        resume_url=profile_update.resume_url
    )
    
    if not success:
         raise HTTPException(status_code=400, detail="Update failed")
         
    # Return updated profile
    updated = db.get_candidate_by_user_id(current_user["id"])
    data = dict(updated)
    data["email"] = current_user["email"]
    
    # Parse JSON fields
    if isinstance(data.get("skills"), str):
        import json
        try:
             data["skills"] = json.loads(data["skills"])
        except json.JSONDecodeError:
             data["skills"] = []
             
    if data.get("analysis_report") and isinstance(data.get("analysis_report"), str):
         import json
         try:
             data["analysis_report"] = json.loads(data["analysis_report"])
         except json.JSONDecodeError:
             data["analysis_report"] = None
             
    return data

@router.post("/applications", response_model=ApplicationResponse)
async def apply_for_job(application: ApplicationCreate, current_user: dict = Depends(get_current_user)):
    """Apply for a job"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        raise HTTPException(status_code=400, detail="Profile incomplete")
        
    # Check if job exists
    job = db.get_job_by_id(application.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    app_id = db.create_application(candidate["id"], application.job_id)
    if not app_id:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    return {
        "id": app_id,
        "job": job,
        "status": "applied",
        "applied_at": "Just now" # simplified
    }

@router.get("/applications", response_model=List[ApplicationResponse])
async def get_my_applications(current_user: dict = Depends(get_current_user)):
    """Get all applications for current candidate"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Not a candidate")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        return []
        
    return db.get_applications_for_candidate(candidate["id"])
