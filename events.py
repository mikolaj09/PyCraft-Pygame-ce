

class Event:

    def __init__(self, name: int):
        self.name = name

    def start(self, *args, **kwargs):
        pass


class EventManager:

    def __init__(self):
        self.active_events = set()
        self.active_events_names = set()

    def active(self, event_name: int) -> bool:
        return event_name in self.active_events_names

    def start_event(self, event_name: int) -> None:
        self.active_events_names.add(event_name)
        self.active_events.add(Event(event_name))

    def stop_event(self, event_name: int) -> None:
        if self.active(event_name):
            self.active_events_names.remove(event_name)
            self.active_events.remove(self.get_event(event_name))

    def get_event(self, event_name: int) -> Event or None:
        if self.active(event_name):
            for event in self.active_events:
                if event.name == event_name:
                    return event
        return None


event_manager = EventManager()
