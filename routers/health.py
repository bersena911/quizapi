from datetime import datetime

from routers import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

started = datetime.now()


@router.get("/")
def health():
    return {
        "started": started.isoformat(),
        "uptime": (datetime.now() - started).total_seconds(),
    }
