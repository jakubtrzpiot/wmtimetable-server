from pydantic import BaseModel

class Lesson(BaseModel):
    name: str
    teacher: str
    classroom: str
    startTime: str
    endTime: str
    type: str
    group: str

class Day(BaseModel): list[Lesson]

class Week(BaseModel):
    monday: Day
    tuesday: Day
    wednesday: Day
    thursday: Day
    friday: Day
    saturday: Day
    sunday: Day


class Timetable(BaseModel):
    oddWeek: list[Day]
    evenWeek: list[Day]

class GroupTimetable(BaseModel):
    id: int
    group: str
    timetable: Timetable
    version: str

class Timetables(BaseModel): list[GroupTimetable]


