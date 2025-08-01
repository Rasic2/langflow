import json

from loguru import logger

from langflow.custom.custom_component.component import Component
from langflow.io import MessageInput, Output
from langflow.schema.data import Data
from langflow.schema.message import Message


class MessageTextToDataComponent(Component):
    display_name = "Message Text to Data"
    description = "Convert a Message['text'] to a Data object"
    icon = "message-square-share"
    name = "MessageTextToData"

    inputs = [
        MessageInput(
            name="message",
            display_name="Message",
            info="The Message object to convert to a Data object",
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="convert_message_text_to_data"),
    ]

    def convert_message_text_to_data(self) -> Data:
        if isinstance(self.message, Message):
            # Convert Message to Data
            valid_json = self.message.text.replace("'", '"')
            return Data(data=json.loads(valid_json))

        msg = "Error converting Message to Data: Input must be a Message object"
        logger.opt(exception=True).debug(msg)
        self.status = msg
        return Data(data={"error": msg})
