from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from settings import app_config

Base = declarative_base()


class DBService:
    engine = None

    def create_engine(self):
        """
        Creates sqlalchemy db engine
        Returns:
            created engine
        """
        self.engine = create_engine(app_config.get("DB_URI"))
        return self.engine

    def dispose_engine(self):
        """
        Disposes engine
        """
        self.engine.dispose()


db_service = DBService()
