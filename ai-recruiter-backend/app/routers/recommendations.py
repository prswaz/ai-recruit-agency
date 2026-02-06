from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import json
from ..services.database import db
from ..routers.auth import get_current_user
from ..models.jobs import JobResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

class RecommendationResponse(BaseModel):
    id: int
    match_score: float
    explanation: str
    job: JobResponse
    # created_at: str

@router.post("/generate", response_model=List[RecommendationResponse])
async def generate_recommendations(current_user: dict = Depends(get_current_user)):
    """Generate new recommendations based on candidate profile"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can get recommendations")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        raise HTTPException(status_code=400, detail="Profile incomplete")
    
    # Extract skills
    skills_json = candidate["skills"]
    skills = []
    if skills_json:
        try:
             skills = json.loads(skills_json)
        except:
             skills = [] # Handle string or bad json
    
    if not skills:
        return [] # No skills, no matches
        
    # Find matching jobs using DB logic
    potential_jobs = db.find_matching_jobs(skills, candidate["experience_level"])
    
    recommendations = []
    
    for job in potential_jobs:
        # Calculate Match Score (Simple overlap logic equivalent to MatcherAgent)
        required_skills = set(job["requirements"])
        candidate_skills_set = set(skills)
        
        if not required_skills:
            match_score = 0.5 # Default if no reqs
        else:
            overlap = len(required_skills.intersection(candidate_skills_set))
            match_score = round(overlap / len(required_skills), 2)
            
        # Filter low matches (e.g. < 30%)
        if match_score >= 0.3:
            # Generate explanation (Static for now, could be LLM)
            explanation = f"Matches {len(required_skills.intersection(candidate_skills_set))} of {len(required_skills)} required skills."
            
            # Save to DB
            rec_id = db.save_recommendation(job["id"], candidate["id"], match_score, explanation)
            
            if rec_id:
                # Construct response
                job_resp = JobResponse(**job, company_name="Company") # DB fetch might miss company name in dict if not joined carefully
                # Ideally db.find_matching_jobs should join companies. Let's fix that assumption if needed.
                # For now, simplistic construction.
                pass 

    # Return all for this candidate
    return await get_recommendations(current_user)

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations(current_user: dict = Depends(get_current_user)):
    """Get existing recommendations"""
    if current_user["role"] != "candidate":
        raise HTTPException(status_code=403, detail="Not a candidate")
        
    candidate = db.get_candidate_by_user_id(current_user["id"])
    if not candidate:
        return []
        
    recs = db.get_recommendations_for_candidate(candidate["id"])
    
    # Format for response
    results = []
    for r in recs:
        # Reconstruct Job object
        # Note: 'r' has joined fields from get_recommendations_for_candidate
        job_data = {
            "id": r["job_id"],
            "title": r["title"],
            "description": "...", # Description might be large, maybe omitted in list view or joined
            "company_id": r["company_id"], 
            "company_name": r["company_name"],
            "location": r["location"],
            "type": r["type"],
            "description": "See details", # simplified
            "requirements": [],
            "benefits": []
        }
        
        results.append({
            "id": r["id"],
            "match_score": r["match_score"],
            "explanation": r["explanation"],
            "job": job_data
        })
        
    return results
