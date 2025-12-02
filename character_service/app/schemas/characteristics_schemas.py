from pydantic import BaseModel


class CharacteristicsSheetCreate(BaseModel):
    str_score: int
    dex_score: int
    con_score: int
    int_score: int
    wis_score: int
    cha_score: int


class CharacteristicsSheetResponse(BaseModel):
    id: int
    str_score: int
    dex_score: int
    con_score: int
    int_score: int
    wis_score: int
    cha_score: int

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            str_score=obj.str_score,
            dex_score=obj.dex_score,
            con_score=obj.con_score,
            int_score=obj.int_score,
            wis_score=obj.wis_score,
            cha_score=obj.cha_score,
        )
