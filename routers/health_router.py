from datetime import datetime

from routers import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

started = datetime.now()


@router.get("/", include_in_schema=False)
def health():
    """
    Checks health of API
    Returns:
        uptime
    """
    return {"started": started, "uptime": (datetime.now() - started).total_seconds()}
