from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    started: datetime
    uptime: int
