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
{context}

## Format example
{format_example}

Role: Your role is to come up with initiatives given a fundamental need. The initiatives should be a 
Requirements: According to the fundamental need in the context and referencing the reasoning for its choice, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Initiatives: Provided as Python List[Dict[str,str]], a list of initiatives represented as a dictionary where the key is the initiative name, and the value is a description of the initiative. Create 5 initiatives. The intiative name should only include alphabetical characters and spaces.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Initiatives": "[{"Initiative name":"Initiative1 name", "Initiative description":"Initiative1 description},{"Initiative name":"Initiative2 name", "Initiative description":"Initiative2 description}]"
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
    "Initiatives": (List[Dict[str,str]], ...),
}


class CreateInitiatives(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, needs):
        ws_name = (needs.instruct_content.dict()["Project name"]).lower().replace(" ","_")
        workspace = WORKSPACE_ROOT / ws_name
        initiatives_path = workspace / "initiatives"
        initiatives_path.mkdir(parents=True, exist_ok=True)
        list_of_initiatives = needs.instruct_content.dict()["Initiatives"]
        for initiative in list_of_initiatives:
            i_path = initiatives_path / initiative["Initiative name"].lower().replace(" ","_")
            i_path.mkdir(parents=True, exist_ok = True)
            initiative_file = i_path / (initiative['Initiative name'].lower().replace(' ','_') + ".txt")
            initiative_file.write_text(initiative['Initiative name'] + "\n" + initiative['Initiative description'])
 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        print("CONTEXT: " + str(context))
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        initiatives = await self._aask_v1(prompt, "initiatives", OUTPUT_MAPPING, format=format)
        return initiatives
