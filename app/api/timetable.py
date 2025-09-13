from ..types.timetables import GroupTimetable
from fastapi import APIRouter
from typing import Union

router = APIRouter()

@router.get("/timetable/{group}")
def get_group_timetable(_id: int) -> GroupTimetable:
    """Return timetable for a specific group."""
    return dict

@router.get("/timetable/{group}/version")
def get_group_version(_id: int) -> str:
    """Return the version string for a specific group."""
    return ''