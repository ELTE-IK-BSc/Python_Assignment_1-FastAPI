from .models import Event


class EventAnalyzer:
    def get_joiners_multiple_meetings_method(events: list[Event]):
        allJoiners = []
        multiJoiners = []
        for event in events:
            for joiner in event.joiners:
                if joiner in allJoiners:
                    multiJoiners.append(joiner)
                else:
                    allJoiners.append(joiner)
        return multiJoiners
