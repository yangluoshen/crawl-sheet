import yaml
import os
import importlib
from dotenv import load_dotenv
from dataclasses import dataclass
from smolagents.agents import CodeAgent, populate_template
from smolagents import OpenAIServerModel

load_dotenv()

def create_agent():
    model = SmolCoderModelOpenrouter(
        model_id="openai/gpt-4.1",
        # model_id="openai/gpt-4o-mini",
        # model_id="google/gemini-2.5-flash-preview-05-20",
        # model_id="anthropic/claude-sonnet-4",
    )
    return SmolCodeAgent(model=model, tools=[])

ADDITIONAL_AUTHORIZED_IMPORTS = ["pandas", "numpy", "json", "scipy", "scipy.stats"]

class SmolCodeAgent(CodeAgent):
    def __init__(self, locale: str = "en", *args, **kwargs):
        if "additional_authorized_imports" not in kwargs:
            kwargs["additional_authorized_imports"] = ADDITIONAL_AUTHORIZED_IMPORTS

        prompt_template = yaml.safe_load(
            importlib.resources.files("prompts")  # type: ignore
            .joinpath("smol_code_agent.yaml")
            .read_text()
        )

        self.locale = locale
        super().__init__(prompt_templates=prompt_template, *args, **kwargs)
        # self.logger = SmolagentsLogger()

    def initialize_system_prompt(self) -> str:
        system_prompt = populate_template(
            self.prompt_templates["system_prompt"],
            variables={
                "tools": self.tools,
                "managed_agents": self.managed_agents,
                "locale": self.locale,
                "authorized_imports": (
                    "You can import from any package you want."
                    if "*" in self.authorized_imports
                    else str(self.authorized_imports)
                ),
            },
        )

        return system_prompt


@dataclass
class SmolCoderModel(OpenAIServerModel):
    model_id: str
    api_base: str
    api_key: str

    def __post_init__(self):
        super().__init__(
            model_id=self.model_id, api_base=self.api_base, api_key=self.api_key
        )


@dataclass
class SmolCoderModelOpenrouter(SmolCoderModel):
    api_base: str = os.environ.get("OPENROUTER_ENDPOINT")
    api_key: str = os.environ.get("OPENROUTER_API_KEY")
