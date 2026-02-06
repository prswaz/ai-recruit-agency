-- =========================================================
-- 1) USERS Table (Centralized Auth)
-- =========================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'candidate', -- 'admin', 'recruiter', 'candidate'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 2) COMPANIES Table
-- =========================================================
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, -- Link to user account
    name TEXT NOT NULL UNIQUE,
    industry TEXT,
    location TEXT,
    website TEXT,
    contact_email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 3) JOBS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    location TEXT,
    type TEXT,
    experience_level TEXT,
    salary_range TEXT,
    description TEXT,
    requirements TEXT,  -- JSON format for required skills
    benefits TEXT,      -- JSON format for job benefits
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 4) CANDIDATES Table
-- =========================================================
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, -- Link to user account
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, -- Keep for easy access, should match users.email
    phone TEXT,
    location TEXT,
    experience_level TEXT,
    resume_url TEXT,
    skills TEXT,  -- JSON format for skills
    analysis_report TEXT, -- JSON format for full AI analysis (strengths, gaps, summary)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 5) APPLICATIONS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'applied',  -- e.g., 'applied', 'screening', 'interviewing', 'hired', 'rejected'
    source TEXT,  -- e.g., 'AI recommendation', 'manual submission'
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 6) INTERVIEWS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    interviewer TEXT,  -- Can link to recruiter or AI agent
    scheduled_time DATETIME NOT NULL,
    feedback TEXT,
    result TEXT,  -- 'pass', 'fail', 'pending'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 7) AI AGENTS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS ai_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    function TEXT,  -- e.g., 'matcher', 'screening', 'outreach'
    model_version TEXT,
    last_active DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 8) RECOMMENDATIONS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    ai_agent_id INTEGER REFERENCES ai_agents(id) ON DELETE SET NULL,
    match_score REAL NOT NULL,  -- e.g., a score between 0 and 1
    explanation TEXT,  -- AI-generated rationale for the match
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 9) FEEDBACK LOG Table
-- =========================================================
CREATE TABLE IF NOT EXISTS feedback_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,  -- e.g., 'recommendation', 'interview', 'application'
    entity_id INTEGER NOT NULL,  -- ID of the referenced entity
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),  -- Rating from 1 to 5
    comments TEXT,
    submitted_by TEXT,  -- e.g., 'recruiter', 'candidate', 'ai'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 10) SKILLS Table
-- =========================================================
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS candidate_skills (
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (candidate_id, skill_id)
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);
