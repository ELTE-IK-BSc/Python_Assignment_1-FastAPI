from .file_storage import EventFileManager
from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    EFM = EventFileManager()
    events = EFM.read_events_from_file()
    return events


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(
    date: str = None, organizer: str = None, status: str = None, event_type: str = None
):
    EFM = EventFileManager()
    allEvents = EFM.read_events_from_file()

    def eventFilter(event: Event) -> bool:
        filtered = True
        if date:
            filtered = filtered and event.date == date
        if organizer:
            filtered = filtered and event.organizer.name == organizer
        if status:
            filtered = filtered and event.status == status
        if event_type:
            filtered = filtered and event.type == event_type
        return filtered

    filtered = filter(eventFilter, allEvents)
    return list(filtered)


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    pass


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    pass


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    pass


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    pass


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
