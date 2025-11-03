"""
Legal Advisory System v8.0 - FastAPI REST API
Deployment-ready API for Railway/Cloud platforms

Endpoints:
- POST /api/ask - Submit a legal query
- GET /api/health - Health check
- GET /api/info - System information
"""

import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'api'))

from conversational_interface import ConversationalInterface

# Initialize FastAPI app
app = FastAPI(
    title="Legal Advisory System v8.0",
    description="Zero-hallucination legal advisory system with clarifying questions and case law verification",
    version="8.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "https://*.netlify.app",
        "https://*.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize conversational interface (singleton)
conversational_interface = None


def get_interface():
    """Get or create conversational interface singleton."""
    global conversational_interface
    if conversational_interface is None:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        conversational_interface = ConversationalInterface(api_key=api_key)
    return conversational_interface


# Request/Response models
class ConversationMessage(BaseModel):
    """Single message in conversation history."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class AskRequest(BaseModel):
    """Request model for /api/ask endpoint."""
    question: str = Field(..., description="Legal question to ask", min_length=1, max_length=2000)
    conversation_history: Optional[List[ConversationMessage]] = Field(
        default=None,
        description="Previous conversation context (last 6 messages)"
    )


class ClarificationResponse(BaseModel):
    """Response when system needs clarification."""
    needs_clarification: bool = True
    clarifying_questions: List[str] = Field(..., description="Questions to help refine the query")
    original_question: str = Field(..., description="User's original question")
    confidence: float = Field(..., description="Current confidence score (0-1)")
    source_module: str = Field(..., description="Best matching module")


class DirectAnswerResponse(BaseModel):
    """Response with direct answer."""
    needs_clarification: bool = False
    answer: str = Field(..., description="Natural language answer")
    confidence: float = Field(..., description="Confidence score (0-1)")
    citations: List[str] = Field(..., description="Legal citations")
    source_module: str = Field(..., description="Module that provided the answer")
    reasoning_chain: List[Dict[str, Any]] = Field(..., description="Full reasoning chain")
    hybrid_score: float = Field(..., description="Hybrid search score")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str
    anthropic_api_configured: bool


class InfoResponse(BaseModel):
    """System information response."""
    name: str
    version: str
    description: str
    features: List[str]
    available_modules: List[str]
    confidence_threshold: float


# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Legal Advisory System v8.0 API",
        "docs": "/api/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="8.0.0",
        anthropic_api_configured=bool(os.getenv('ANTHROPIC_API_KEY'))
    )


@app.get("/api/info", response_model=InfoResponse)
async def system_info():
    """Get system information and capabilities."""
    return InfoResponse(
        name="Legal Advisory System",
        version="8.0.0",
        description="Zero-hallucination legal advisory with clarifying questions and case law verification",
        features=[
            "Clarifying questions (< 30% confidence)",
            "Case law verification (3 layers: WHY/WHAT/WHERE)",
            "Conversation context maintenance",
            "Hybrid search (BM25 + 6D logic tree)",
            "Zero hallucination architecture (<2% error rate)"
        ],
        available_modules=[
            "Order 21: Costs Assessment",
            "Order 5: Amicable Resolution",
            "Order 14: Payment into Court"
        ],
        confidence_threshold=0.30
    )


@app.post("/api/ask")
async def ask_question(request: AskRequest):
    """
    Submit a legal question and get an answer.

    The system will either:
    1. Provide a direct answer (if confidence >= 30%)
    2. Ask clarifying questions (if confidence < 30%)

    Returns ClarificationResponse or DirectAnswerResponse.
    """
    try:
        # Get interface
        interface = get_interface()

        # Convert conversation history
        conversation_history = None
        if request.conversation_history:
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]

        # Query the system
        result = interface.ask(
            question=request.question,
            conversation_history=conversation_history
        )

        # Return appropriate response
        if result.get('needs_clarification'):
            return ClarificationResponse(
                needs_clarification=True,
                clarifying_questions=result['clarifying_questions'],
                original_question=result['original_question'],
                confidence=result['confidence'],
                source_module=result.get('source_module', 'unknown')
            )
        else:
            return DirectAnswerResponse(
                needs_clarification=False,
                answer=result['answer'],
                confidence=result['confidence'],
                citations=result['citations'],
                source_module=result['source_module'],
                reasoning_chain=result['reasoning_chain'],
                hybrid_score=result.get('hybrid_score', 0.0)
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# Development server
if __name__ == "__main__":
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it before running the server:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Run server
    port = int(os.getenv('PORT', 8000))
    print(f"🚀 Starting Legal Advisory API on port {port}")
    print(f"📚 API Documentation: http://localhost:{port}/api/docs")
    print(f"❤️  Health Check: http://localhost:{port}/api/health")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
