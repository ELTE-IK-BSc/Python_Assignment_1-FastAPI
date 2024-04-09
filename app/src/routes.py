from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer
from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    events = EFM.read_events_from_file()
    # Return all events from JSON file
    return events


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(
    date: str = None, organizer: str = None, status: str = None, event_type: str = None
):
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()

    # The eventFilterer function checks for an given event if all the not None conditionals are True
    def eventFilterer(event: Event) -> bool:
        filtered = True
        if date:
            # Check for given date
            filtered = filtered and event.date == date
        if organizer:
            # Check for given organizer
            filtered = filtered and event.organizer.name == organizer
        if status:
            # Check for given status
            filtered = filtered and event.status == status
        if event_type:
            # Check for given type
            filtered = filtered and event.type == event_type

        # Return result True if all conditions met and False if any of is fasle
        return filtered

    # Filter events with eventFilterer
    filtered = filter(eventFilterer, allEvents)
    # Return filtered events
    return list(filtered)


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()
    # Check if event_id is a real/taken event id
    if EFM.isValidId(event_id, allEvents):
        # If a real id go over the events and return the right one
        for event in allEvents:
            # Check for the event by id and return it
            if event.id == event_id:
                return event
    # Else Raise exception because event_id is not a real id
    else:
        raise HTTPException(status_code=422, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()

    # Check if event_id is a real/taken event id
    if not EFM.isValidId(event.id, allEvents):
        #  If not than add new event to the list
        allEvents.append(event)
        # Write out all events into the JSON file
        EFM.write_events_to_file(allEvents)
        # Return with the new event
        return event
    else:
        # Else Raise exception because event_id is already taken
        raise HTTPException(status_code=422, detail="Event ID already exists")


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()

    # Check if event_id is a real/taken event id
    if EFM.isValidId(event_id, allEvents):
        # If a real id go over the events and update the right one
        updatedEvents = list(map(lambda e: e if e.id != event_id else event, allEvents))
        # Write out changes int the JSON file
        EFM.write_events_to_file(updatedEvents)
        # Return with the updated event
        return event
    else:
        # Else Raise exception because event_id is not a real id
        raise HTTPException(status_code=422, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    # Create EventFileManager instance
    EFM = EventFileManager()
    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()

    # Check if event_id is a real/taken event id
    if EFM.isValidId(event_id, allEvents):
        # If a real id go over the events
        for event in allEvents:
            # Check for the event by id the remove it
            if event.id == event_id:
                allEvents.remove(event)
                break
        # Write out changes int the JSON file
        EFM.write_events_to_file(allEvents)
        # Return afformation message
        return "Event deleted successfully"
    else:
        # Else Raise exception because event_id is not a real id
        raise HTTPException(status_code=422, detail="Event not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    # Create EventFileManager instance
    EFM = EventFileManager()

    # Get all events from JSON file
    allEvents = EFM.read_events_from_file()

    # Filter joiners using get_joiners_multiple_meetings_method
    multiJoiners = EventAnalyzer.get_joiners_multiple_meetings_method(allEvents)

    # Check if has any multi joiner int the list
    if len(multiJoiners) > 0:
        # If list has at least one joiner then return list
        return multiJoiners
    else:
        # Else return str error message
        return "No joiners attending at least 2 meetings"
