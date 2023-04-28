import logging

from services.db_service import db_service
from services.logger_service import set_log_configuration

set_log_configuration()

logger = logging.getLogger(__name__)


async def shutdown_event():
    """
    On application shutdown disposes sqlalchemy engine
    """
    logger.info("Disposing DB Engine")
    db_service.dispose_engine()
    logger.info("DB Engine Dispose Finished")
