from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import questions, answers
from .config import settings
from .utils.logging import logger

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API service for managing questions and answers"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Q&A API Service", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}