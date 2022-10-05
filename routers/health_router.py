from datetime import datetime

from routers import APIRouter
from schemas.health_schema import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

started = datetime.now()


@router.get("/", response_model=HealthResponse)
def health():
    """
    Checks health of API
    Returns:
        uptime
    """
    return HealthResponse(
        started=started, uptime=(datetime.now() - started).total_seconds()
    )
