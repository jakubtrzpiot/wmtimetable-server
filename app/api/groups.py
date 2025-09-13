from ..types.groups import Groups
from fastapi import APIRouter
from typing import Union

router = APIRouter()

@router.get("/groups")
def get_groups() -> Groups:
    """Return a list of all group names."""
    return dict
