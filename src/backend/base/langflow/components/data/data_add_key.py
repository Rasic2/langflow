from langflow.custom.custom_component.component import Component
from langflow.inputs import DataInput, StrInput, MessageInput
from langflow.io import Output
from langflow.schema import Data


class DataAddKeyComponent(Component):
    display_name = "Data Add"
    description = "For Specific Key of Data (list type), add key/value"
    icon = "database"
    name = "DataAddKey"

    inputs = [
        DataInput(
            name="data_for_add",
            display_name="Data",
            info="Provide the data"
        ),
        MessageInput(
            name="key_for_data",
            display_name="Key of Data"
        ),
        StrInput(
            name="key_for_add",
            display_name="New Key"
        ),
        MessageInput(
            name="value_for_add",
            display_name="Value for New Key"
        )
    ]

    outputs = [
        Output(name="output_data", display_name="Updated Data", method="add_key_for_data"),
    ]

    def add_key_for_data(self) -> Data:
        data = {}
        for k, v in self.data_for_add.data.items():
            if k == self.key_for_add:
                new_v = []
                for item in v:
                    item[self.key_for_add] = self.value_for_add
                    new_v.append(item)
                data[k] = new_v
            else:
                data[k] = v

        return Data(data=data)
