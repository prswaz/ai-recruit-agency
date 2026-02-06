# 🗺️ Technical Feature Mapping

Use this guide to jump to specific files during a technical deep-dive or presentation.

## 1. AI Logic & Orchestration
*   **Orchestrator Agent**: `backend_django/agents/orchestrator.py`
    *   *Where the multi-agent flow is defined.*
*   **Agent Manager (Singleton)**: `backend_django/ai_engine/agent_manager.py`
    *   *Handles interaction with AI models and logging.*
*   **Resume Analysis Service**: `backend_django/candidates/services.py`
    *   *Encapsulates the business logic for processing resumes.*

## 2. API & Backend Structure
*   **Database Schema**: `db/schema_mssql.sql`
*   **Production Settings**: `backend_django/ai_recruiter_django/settings.py`
    *   *Look for `CORS`, `MIDDLEWARE`, and `DATABASES`.*
*   **Candidate Views**: `backend_django/candidates/views.py`
    *   *Endpoints for AI analysis and profile management.*
*   **Authentication Serializers**: `backend_django/authentication/serializers.py`
    *   *Custom logic for email-based login and token claims.*

## 3. Frontend UI Components
*   **AI Insight Card**: `ui/src/components/MatchIntelligenceCard.jsx`
    *   *The visual representation of AI analysis scores.*
*   **Candidate Dashboard**: `ui/src/pages/Dashboard.jsx`
    *   *Main landing for users with stats and job matches.*
*   **API Service**: `ui/src/services/api.js`
    *   *Axios configuration and interceptors for JWT.*

## 4. Models & Persistence
*   **Audit Logs**: `backend_django/ai_engine/models.py` (`AILog` model)
*   **Jobs & Applications**: `backend_django/core/models.py`
*   **User Profiles**: `backend_django/candidates/models.py`
