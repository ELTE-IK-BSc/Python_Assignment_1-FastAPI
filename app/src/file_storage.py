import json
from .models import Event


class EventFileManager:

    def __init__(self):
        self.FILE_PATH = "event.json"

    def read_events_from_file(self) -> list[Event]:
        event_list = []
        with open(self.FILE_PATH, "r") as read_file:
            data = json.load(read_file)
            for event_data in data:
                event = Event(**event_data)
                event_list.append(event)
        return event_list

    def write_events_to_file(self, eventlist: list[Event]):
        with open(self.FILE_PATH, "w") as file:
            serializableEvents = list(map(lambda event: event.model_dump(), eventlist))
            data = json.dumps(serializableEvents)
            file.write(data)

    def event_ids(self, eventlist: list[Event]) -> list[int]:
        return list(map(lambda ev: ev.id, eventlist))

    def isValidId(self, id: int, eventlist: list[Event]) -> bool:
        return id in self.event_ids(eventlist)
