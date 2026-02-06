from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..services.database import db
from ..models.interviews import InterviewResponse, InterviewCreate, InterviewUpdate
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/interviews",
    tags=["interviews"]
)

@router.get("/", response_model=List[InterviewResponse])
async def get_my_interviews(current_user: dict = Depends(get_current_user)):
    """Get all interviews for the current candidate"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can view their interviews")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        return []
        
    return db.get_interviews_for_candidate(candidate["id"])

# For Recruiter/System to schedule
@router.post("/", response_model=InterviewResponse)
async def schedule_interview(interview: InterviewCreate, current_user: dict = Depends(get_current_user)):
    """Schedule an interview (Recruiter/Admin only)"""
    # For simplicity, allowing recruiters to schedule
    if current_user["role"] not in ["recruiter", "admin"]:
        # Allow self-scheduling for demo if needed? No, standard is recruiter.
        # But wait, how do we demo without a recruiter login flow readily available? 
        # The prompt implies we have recruiter login.
        raise HTTPException(status_code=403, detail="Not authorized to schedule interviews")

    interview_id = db.create_interview(
        interview.application_id, 
        interview.scheduled_time.isoformat(), # Store as string
        interview.interviewer
    )
    
    # Update application status
    # We need a db method for this, update status to 'interviewing'
    # db.update_application_status(interview.application_id, "interviewing") # TODO add this if strictly needed

    # Fetch created interview (simplified return)
    return {
        "id": interview_id,
        "application_id": interview.application_id,
        "interviewer": interview.interviewer,
        "scheduled_time": interview.scheduled_time,
        "result": "pending",
        "feedback": None,
        "created_at": "Just now"
    }

@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(interview_id: int, update: InterviewUpdate, current_user: dict = Depends(get_current_user)):
    """Update interview status/feedback (Recruiter only)"""
    if current_user["role"] not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    success = db.update_interview_status(
        interview_id, 
        result=update.result, 
        feedback=update.feedback
    )
    
    if not success:
         raise HTTPException(status_code=404, detail="Interview not found")
         
    return {
        "id": interview_id,
        "application_id": 0, # Placeholder
        "interviewer": "Updated",
        "scheduled_time": "2023-01-01T00:00:00", # Placeholder
        "result": update.result,
        "feedback": update.feedback,
        "created_at": "Just now"
    }
