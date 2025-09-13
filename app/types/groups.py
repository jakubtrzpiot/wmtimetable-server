from pydantic import BaseModel

class Group(BaseModel):
    id: int
    name: str

class Groups(BaseModel): list[Group]