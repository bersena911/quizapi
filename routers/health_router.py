from datetime import datetime

from routers import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

started = datetime.now()


@router.get("/")
def health():
    """
    Checks health of API
    Returns:
        uptime
    """
    return {
        "started": started.isoformat(),
        "uptime": (datetime.now() - started).total_seconds(),
    }
