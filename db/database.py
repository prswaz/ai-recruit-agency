import pyodbc
import json
import hashlib


class JobDatabaseSQLServer:
    def __init__(self, server, database, username, password):
        self.conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        self._connect()

    def _connect(self):
        self.conn = pyodbc.connect(self.conn_str)
        self.conn.autocommit = True

    # =====================================================
    # USERS
    # =====================================================
    def add_user(self, email: str, password: str, role: str = "candidate") -> int:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
        INSERT INTO users (email, password_hash, role)
        VALUES (?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (email, password_hash, role))
            user_id = cursor.fetchval()
            return int(user_id)
        except pyodbc.IntegrityError:
            raise ValueError("Email already exists")

    def get_user_by_email(self, email: str):
        query = "SELECT * FROM users WHERE email = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        return row

    # =====================================================
    # COMPANIES
    # =====================================================
    def add_company(self, company_data: dict) -> int:
        query = """
        INSERT INTO companies (user_id, name, industry, location, website, contact_email)
        VALUES (?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        cursor.execute(
            query,
            (
                company_data["user_id"],
                company_data["name"],
                company_data.get("industry"),
                company_data.get("location"),
                company_data.get("website"),
                company_data.get("contact_email"),
            ),
        )
        return int(cursor.fetchval())

    # =====================================================
    # JOBS
    # =====================================================
    def add_job(self, job_data: dict) -> int:
        query = """
        INSERT INTO jobs
        (title, company_id, location, type, experience_level,
         salary_range, description, requirements, benefits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        cursor.execute(
            query,
            (
                job_data["title"],
                job_data["company_id"],
                job_data.get("location"),
                job_data.get("type"),
                job_data.get("experience_level"),
                job_data.get("salary_range"),
                job_data.get("description"),
                json.dumps(job_data.get("requirements", [])),
                json.dumps(job_data.get("benefits", [])),
            ),
        )
        return int(cursor.fetchval())

    def get_all_jobs(self):
        query = """
        SELECT j.id, j.title, c.name AS company_name,
               j.location, j.experience_level, j.salary_range,
               j.description, j.requirements, j.benefits
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        ORDER BY j.created_at DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(
                {
                    "id": row.id,
                    "title": row.title,
                    "company": row.company_name,
                    "location": row.location,
                    "experience_level": row.experience_level,
                    "salary_range": row.salary_range,
                    "description": row.description,
                    "requirements": json.loads(row.requirements),
                    "benefits": json.loads(row.benefits),
                }
            )
        return result

    # =====================================================
    # CANDIDATES
    # =====================================================
    def add_candidate(self, candidate_data: dict) -> int:
        query = """
        INSERT INTO candidates
        (user_id, full_name, email, phone, location,
         experience_level, resume_url, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        cursor.execute(
            query,
            (
                candidate_data["user_id"],
                candidate_data["full_name"],
                candidate_data["email"],
                candidate_data.get("phone"),
                candidate_data.get("location"),
                candidate_data.get("experience_level"),
                candidate_data.get("resume_url"),
                json.dumps(candidate_data.get("skills", [])),
            ),
        )
        return int(cursor.fetchval())

    def get_candidate_by_email(self, email: str):
        query = "SELECT * FROM candidates WHERE email = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (email,))
        return cursor.fetchone()

    # =====================================================
    # APPLICATIONS
    # =====================================================
    def add_application(self, application_data: dict) -> int:
        query = """
        INSERT INTO applications (candidate_id, job_id, status, source)
        VALUES (?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        cursor.execute(
            query,
            (
                application_data["candidate_id"],
                application_data["job_id"],
                application_data.get("status", "applied"),
                application_data.get("source"),
            ),
        )
        return int(cursor.fetchval())

    def get_applications_for_candidate(self, candidate_id: int):
        query = """
        SELECT a.id, a.status, a.applied_at,
               j.title AS job_title,
               c.name AS company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE a.candidate_id = ?
        ORDER BY a.applied_at DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (candidate_id,))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================
    def get_recommendations(self, candidate_id: int):
        query = """
        SELECT j.title, r.match_score, r.explanation
        FROM recommendations r
        JOIN jobs j ON r.job_id = j.id
        WHERE r.candidate_id = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (candidate_id,))
        rows = cursor.fetchall()
        return [
            {
                "job_title": row[0],
                "match_score": row[1],
                "explanation": row[2],
            }
            for row in rows
        ]
