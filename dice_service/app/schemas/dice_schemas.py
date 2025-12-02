from fastapi import Query
from pydantic import BaseModel


class DiceRollResponse(BaseModel):
    roll_result: int


class DiceRollModRequest(BaseModel):
    mod: int = Query(0, ge=-100, le=100)
    roll_count: int = Query(1, ge=1, le=100)


class DiceRollModResponse(BaseModel):
    roll_result: int
