from typing import Dict, Any, List
from .base_agent import BaseAgent
from core.models import Job
import json
from django.db.models import Q

class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Matcher",
            instructions="""Match candidate profiles with job positions.
            Consider: skills match, experience level, location preferences.
            Provide detailed reasoning and compatibility scores.
            Return matches in JSON format with title, match_score, and location fields.""",
        )

    async def run(self, messages: list) -> Dict[str, Any]:
        """Match candidate with available positions"""
        print("🎯 Matcher: Finding suitable job matches")

        try:
            # Convert single quotes to double quotes to make it valid JSON
            content = messages[-1].get("content", "{}").replace("'", '"')
            analysis_results = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing analysis results: {e}")
            return {
                "matched_jobs": [],
                "match_timestamp": "2024-03-14",
                "number_of_matches": 0,
            }

        # Extract skills and experience level from analysis
        skills_analysis = analysis_results.get("skills_analysis", {})
        if not skills_analysis:
            print("No skills analysis provided in the input.")
            return {
                "matched_jobs": [],
                "match_timestamp": "2024-03-14",
                "number_of_matches": 0,
            }

        # Extract technical skills and experience level directly
        skills = skills_analysis.get("technical_skills", [])
        experience_level = skills_analysis.get("experience_level", "Mid-level")

        if not isinstance(skills, list) or not skills:
            print("No valid skills found, defaulting to an empty list.")
            skills = []

        if experience_level not in ["Junior", "Mid-level", "Senior", "Lead", "Executive"]:
            print("Invalid or missing experience level, defaulting to Mid-level.")
            if not experience_level:
                experience_level = "Mid-level"

        print(f" ==>>> Skills: {skills}, Experience Level: {experience_level}")
        
        # Search jobs database - wrap in sync_to_async since we're in async context
        from asgiref.sync import sync_to_async
        matching_jobs = await sync_to_async(self.search_jobs)(skills, experience_level)

        # Calculate match scores
        scored_jobs = []
        for job in matching_jobs:
            # Calculate match score based on requirements overlap
            # Requirements are stored as JSON field or list
            
            job_requirements = job.requirements # This assumes JSON field or list
            if isinstance(job_requirements, str):
                try:
                    job_requirements = json.loads(job_requirements)
                except:
                    job_requirements = [job_requirements]
            
            # Simple intersection
            required_skills = set([r.lower() for r in job_requirements])
            candidate_skills = set([s.lower() for s in skills])
            
            overlap = 0
            for skill in candidate_skills:
                # Fuzzy match simple
                if any(skill in req or req in skill for req in required_skills):
                    overlap += 1
            
            total_required = len(required_skills)
            match_score = (
                int((overlap / total_required) * 100) if total_required > 0 else 0
            )

            # Lower threshold for matching to 20%
            if match_score >= 20:  # Include jobs with >20% match
                scored_jobs.append(
                    {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company.name if job.company else "Unknown",
                        "match_score": f"{match_score}%",
                        "location": job.location,
                        "salary_range": job.salary_range,
                        "requirements": job_requirements,
                    }
                )

        print(f" ==>>> Scored Jobs: {scored_jobs}")
        # Sort by match score
        scored_jobs.sort(key=lambda x: int(x["match_score"].rstrip("%")), reverse=True)

        return {
            "matched_jobs": scored_jobs[:3],  # Top 3 matches
            "match_timestamp": "2024-03-14",
            "number_of_matches": len(scored_jobs),
        }

    def search_jobs(self, skills: List[str], experience_level: str):
        """Search jobs based on skills and experience level using Django ORM"""
        # normalize experience level for better matching? or just loose filter
        
        # Base query with select_related to pre-fetch company data
        jobs = Job.objects.select_related('company').all()
        
        # Filter by skills (OR logic)
        if skills:
            q_obj = Q()
            for skill in skills:
                q_obj |= Q(requirements__icontains=skill) | Q(description__icontains=skill)
            jobs = jobs.filter(q_obj).distinct()
        
        return list(jobs)

