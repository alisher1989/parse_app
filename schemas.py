from pydantic import BaseModel


class Record(BaseModel):
    id: int
    img: str
    price: str
    date: str

    class Config:
        orm_mode = True