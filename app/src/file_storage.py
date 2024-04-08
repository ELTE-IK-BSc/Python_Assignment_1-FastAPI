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


