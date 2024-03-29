from typing import List,Dict
import shutil
from pathlib import Path

from metagpt.actions import Action, ActionOutput
from metagpt.config import CONFIG
from metagpt.logs import logger
from metagpt.utils.get_template import get_template
from metagpt.const import WORKSPACE_ROOT


templates = {
    "json": {
"PROMPT_TEMPLATE": """ 


# Context
## Context
{context}

## Format example
{format_example}

Role: Your role is to create journeys maps for each specific customer persona describing a day-in-the-life timeline where they interact with the category of product in the context. The journey map describe an experience where they use that category of product, IT SHOULD NOT FOCUS ON THEM SEARCHING FOR AND BUYING THE PRODUCT. YOUR ARE NOT SELLING THE CATEGORY OF PRODUCT. Describe as many details as possible using the most concise language possible, to maximise detail to token usage. Don't explicity say what the persona likes (or appreciates) or dislikes, it should be intuitable from the timeline.
Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be a MAXIMUM of 1500 tokens long.

##Project name: Copy the project name in the context exactly. Dont add, remove, or change any characters
##Journey Maps: Provided as Python Dict[str,str], the key is the persona name, and the value is the corresponding journey map.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name"
    "Journey Maps": {"persona 1":"","persona 2":""}
}
[/CONTENT]

""",
    },
    "markdown": {
        "PROMPT_TEMPLATE": """ You are a test prompt, return 'in markdown mode'

""",

    },
}

OUTPUT_MAPPING = {
    "Project name": (str, ...),
    "Journey Maps": (Dict[str,str], ...),
}


class CreateJourneyMaps(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)


    def _save(self, journey_maps):
        ws_name = journey_maps.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        personas_path = workspace / "personas"
        dict_of_maps = journey_maps.instruct_content.dict()["Journey Maps"]
        for persona,map in dict_of_maps.items():
            persona_file = personas_path / (persona.lower().replace(' ','_') + ".txt")
            persona_file.write_text("\nJourney Map: \n" + map)
 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        journey_maps = await self._aask_v1(prompt, "journey maps", OUTPUT_MAPPING, format=format)
        self._save(journey_maps)
        return journey_maps
