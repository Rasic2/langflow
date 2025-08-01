from typing import cast

from langchain_google_vertexai._utils import replace_defs_in_schema
from langchain_google_vertexai.functions_utils import _format_json_schema_to_gapic

from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.inputs.inputs import MessageTextInput, CodeInput
from langflow.io import BoolInput, FileInput, FloatInput, IntInput, StrInput


class ChatVertexAIComponent(LCModelComponent):
    display_name = "Vertex AI"
    description = "Generate text using Vertex AI LLMs."
    icon = "VertexAI"
    name = "VertexAiModel"

    inputs = [
        *LCModelComponent._base_inputs,
        FileInput(
            name="credentials",
            display_name="Credentials",
            info="JSON credentials file. Leave empty to fallback to environment variables",
            file_types=["json"],
        ),
        MessageTextInput(name="model_name", display_name="Model Name", value="gemini-1.5-pro"),
        StrInput(name="project", display_name="Project", info="The project ID.", advanced=True),
        StrInput(name="location", display_name="Location", value="us-central1", advanced=True),
        StrInput(name="response_mime_type", display_name="Response Mime Type", value="application/json", advanced=True),
        StrInput(name="response_schema_class", display_name="Response Schema Class", advanced=True),
        CodeInput(name="response_schema", display_name="Response Schema", info="The Python code to execute.",
                  advanced=True),
        IntInput(name="max_output_tokens", display_name="Max Output Tokens", advanced=True),
        IntInput(name="max_retries", display_name="Max Retries", value=1, advanced=True),
        FloatInput(name="temperature", value=0.0, display_name="Temperature"),
        IntInput(name="top_k", display_name="Top K", advanced=True),
        FloatInput(name="top_p", display_name="Top P", value=0.95, advanced=True),
        BoolInput(name="verbose", display_name="Verbose", value=False, advanced=True),
    ]

    def build_model(self) -> LanguageModel:
        try:
            from langchain_google_vertexai import ChatVertexAI
        except ImportError as e:
            msg = "Please install the langchain-google-vertexai package to use the VertexAIEmbeddings component."
            raise ImportError(msg) from e
        location = self.location or None
        if self.credentials:
            from google.cloud import aiplatform
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(self.credentials)
            project = self.project or credentials.project_id
            # ChatVertexAI sometimes skip manual credentials initialization
            aiplatform.init(
                project=project,
                location=location,
                credentials=credentials,
            )
        else:
            project = self.project or None
            credentials = None

        response_schema = None
        if self.response_schema:
            # 动态执行代码（生产环境需严格检查输入！）
            namespace = {}
            exec(self.response_schema, namespace)
            response_schema = namespace[self.response_schema_class].model_json_schema()
            response_schema = replace_defs_in_schema(response_schema)
            response_schema = _format_json_schema_to_gapic(response_schema)

        return cast(
            "LanguageModel",
            ChatVertexAI(
                response_mime_type=self.response_mime_type,
                response_schema=response_schema,
                credentials=credentials,
                location=location,
                project=project,
                max_output_tokens=self.max_output_tokens or None,
                max_retries=self.max_retries,
                model_name=self.model_name,
                temperature=self.temperature,
                top_k=self.top_k or None,
                top_p=self.top_p,
                verbose=self.verbose,
            ),
        )
