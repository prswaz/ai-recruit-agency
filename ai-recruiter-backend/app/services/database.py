import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class JobDatabase:
    def __init__(self):
        # We'll assume the DB is in the parent 'db' folder relative to the project root for now,
        # or we could move it to the backend folder. Let's keep it in 'db' at the root.
        # Current file path: .../ai-recruiter-agency/ai-recruiter-backend/app/services/database.py
        # Project Root: .../ai-recruiter-agency
        
        self.root_dir = Path(__file__).parent.parent.parent.parent
        self.db_path = self.root_dir / "db" / "jobs.sqlite"
        self.schema_path = self.root_dir / "db" / "schema.sql"
        
        print(f"DEBUG: Root Dir: {self.root_dir}")
        print(f"DEBUG: DB Path: {self.db_path}")
        print(f"DEBUG: Schema Path: {self.schema_path}")

        # Ensure db directory exists
        self.db_path.parent.mkdir(exist_ok=True)
        
    def init_db(self):
        """Initialize the database with the schema"""
        if not self.schema_path.exists():
             # Fallback if running from a different context or if schema moved? 
             # For now, let's just log or error.
             print(f"Warning: Schema file not found at {self.schema_path}")
             return

        with open(self.schema_path) as f:
            schema = f.read()

        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # --- User / Auth ---
    def create_user(self, email: str, password_hash: str, role: str) -> int:
        query = "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, password_hash, role))
            return cursor.lastrowid

    def get_user_by_email(self, email: str):
        query = "SELECT * FROM users WHERE email = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            return cursor.fetchone()

    def get_candidate_by_user_id(self, user_id: int):
        query = "SELECT * FROM candidates WHERE user_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
            
    def get_company_by_user_id(self, user_id: int):
        query = "SELECT * FROM companies WHERE user_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchone()


    # --- Companies ---
    def create_company(self, user_id: int, name: str, **kwargs) -> int:
        query = """
        INSERT INTO companies (user_id, name, industry, location, website, contact_email) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                user_id,
                name,
                kwargs.get("industry"),
                kwargs.get("location"),
                kwargs.get("website"),
                kwargs.get("contact_email")
            ))
            return cursor.lastrowid

    # --- Candidates ---
    def create_candidate(self, user_id: int, full_name: str, email: str, **kwargs) -> int:
        query = """
        INSERT INTO candidates (user_id, full_name, email, phone, location, experience_level, resume_url, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                user_id,
                full_name,
                email,
                kwargs.get("phone"),
                kwargs.get("location"),
                kwargs.get("experience_level"),
                kwargs.get("resume_url"),
                json.dumps(kwargs.get("skills", [])),
            ))
            return cursor.lastrowid

    def update_candidate(self, candidate_id: int, **kwargs):
        allowed_keys = ["full_name", "phone", "location", "experience_level", "resume_url"]
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_keys and value is not None:
                updates.append(f"{key} = ?")
                params.append(value)
                
        if not updates:
            return False
            
        params.append(candidate_id)
        query = f"UPDATE candidates SET {', '.join(updates)} WHERE id = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def update_candidate_analysis(self, candidate_id: int, analysis_report: dict, skills: list):
        query = "UPDATE candidates SET analysis_report = ?, skills = ? WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (json.dumps(analysis_report), json.dumps(skills), candidate_id))
            conn.commit()
    def add_job(self, job_data: dict) -> int:
        query = """
        INSERT INTO jobs (title, company_id, location, type, experience_level, salary_range, description, requirements, benefits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                job_data["title"],
                job_data["company_id"],
                job_data["location"],
                job_data["type"],
                job_data["experience_level"],
                job_data.get("salary_range"),
                job_data["description"],
                json.dumps(job_data["requirements"]),
                json.dumps(job_data.get("benefits", [])),
            ))
            return cursor.lastrowid

    def get_job_by_id(self, job_id: int):
        query = """
        SELECT jobs.*, companies.name AS company_name 
        FROM jobs
        JOIN companies ON jobs.company_id = companies.id
        WHERE jobs.id = ?
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (job_id,))
            row = cursor.fetchone()
            if row:
                d = dict(row)
                d["requirements"] = json.loads(d["requirements"]) if d["requirements"] else []
                d["benefits"] = json.loads(d["benefits"]) if d["benefits"] else []
                return d
            return None

    def get_all_jobs(self):
        query = """
        SELECT jobs.*, companies.name AS company_name 
        FROM jobs
        JOIN companies ON jobs.company_id = companies.id
        ORDER BY jobs.created_at DESC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d["requirements"] = json.loads(d["requirements"]) if d["requirements"] else []
                d["benefits"] = json.loads(d["benefits"]) if d["benefits"] else []
                results.append(d)
            return results

    # --- Applications ---
    def create_application(self, candidate_id: int, job_id: int, source: str = "web"):
        # Check if already applied
        check_query = "SELECT id FROM applications WHERE candidate_id = ? AND job_id = ?"
        
        insert_query = """
        INSERT INTO applications (candidate_id, job_id, status, source)
        VALUES (?, ?, 'applied', ?)
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(check_query, (candidate_id, job_id))
            if cursor.fetchone():
                return None # Already applied
                
            cursor.execute(insert_query, (candidate_id, job_id, source))
            return cursor.lastrowid

    def get_applications_for_candidate(self, candidate_id: int):
        query = """
        SELECT a.id, a.status, a.applied_at, 
               j.id as job_id, j.title, j.location, j.type, j.description, j.requirements, j.benefits,
               c.name as company_name, c.id as company_id
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE a.candidate_id = ?
        ORDER BY a.applied_at DESC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                r = dict(row)
                # Construct nested job object
                job_obj = {
                    "id": r["job_id"],
                    "title": r["title"],
                    "location": r["location"],
                    "type": r["type"],
                    "description": r["description"],
                    "company_id": r["company_id"],
                    "company_name": r["company_name"],
                    "requirements": json.loads(r["requirements"]) if r["requirements"] else [],
                    "benefits": json.loads(r["benefits"]) if r["benefits"] else []
                }
                results.append({
                    "id": r["id"],
                    "status": r["status"],
                    "applied_at": str(r["applied_at"]),
                })
            return results

    def get_applications_for_job(self, job_id: int):
        query = """
        SELECT a.id, a.status, a.applied_at, 
               c.full_name, c.email, c.resume_url, c.experience_level, c.analysis_report
        FROM applications a
        JOIN candidates c ON a.candidate_id = c.id
        WHERE a.job_id = ?
        ORDER BY a.applied_at DESC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (job_id,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                r = dict(row)
                 # Parse analysis report if present
                if r.get("analysis_report"):
                    try:
                        r["analysis_report"] = json.loads(r["analysis_report"])
                    except:
                        r["analysis_report"] = None
                results.append(r)
            return results

    # --- Interviews ---
    def create_interview(self, application_id: int, scheduled_time: str, interviewer: str = "AI Recruiter"):
        query = """
        INSERT INTO interviews (application_id, scheduled_time, interviewer, result)
        VALUES (?, ?, ?, 'pending')
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (application_id, scheduled_time, interviewer))
            return cursor.lastrowid

    def get_interviews_for_candidate(self, candidate_id: int):
        query = """
        SELECT i.*, j.title as job_title, c.name as company_name
        FROM interviews i
        JOIN applications a ON i.application_id = a.id
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE a.candidate_id = ?
        ORDER BY i.scheduled_time DESC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id,))
            return [dict(row) for row in cursor.fetchall()]

    def update_interview_status(self, interview_id: int, result: str = None, feedback: str = None):
        updates = []
        params = []
        if result:
            updates.append("result = ?")
            params.append(result)
        if feedback:
            updates.append("feedback = ?")
            params.append(feedback)
            
        if not updates:
            return False
            
        params.append(interview_id)
        query = f"UPDATE interviews SET {', '.join(updates)} WHERE id = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    # --- Recommendations / Matching ---
    def find_matching_jobs(self, skills: List[str], experience_level: str) -> List[Dict]:
        """Find jobs matching skills and experience level using simplified logic"""
        if not skills:
            return []
            
        # Base query
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []
        
        # Filter by experience if provided (optional or strict?)
        # Let's be lenient for now or strict depending on agent logic. 
        # Agent was strict: WHERE experience_level = ?
        if experience_level:
             # Normalize experience level to match DB values if needed
             # For now assume exact match or partial match
             pass 
             # query += " AND experience_level = ?"
             # params.append(experience_level)
        
        # OR logic for skills like the original agent
        if skills:
            query += " AND ("
            conditions = []
            for skill in skills:
                conditions.append("requirements LIKE ?")
                params.append(f"%{skill}%")
            query += " OR ".join(conditions) + ")"
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                d = dict(row)
                d["requirements"] = json.loads(d["requirements"]) if d["requirements"] else []
                results.append(d)
            return results

    def save_recommendation(self, job_id: int, candidate_id: int, match_score: float, explanation: str):
        # Check if exists
        check_query = "SELECT id FROM recommendations WHERE job_id = ? AND candidate_id = ?"
        
        insert_query = """
        INSERT INTO recommendations (job_id, candidate_id, match_score, explanation)
        VALUES (?, ?, ?, ?)
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(check_query, (job_id, candidate_id))
            if cursor.fetchone():
                return None
                
            cursor.execute(insert_query, (job_id, candidate_id, match_score, explanation))
            return cursor.lastrowid

    def get_recommendations_for_candidate(self, candidate_id: int):
        query = """
        SELECT r.*, j.title, j.company_id, j.location, j.type, c.name as company_name
        FROM recommendations r
        JOIN jobs j ON r.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE r.candidate_id = ?
        ORDER BY r.match_score DESC
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
# Global database instance  
db = JobDatabase()
