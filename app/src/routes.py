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
    EFM = EventFileManager()
    allEvents = EFM.read_events_from_file()
    if EFM.isValidId(event_id, allEvents):
        for e in allEvents:
            if e.id == event_id:
                return e
    else:
        raise HTTPException(status_code=422, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    EFM = EventFileManager()
    allEvents = EFM.read_events_from_file()
    if not EFM.isValidId(event.id, allEvents):
        allEvents.append(event)
        EFM.write_events_to_file(allEvents)
        return event
    else:
        raise HTTPException(status_code=422, detail="Event ID already exists")


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    EFM = EventFileManager()
    allEvents = EFM.read_events_from_file()
    if EFM.isValidId(event_id, allEvents):
        updatedEvents = list(map(lambda e: e if e.id != event_id else event, allEvents))
        EFM.write_events_to_file(updatedEvents)
        return event
    else:
        raise HTTPException(status_code=422, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    EFM = EventFileManager()
    allEvents = EFM.read_events_from_file()
    if EFM.isValidId(event_id, allEvents):
        for e in allEvents:
            if e.id == event_id:
                allEvents.remove(e)
                break
        EFM.write_events_to_file(allEvents)
        return "Event deleted successfully"
    else:
        raise HTTPException(status_code=422, detail="Event not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
