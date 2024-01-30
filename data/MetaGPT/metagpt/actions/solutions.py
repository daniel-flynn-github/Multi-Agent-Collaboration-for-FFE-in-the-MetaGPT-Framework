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

Role: Your role is to use your knowledge to generate eight potential product solutions to a pain point. Remember to consider the project background provided and only generate ideas that are suitable. The solutions MUST address the pain point, and the descriptions must be explicit in how they address the pain point.
Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters.
##Solutions: Provided as Python List[Dict[str,str]], each element in the list should be a product solution represented as a dictionary. The dictionary should contain the name of the product and a description of the product. The product name should only include alphabetical characters and spaces. Create 5 products.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name"
    "Solutions": [{"Product name":"", "Description":""},
                  {"Product name":"", "Description":""}]
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
    "Solutions": (List[Dict[str,str]], ...),
}


class CreateSolutions(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, solutions):
        ws_name = solutions.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        product_path = workspace / "product"
        product_path.mkdir(parents=True, exist_ok=True)
        list_of_solutions = solutions.instruct_content.dict()["Solutions"]
        solutions_path = product_path / "product_ideas"
        solutions_path.mkdir(parents=True, exist_ok=True)
        for solution in list_of_solutions:
            solution_file = solutions_path / (solution['Product name'].lower().replace(' ','_') + ".txt")
            solution_file.write_text("Product: " + solution["Product name"] + "\nProduct Description: " + solution["Description"])
 

    async def run(self, issue, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(issue=issue, format_example=format_example)
        logger.debug(prompt)
        solutions = await self._aask_v1(prompt, "solutions", OUTPUT_MAPPING, format=format)
        self._save(solutions)
        return solutions
