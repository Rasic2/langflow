import os

import requests

from langflow.custom.custom_component.component import Component
from langflow.inputs import FileInput
from langflow.io import Output
from langflow.schema import Message


class PDFParserComponent(Component):
    display_name = "Literature PDF Parser"
    description = "parse pdf to content"
    icon = "file-text"
    name = "PDFParser"
    legacy = False

    inputs = [
        FileInput(
            name="pdf_file"
        )
    ]

    outputs = [
        Output(name="content", display_name="PDF Content", method="load_pdf_to_content"),
    ]

    def load_pdf_to_content(self) -> Message:
        host = "http://101.126.82.63:40001"
        parser_api = f"{host}/trigger-file-async"
        result_api = f"{host}/get-result"

        file_path = self.pdf_file
        files = {
            'file': open(file_path, 'rb')
        }
        parser_data = {
            'token': os.path.basename(file_path)[:15],  # 需满足正则校验，r'^[-\._?=&a-zA-Z0-9]{1,128}$'
        }

        semantic_cfg = {
            'textual': 3,  # 兼容False，True设置，等价于Disable = 0， OCRFast = 1
            'chart': 1,
            "table": True,
            "molecule": True,
            "equation": True,
            "figure": False,
            "expression": True,
        }
        extra_cfg = {}
        parser_data.update(**semantic_cfg)
        parser_data.update(extra_cfg)

        # parse pdf
        parser_response = requests.post(parser_api, files=files, data={'sync': True, **parser_data})

        # get content
        result_response = requests.post(result_api, json={"token": parser_data['token']})
        result_response_content = result_response.json()['content']

        return Message(text=result_response_content)
