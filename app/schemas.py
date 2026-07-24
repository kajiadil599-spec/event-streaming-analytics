from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import time

class TelemetryEvent(BaseModel):
    client_id: str = Field(..., example="client_app_01")
    event_type: str = Field(..., example="user_click")
    timestamp: float = Field(default_factory=time.time)
    payload: Dict[str, Any] = Field(default_factory=dict)

class IngestionResponse(BaseModel):
    status: str
    message: str
    event_id: Optional[str] = None