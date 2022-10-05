import logging

from services.db_service import db_service
from services.logger_service import set_log_configuration

set_log_configuration()

logger = logging.getLogger(__name__)


async def startup_event():
    """
    On application start creates sqlalchemy engine
    """
    logger.info("Creating DB Engine")
    db_service.create_engine()
    logger.info("DB Engine Creation Finished")


async def shutdown_event():
    """
    On application shutdown disposes sqlalchemy engine
    """
    logger.info("Disposing DB Engine")
    db_service.dispose_engine()
    logger.info("DB Engine Dispose Finished")
