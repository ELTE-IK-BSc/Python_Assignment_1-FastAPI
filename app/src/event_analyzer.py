from .models import Event


class EventAnalyzer:
    # Analyz event joiners
    def get_joiners_multiple_meetings_method(events: list[Event]):

        # List of all joiners
        allJoiners = []
        # List of joineer who at least come up twice
        multiJoiners = []

        # Go over events
        for event in events:
            # Go over event joiners
            for joiner in event.joiners:

                # If joier appeared earlier add to multiJoiners
                if joiner in allJoiners:
                    multiJoiners.append(joiner)
                # Else joier appears first time add to allJoiners
                else:
                    allJoiners.append(joiner)

        # return filtered multi joiners who at least appeared twice
        return multiJoiners
