# 🤖 AI Recruiter Agency

An AI-native recruitment platform that leverages a multi-agent system to automate and enhance the job application and screening process. Built with a production-hardened Django backend and a premium React frontend.

## 🌟 Key Features

- **Multi-Agent AI Engine**: Specialized agents for resume extraction, skill analysis, and job matching.
- **Market Readiness Scoring**: Real-time AI analysis of resumes with quantified feedback.
- **Superpowers & Gaps**: Visual breakdown of candidate strengths and growth areas.
- **SQL Server Persistence**: All AI insights are permanently stored in SQL Server 2022.
- **JWT Authentication**: Role-based access control for Candidates and Recruiters.
- **Production Hardened**: Pre-configured with SSL, HSTS, and secure cookie settings.

## 🛠 Tech Stack

- **Frontend**: React.js, Vite, Vanilla CSS (Premium Glassmorphism), Lucide Icons.
- **Backend**: Django, Django REST Framework, SimpleJWT.
- **Database**: SQL Server 2022 (Primary), SQLite (optional local dev).
- **AI**: Multi-agent orchestration with audit logging.
- **DevOps**: Docker, Docker Compose.

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- SQL Server (or use the provided Docker setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-recruiter-agency
   ```

2. **Backend Setup**
   ```bash
   cd backend_django
   python -m venv .venv
   source .venv/bin/button/activate  # or .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Configure your settings
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd ui
   npm install
   npm run dev
   ```

## 🏗 Architecture

### AI Multi-Agent System
Our proprietary AI engine uses a directed workflow:
1. **Orchestrator**: Manages state and transitions.
2. **Extractor**: Converts unstructured resumes (PDF/Docx) into structured entities.
3. **Analyzer**: Normalizes skills and evaluates technical depth.
4. **Matcher**: Calculates compatibility between candidates and active jobs.

### Database Schema
The project uses a normalized schema designed for high-performance SQL Server environments. See `/db/schema_mssql.sql` for the full definition.

## 📊 Presentation Materials
For a detailed guide on project features and implementation details for demonstrations, see [PRESENTATION_GUIDE.md](./PRESENTATION_GUIDE.md).

---
Built with ❤️ by the AI Recruiter Team.
