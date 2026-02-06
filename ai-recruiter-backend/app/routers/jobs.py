from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..services.database import db
from ..models.jobs import JobCreate, JobResponse
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/", response_model=List[JobResponse])
async def get_jobs():
    """List all available jobs"""
    return db.get_all_jobs()

@router.get("/{job_id}", response_model=JobResponse)
async def get_job_detail(job_id: int):
    """Get specific job details"""
    job = db.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    """Create a new job posting (Recruiters only)"""
    if current_user["role"] != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can post jobs")
    
    # Get company ID for this user
    company = db.get_company_by_user_id(current_user["id"])
    if not company:
        raise HTTPException(status_code=400, detail="Recruiter profile incomplete")
        
    job_data = job.model_dump()
    job_data["company_id"] = company["id"]
    
    created_job = db.get_job_by_id(job_id)
    return created_job

@router.get("/{job_id}/applications", response_model=List) # Using List[dict] simplified or create a model
async def get_job_applications(job_id: int, current_user: dict = Depends(get_current_user)):
    """Get all applications for a specific job (Recruiter only)"""
    if current_user["role"] != "recruiter":
         raise HTTPException(status_code=403, detail="Only recruiters can view applications")
    
    # Verify ownership
    job = db.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    company = db.get_company_by_user_id(current_user["id"])
    if not company or job["company_id"] != company["id"]:
         raise HTTPException(status_code=403, detail="Not your job posting")
         
    return db.get_applications_for_job(job_id)
