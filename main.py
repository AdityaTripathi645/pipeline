from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

# Allow CORS for your HTML file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mocking the Pathway Client for demonstration
# In production, this would query the VectorStoreServer running above
@app.post("/api/query")
async def query_engine(question: str):
    # 1. Search Vector Index (Real-time)
    # 2. Construct Prompt with Context
    # 3. Call LLM
    return {
        "answer": "Based on live data: CRM updated 847 records 2 mins ago.",
        "sources": ["CRM_delta_sync", "pricing_db_v2"],
        "latency_ms": 42
    }

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Simulate live stream events from Pathway
    while True:
        event = {
            "time": "12:00:00",
            "source": "DB",
            "content": "PostgreSQL: ticket_status changed for 23 rows",
            "badge": "UPDATED"
        }
        await websocket.send_json(event)
        await asyncio.sleep(3.5) # Match frontend animation speed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)