from fastapi import Depends
from pymongo.database import Database

from app.db.db_vitals import get_database
from app.db.repos.wiki_repository import WikiRepository
from app.handbook_service import HandbookService


def get_handbook_service(
    db: Database = Depends(get_database),
) -> HandbookService:
    handbook_service = HandbookService()
    wiki_repository = WikiRepository(db)
    handbook_service.set_repository(wiki_repository)
    return handbook_service
