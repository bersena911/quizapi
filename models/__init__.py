import os
import importlib

from services.db_service import Base  # noqa

for module in os.listdir(os.path.dirname(__file__)):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    importlib.import_module(f".{module[:-3]}", package=__package__)
