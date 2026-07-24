from fastapi import FastAPI, HTTPException, status
from app.schemas import TelemetryEvent, IngestionResponse
from app.services.rate_limiter import rate_limiter
import uuid

app = FastAPI(
    title="High-Throughput Event Streaming Pipeline",
    version="1.0.0",
    description="Real-time event ingestion and analytics engine"
)

# In-memory buffer to hold ingested events before processing
EVENT_BUFFER = []

@app.get("/")
def read_root():
    return {"service": "Event Ingestion Engine", "status": "active"}

@app.post(
    "/api/v1/events", 
    response_model=IngestionResponse, 
    status_code=status.HTTP_202_ACCEPTED
)
async def ingest_event(event: TelemetryEvent):
    # 1. Enforce Rate Limiting
    if not rate_limiter.is_allowed(event.client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded for client '{event.client_id}'."
        )

    # 2. Assign unique ID and buffer the event
    event_id = str(uuid.uuid4())
    buffered_payload = {
        "event_id": event_id,
        "client_id": event.client_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp,
        "payload": event.payload
    }
    EVENT_BUFFER.append(buffered_payload)

    return IngestionResponse(
        status="accepted",
        message="Event received successfully.",
        event_id=event_id
    )

@app.get("/api/v1/stats")
def get_stats():
    return {
        "total_buffered_events": len(EVENT_BUFFER),
        "buffer_preview": EVENT_BUFFER[-5:]  # Last 5 events
    }