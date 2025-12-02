from fastapi import Depends
from pymongo.database import Database

from app.db.db_vitals import get_database
from app.db.repos.setting_repository import SettingRepository
from app.setting_service import SettingService


def get_setting_service(db: Database = Depends(get_database)) -> SettingService:
    svc = SettingService()
    repo = SettingRepository(db)
    svc.set_repository(repo)
    return svc
