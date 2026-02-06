from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .services.database import db
from .routers import auth, jobs, candidates, recommendations, ai_processing, interviews

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.init_db()
    yield
    # Shutdown

app = FastAPI(title="AI Recruiter Agency API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(recommendations.router)
app.include_router(ai_processing.router)
app.include_router(interviews.router)

@app.get("/")
async def root():
    return {"message": "AI Recruiter Agency API is running"}
