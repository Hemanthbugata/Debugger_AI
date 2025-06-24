from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.debug import router as debug_router
from app.api.feedback import router as feedback_router

app = FastAPI(
    title="Agent Debugger AI Backend",
    description="AI-powered debugging using Stack Overflow and Reddit",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(debug_router, prefix="/debug", tags=["Debug"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])