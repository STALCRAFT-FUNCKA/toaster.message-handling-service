"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {
        "warn": "warns",
    }

    async def initiate_warn(self, event, message, setting=None):
        queue = self.event_queues["warn"]
        data = {
            "author_id": 0,
            "author_name": "TOASTER",
            "setting": setting,
            "reason_message": message,
            "target_id": event.get("user_id"),
            "target_name": event.get("user_name"),
            "peer_id": event.get("peer_id"),
            "peer_name": event.get("peer_name"),
            "cmid": event.get("cmid"),
            "warn_count": 0,
            "target_message_cmid": event.get("cmid"),
        }
        await self._send_data(data, queue)


producer = CustomProducer()
