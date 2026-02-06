-- =========================================================
-- AI Recruiter Agency - Master Schema (SQL Server)
-- Version: 2.0 (Production Grade)
-- Redesigned for Scalability, Integrity, and Performance
-- =========================================================

-- 1) USERS Table (Centralized Auth)
CREATE TABLE users (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(MAX) NOT NULL,
    role NVARCHAR(50) NOT NULL DEFAULT 'candidate', -- 'admin', 'recruiter', 'candidate'
    first_name NVARCHAR(100),
    last_name NVARCHAR(100),
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 2) COMPANIES Table
CREATE TABLE companies (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    name NVARCHAR(255) NOT NULL UNIQUE,
    industry NVARCHAR(100),
    location NVARCHAR(255),
    website NVARCHAR(2048),
    contact_email NVARCHAR(255),
    description NVARCHAR(MAX),
    logo_url NVARCHAR(2048),
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO
CREATE INDEX IX_Companies_Name ON companies(name);
GO

-- 3) JOBS Table
CREATE TABLE jobs (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title NVARCHAR(255) NOT NULL,
    location NVARCHAR(255),
    type NVARCHAR(50), -- 'Full-time', 'Contract', etc.
    experience_level NVARCHAR(50), -- 'Junior', 'Mid', 'Senior'
    salary_range NVARCHAR(100),
    description NVARCHAR(MAX),
    requirements_json NVARCHAR(MAX), -- JSON: ["Python", "Django"] (Quick cache)
    benefits_json NVARCHAR(MAX),     -- JSON: ["Health", "Remote"]
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO
CREATE INDEX IX_Jobs_Title ON jobs(title);
CREATE INDEX IX_Jobs_Company ON jobs(company_id);
GO

-- 4) CANDIDATES Table
CREATE TABLE candidates (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL, -- distinct from users.email just in case
    phone NVARCHAR(50),
    location NVARCHAR(255),
    experience_level NVARCHAR(50),
    resume_url NVARCHAR(2048),
    linkedin_url NVARCHAR(2048),
    portfolio_url NVARCHAR(2048),
    
    -- AI Analysis Cache (Normalized data in `skills` table, but full report here)
    analysis_report_json NVARCHAR(MAX), -- Full logic/reasoning from AI
    
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO
CREATE INDEX IX_Candidates_User ON candidates(user_id);
GO

-- 5) APPLICATIONS Table
CREATE TABLE applications (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    candidate_id BIGINT NOT NULL REFERENCES candidates(id) ON DELETE NO ACTION, -- Prevent cycles/cascades if needed
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status NVARCHAR(50) NOT NULL DEFAULT 'applied', -- 'applied', 'screening', 'interview', 'offer', 'rejected'
    ai_score FLOAT, -- 0.0 to 100.0
    ai_feedback NVARCHAR(MAX),
    applied_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO
CREATE INDEX IX_Applications_Candidate_Job ON applications(candidate_id, job_id);
GO

-- 6) INTERVIEWS Table
CREATE TABLE interviews (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    interviewer_id BIGINT REFERENCES users(id), -- User conducting interview
    scheduled_time DATETIME2 NOT NULL,
    meeting_link NVARCHAR(2048),
    status NVARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'completed', 'cancelled'
    feedback NVARCHAR(MAX),
    result NVARCHAR(50),
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 7) SKILLS Table (Normalized)
CREATE TABLE skills (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE
);
GO

CREATE TABLE candidate_skills (
    candidate_id BIGINT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    skill_id BIGINT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    proficiency NVARCHAR(50), -- 'Beginner', 'Expert'
    PRIMARY KEY (candidate_id, skill_id)
);
GO

CREATE TABLE job_skills (
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id BIGINT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    is_required BIT DEFAULT 1,
    PRIMARY KEY (job_id, skill_id)
);
GO

-- 8) AI AGENTS & LOGS (Explainability)
CREATE TABLE ai_agents (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    version NVARCHAR(50),
    description NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

CREATE TABLE ai_logs (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    agent_id BIGINT REFERENCES ai_agents(id),
    action_type NVARCHAR(100), -- 'ResumeAnalysis', 'MatchScoring'
    input_data NVARCHAR(MAX), -- JSON snapshot
    output_data NVARCHAR(MAX), -- JSON result
    execution_time_ms INT,
    created_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO
