from typing import List,Dict,Tuple
import shutil
import numpy as np
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

Role: Your role is to to analyse a collection of journey maps detailing different personas experience with a category of products, and identify design principles a products in that category should adhere to. In addition to the journey maps, identify design principles from the companies profile, mission, and existing product range as provided in the context. Generate 10 design principles in total.
Requirements: According to the context and using the journey maps within it, fill in the following missing information, each section name is a key. If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be a MAXIMUM of 1500 tokens long.

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Principle 1: Provided as Python str, the value is the principle
##Principle 2: Provided as Python str, the value is the principle
##Principle 3: Provided as Python str, the value is the principle
##Principle 4: Provided as Python str, the value is the principle
##Principle 5: Provided as Python str, the value is the principle
##Principle 6: Provided as Python str, the value is the principle
##Principle 7: Provided as Python str, the value is the principle
##Principle 8: Provided as Python str, the value is the principle
##Principle 9: Provided as Python str, the value is the principle
##Principle 10: Provided as Python str, the value is the principle


output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Principle 1": ""
    ""Principle 2": ""
    ""Principle 3": ""
    ""Principle 4": ""
    ""Principle 5": ""
    ""Principle 6": ""
    ""Principle 7": ""
    ""Principle 8": ""
    ""Principle 9": ""
    ""Principle 10": ""
    
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
    "Principle 1": (str, ...),
    "Principle 2": (str, ...),
    "Principle 3": (str, ...),
    "Principle 4": (str, ...),
    "Principle 5": (str, ...),
    "Principle 6": (str, ...),
    "Principle 7": (str, ...),
    "Principle 8": (str, ...),
    "Principle 9": (str, ...),
    "Principle 10": (str, ...),


}

class CreateDesignPrinciples(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)
        



    def _save(self, needs):
        ws_name = (needs.instruct_content.dict()["Project name"]).lower().replace(" ","_")
        workspace = WORKSPACE_ROOT / ws_name
        imperative_path = workspace / "imperatives"
        instruct_dict = needs.instruct_content.dict()
        principle_file = imperative_path / "design_principles.txt"
        for name, principle in list(instruct_dict.items()):
            principle_file.write_text(name + ": " + principle + "\n")
        

 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        design_principles = await self._aask_v1(prompt, "design_principles", OUTPUT_MAPPING, format=format)
        self._save(design_principles)
        return design_principles
