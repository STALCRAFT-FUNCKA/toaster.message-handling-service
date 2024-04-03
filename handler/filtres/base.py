from vk_api import VkApi, VkApiError
from db import db
from tools.keyboards import SnackbarAnswer
from .abc import ABCHandler


class BaseFilter(ABCHandler):
    """Command handler base class.
    """
    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api


    def snackbar(self, event: dict, text: str):
        """Sends a snackbar to the user.

        Args:
            event (ButtonEvent): VK button_pressed custom event.
            text (str): Sncakbar text.
        """
        self.api.messages.sendMessageEventAnswer(
            event_id=event.get("button_event_id"),
            user_id=event.get("user_id"),
            peer_id=event.get("peer_id"),
            event_data=SnackbarAnswer(text).data
        )


    @staticmethod
    def _is_anabled(event: dict, field_name: str, setting_name: str) -> bool:
        setting = db.execute.select(
            schema="toaster_settings",
            table=field_name,
            fields=(field_name,),
            conv_id=event.get("peer_id"),
            system_name=setting_name
        )

        return bool(setting[0][0]) if setting else False


    @staticmethod
    def _has_content(event: dict, content_name: str) -> bool:
        content = event.get("attachments")
        return content_name in content


    def delete_own_message(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """
        try:
            self.api.messages.delete(
                delete_for_all=1,
                peer_id=event.get("peer_id"),
                cmids=event.get("cmid")
            )

        except VkApiError:
            ...


    async def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me
