# pipeline_fallback.py - Windows-compatible simplified backend
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import random
from datetime import datetime

app = FastAPI(title="MNEMO Engine (Fallback)")

# Enable CORS for your HTML frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock vector store (in-memory for demo)
vector_index = []
stream_events = []

class QueryRequest(BaseModel):
    question: str

@app.post("/api/query")
async def query_engine(req: QueryRequest):
    """Mock query endpoint - simulates real-time search"""
    await asyncio.sleep(random.uniform(0.3, 0.8))  # Simulate latency
    
    # Simple keyword-based mock response
    q = req.question.lower()
    if "changed" in q or "last 10 minutes" in q:
        answer = "In the last 10 minutes, MNEMO detected: (1) CRM updated 847 customer records, (2) product pricing modified for 14 SKUs (+3.2% avg), (3) 23 support tickets moved to 'In Progress'. All reflected in live index."
        sources = ["CRM_delta_sync", "pricing_db_v2", "support_tickets.db"]
    elif "roadmap" in q or "pdf" in q:
        answer = "Q2 2026 roadmap outlines: real-time analytics dashboard (P0, April), API v3 migration (P0, March), mobile app launch (P1, May), infrastructure cost optimization (P2). References 3 external dependencies."
        sources = ["Q2_roadmap_2026.pdf", "staffing_plan_2026.xlsx"]
    else:
        answer = f"Based on {len(vector_index)} indexed vectors: Your query about '{req.question[:50]}...' matches 3 relevant documents. In production, this would retrieve fresh context from your live data streams."
        sources = ["mock_source_1", "mock_source_2"]
    
    return {
        "answer": answer,
        "sources": sources,
        "latency_ms": random.randint(35, 75),
        "vectors_searched": len(vector_index)
    }

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    """Simulates live data stream events for the frontend"""
    await websocket.accept()
    
    mock_events = [
        {"source": "DB", "content": "Updated 847 customer records — delta sync", "badge": "INDEXED"},
        {"source": "API", "content": "GitHub webhook: 3 new commits to main", "badge": "VECTORIZED"},
        {"source": "FILE", "content": "New file: Q2_roadmap_2026.pdf — chunking...", "badge": "PROCESSING"},
        {"source": "WEB", "content": "Competitor pricing crawled — 2 changes detected", "badge": "INDEXED"},
        {"source": "DB", "content": "ticket_status changed for 23 rows → vectors updated", "badge": "UPDATED"},
    ]
    
    while True:
        event = random.choice(mock_events)
        event["time"] = datetime.now().strftime("%H:%M:%S")
        await websocket.send_json(event)
        await asyncio.sleep(random.uniform(2.5, 4.5))  # Random interval

@app.get("/api/stats")
async def get_stats():
    """Return mock metrics for the dashboard"""
    return {
        "vectors_in_index": 247432 + random.randint(0, 100),
        "ingestion_latency_ms": random.randint(30, 60),
        "reingestion_rate": 0,
        "answer_accuracy": round(99.5 + random.random() * 0.5, 1),
        "live_sources": 8
    }

# Optional: Add a simple vector ingestion endpoint
@app.post("/api/ingest")
async def ingest_document(text: str, source: str = "unknown"):
    """Mock document ingestion - adds to in-memory index"""
    vector_index.append({
        "id": len(vector_index) + 1,
        "text": text[:200],  # Truncate for demo
        "source": source,
        "timestamp": time.time()
    })
    stream_events.append({
        "type": "ingest",
        "source": source,
        "count": len(vector_index),
        "time": datetime.now().isoformat()
    })
    return {"status": "indexed", "vector_id": len(vector_index)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 MNEMO Fallback Engine starting on http://localhost:8001")
    print("💡 Connect your HTML frontend to this backend")
    uvicorn.run(app, host="0.0.0.0", port=8001)