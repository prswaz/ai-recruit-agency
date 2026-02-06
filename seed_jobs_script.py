import sqlite3
import json
from pathlib import Path

DB_PATH = Path("db/jobs.sqlite")

def seed_jobs():
    jobs = [
        {
            "title": "Senior Frontend Engineer",
            "company": "TechFlow Systems",
            "location": "San Francisco, CA (Remote)",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary_range": "$140k - $180k",
            "description": "We are looking for an experienced React developer to lead our dashboard team.",
            "requirements": ["React", "TypeScript", "Redux", "CSS3", "Git"],
            "benefits": ["Remote work", "Health insurance", "401k"]
        },
        {
            "title": "Backend Python Developer",
            "company": "DataMinds AI",
            "location": "New York, NY",
            "type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_range": "$120k - $150k",
            "description": "Join our AI team to build robust APIs using FastAPI and Python.",
            "requirements": ["Python", "FastAPI", "SQL", "Docker", "AWS"],
            "benefits": ["Stock options", "Gym stipend", "Catered lunch"]
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupX",
            "location": "Austin, TX",
            "type": "Contract",
            "experience_level": "Entry-Level",
            "salary_range": "$80k - $100k",
            "description": "Early stage startup looking for a generalist to build our MVP.",
            "requirements": ["JavaScript", "Node.js", "React", "MongoDB"],
            "benefits": ["Flexible hours", "Learning budget"]
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudScale",
            "location": "Remote",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary_range": "$150k - $200k",
            "description": "Manage our Kubernetes clusters and CI/CD pipelines.",
            "requirements": ["Kubernetes", "Terraform", "AWS", "CI/CD", "Python"],
            "benefits": ["Unlimited PTO", "Home office stipend"]
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Visionary AI",
            "location": "Seattle, WA",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary_range": "$170k - $220k",
            "description": "Build computer vision models for autonomous vehicles.",
            "requirements": ["Python", "PyTorch", "TensorFlow", "C++", "Computer Vision"],
            "benefits": ["Relocation assistance", "Bonus"]
        },
        {
            "title": "Product Designer",
            "company": "Creative Solutions",
            "location": "Los Angeles, CA",
            "type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_range": "$110k - $140k",
            "description": "Design intuitive user interfaces for our crypto wallet app.",
            "requirements": ["Figma", "UI/UX", "Prototyping", "User Research"],
            "benefits": ["Crypto bonus", "Health"]
        },
        {
            "title": "Go Backend Engineer",
            "company": "FastPay",
            "location": "Chicago, IL",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary_range": "$160k - $190k",
            "description": "High performance payment processing systems.",
            "requirements": ["Go", "Microservices", "gRPC", "PostgreSQL"],
            "benefits": ["401k match", "Dental"]
        },
        {
            "title": "Junior Web Developer",
            "company": "Local Agency",
            "location": "Miami, FL",
            "type": "Full-time",
            "experience_level": "Junior",
            "salary_range": "$60k - $80k",
            "description": "Maintain client websites and build landing pages.",
            "requirements": ["HTML", "CSS", "JavaScript", "WordPress"],
            "benefits": ["Mentorship", "Chill culture"]
        },
        {
            "title": "Data Scientist",
            "company": "HealthAnalytica",
            "location": "Boston, MA",
            "type": "Full-time",
            "experience_level": "PhD",
            "salary_range": "$180k - $250k",
            "description": "Analyze clinical trial data to improve patient outcomes.",
            "requirements": ["Python", "R", "Statistics", "Machine Learning"],
            "benefits": ["Research budget", "Conference travel"]
        },
        {
            "title": "React Native Developer",
            "company": "MobileFirst",
            "location": "Remote",
            "type": "Contract",
            "experience_level": "Mid-Level",
            "salary_range": "$60/hr",
            "description": "Help us ship our iOS and Android app before Q4.",
            "requirements": ["React Native", "Redux", "Mobile Development"],
            "benefits": []
        }
    ]

    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get a user id to assign companies to (create one if not exists)
    cursor.execute("SELECT id FROM users WHERE role='recruiter' LIMIT 1")
    user_row = cursor.fetchone()
    if not user_row:
        print("Creating dummy recruiter user...")
        cursor.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)", 
                       ("recruiter@seed.com", "dummyhash", "recruiter"))
        user_id = cursor.lastrowid
    else:
        user_id = user_row[0]

    for job in jobs:
        # Check if company exists, else create
        cursor.execute("SELECT id FROM companies WHERE name=?", (job["company"],))
        comp_row = cursor.fetchone()
        if not comp_row:
            cursor.execute("INSERT INTO companies (user_id, name, location) VALUES (?, ?, ?)", 
                           (user_id, job["company"], job["location"]))
            company_id = cursor.lastrowid
        else:
            company_id = comp_row[0]

        # Insert Job
        print(f"Inserting job: {job['title']} at {job['company']}")
        cursor.execute("""
            INSERT INTO jobs (title, company_id, location, type, experience_level, salary_range, description, requirements, benefits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["title"], 
            company_id, 
            job["location"], 
            job["type"], 
            job["experience_level"], 
            job["salary_range"], 
            job["description"], 
            json.dumps(job["requirements"]), 
            json.dumps(job["benefits"])
        ))

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_jobs()
