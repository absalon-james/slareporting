import client
import logging

from utils import timestamp_to_datetime

logger = logging.getLogger(__name__)


class Event:
    """Models a notification event."""

    def __init__(self, state, previous_state, timestamp):
        """Inits the event

        :param state: This state
        :type state: str
        :param previous_state: Previous state
        :type previous_state: str
        :param timestamp: Number of milliseconds since epoch
        :type timestamp: int
        """
        self.state = state
        self.previous_state = previous_state
        self.timestamp = timestamp

    def __repr__(self):
        """Convenience method for logging/printing.

        :returns: Representation of the event
        :rtype: str
        """
        return "{}---to {} from {}".format(
            self.timestamp,
            self.state,
            self.previous_state
        )


class Alarm:
    """Report model for an alarm."""

    def __init__(self, entity, check, alarm):
        """Init the alarm report

        :param entity: Maas entity object
        :type entity: ?
        :param check: Maas check object
        :type check: ?
        :param alarm: Maas alarm object
        :type ?:
        """
        self.driver = client.get_instance()
        self.entity = entity
        self.check = check
        self.alarm = alarm

        # This will be changed every time the report is run.
        self.events = None

    def history(self):
        """Get notification history for the alarm.

        :returns: List of event objects
        :rtype: list
        """
        events = []
        history = self.driver.ex_list_alarm_notification_history(
            self.entity,
            self.alarm,
            self.check
        )
        for event in history:
            events.append(Event(
                event['state'],
                event['previous_state'],
                event['timestamp']
            ))
        return events

    def assume_ends(self, start, stop):
        """Assume some ending data points.

        Notifications won't typically occur on time window boundaries.

        @TODO - Figure out what to do with checks dissappearing
        mid time window

        :param start: Starting time in milliseconds
        :type start: int
        :param stop: Stopping time in milliseconds
        :type stop: int
        """
        # Don't assume anything if no data points.
        if not self.events:
            return
        # Assume a data point at the beginning of the window
        if self.events[0].timestamp > start:
            self.events.insert(0, Event(
                self.events[0].previous_state,
                None,
                start
            ))
        # Assume a data point at the end of the window
        if self.events[-1].timestamp < stop:
            self.events.append(Event(
                self.events[-1].state,
                self.events[-1].state,
                stop
            ))

    def from_file(self, filename):
        """Load event data from a file.

        :param filename: Name of csv file containing data.
        :type filename: str
        """
        pass

    def from_api(self, entity, check, alarm):
        """Load event data from api

        :param entity: Maas entity object
        :type entity: ?
        :param check: Maas check object
        :type check: ?
        :param alarm: Maas alarm object
        :type alarm: ?
        """
        pass

    def run(self, start, stop):
        """Runs the report for provided time window.

        :param start: Starting time in milliseconds
        :type start: int
        :param stop: Stopping time in milliseconds
        :type stop: int
        :returns: ?
        :rtype: ?
        """
        def timefilter(e):
            return e.timestamp >= start and e.timestamp <= stop

        # Get events between provided time window
        self.events = filter(timefilter, self.history())
        self.assume_ends(start, stop)
        for i, event in enumerate(self.events[:-1]):
            event_start = timestamp_to_datetime(event.timestamp)
            event_stop = timestamp_to_datetime(self.events[i + 1].timestamp)
            yield {
                'entity_id': self.entity.id,
                'entity_label': self.entity.label,
                'check_id': self.check.id,
                'check_label': self.check.label,
                'alarm_id': self.alarm.id,
                'alarm_label': self.alarm.label,
                'valid': True,
                'state': event.state,
                'duration': self.events[i + 1].timestamp - event.timestamp,
                'start': event_start.isoformat(),
                'stop': event_stop.isoformat()
            }
