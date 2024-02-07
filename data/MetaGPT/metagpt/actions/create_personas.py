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
## Original Issue
{issue}

## Format example
{format_example}

Role: Your role is to create 5 customer personas that would interact with a given product type that is made by a given company.
Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible

##Project name: Come up with a project name, the name should be a sequence of words connected by only underscores instead of spaces, based off the original issue
##Personas: Provided as Python List[Dict[str,str]], the parameters are persona name, persona decription, respectively. The persona name should only include alphabetical characters and spaces. The name used should be a real name and consistent throughout. Don't add any new keys to the dictionary.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name"
    "Personas": [{"Name":"Persona1 name", "Age:Persona1 age","Demographic":"Persona1 Demographic", "Biography":"Persona1 biography","Goals":"Persona1 goals","Fustrations","Persona1 fustrations"},
                {"Name":"Persona2 name", "Age:Persona2 age","Demographic":"Persona2 Demographic", "Biography":"Persona2 biography","Goals":"Persona2 goals","Fustrations","Persona2 fustrations"}],
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
    "Personas": (List[Dict[str,str]], ...),
}


class CreatePersonas(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def recreate_workspace(self, workspace: Path):
        try:
            shutil.rmtree(workspace)
        except FileNotFoundError:
            pass  # Folder does not exist, but we don't care
        workspace.mkdir(parents=True, exist_ok=True)


    def _save(self, personas):
        ws_name = personas.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        workspace.mkdir(parents=True, exist_ok=True)
        self.recreate_workspace(workspace)
        personas_path = workspace / "personas"
        personas_path.mkdir(parents=True, exist_ok=True)
        list_of_personas = personas.instruct_content.dict()["Personas"]
        for persona in list_of_personas:
            persona_file = personas_path / (persona['Name'].lower().replace(' ','_') + ".txt")
            s = ""
            for k,v in persona.items():
                s += k + ": " + v + "\n\n"
            persona_file.write_text(s)
 

    async def run(self, issue, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(issue=issue, format_example=format_example)
        logger.debug(prompt)
        personas = await self._aask_v1(prompt, "personas", OUTPUT_MAPPING, format=format)
        self._save(personas)
        return personas
