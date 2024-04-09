import json
from .models import Event


class EventFileManager:

    def __init__(self):
        # Intial FILE_PATH with the event file
        self.FILE_PATH = "event.json"

    def read_events_from_file(self) -> list[Event]:
        # Creat event list
        event_list = []
        # Read event JSON file
        with open(self.FILE_PATH, "r") as read_file:
            data = json.load(read_file)
            # Casting JSON evnts as Event and add to event list
            for event_data in data:
                event = Event(**event_data)
                event_list.append(event)
        return event_list

    def write_events_to_file(self, eventlist: list[Event]):
        # Write event JSON file
        with open(self.FILE_PATH, "w") as file:
            # Cast pydantic classes to dict
            serializableEvents = list(map(lambda event: event.model_dump(), eventlist))
            #  Convert list to JSON string
            data = json.dumps(serializableEvents)
            # Write out data into the file
            file.write(data)

    def event_ids(self, eventlist: list[Event]) -> list[int]:
        # return the list of taken ids
        return list(map(lambda ev: ev.id, eventlist))

    def isValidId(self, id: int, eventlist: list[Event]) -> bool:
        # return if the given id is in the taken ids lit
        return id in self.event_ids(eventlist)
