from bohrium_open_sdk.db import SQLClient

from langflow.custom.custom_component.component import Component
from langflow.inputs import DataInput, StrInput
from langflow.io import Output
from langflow.schema import Message


class DataToDBComponent(Component):
    display_name = "Export DB"
    description = "Load data to Bohr database"
    icon = "database"
    name = "DataToDB"
    legacy = False

    inputs = [
        StrInput(
            name="access_key",
            display_name="AccessKey",
            info="Provide AccessKey"
        ),
        StrInput(
            name="table_id",
            display_name="Table ID",
            info="Provide Table ID"
        ),
        DataInput(
            name="data_for_db",
            display_name="Import Data",
            info="Provide the data"
        ),
        StrInput(
            name="key_of_data",
            display_name="Data Key"
        )
    ]

    outputs = [
        Output(name="load_status", display_name="Load Status", method="load_data_to_db"),
    ]

    def load_data_to_db(self) -> Message:
        AccessKey = self.access_key
        table_ak = self.table_id
        AppKey = ""
        BaseUrl = "https://openapi.dp.tech"

        database_client = SQLClient(access_key=AccessKey, app_key=AppKey, openapi_addr=BaseUrl)
        database_client.table_with_ak(table_ak).Insert(self.data_for_db.data[self.key_of_data])

        return Message(text="Success load data to db")
