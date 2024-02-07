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

Role: Your role is to summarise the product idea in the context passed to you. The summary should consist of the name of the product, a description of it, and a justification of why it would work
Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible

##Project name: Copy the project name in the context exactly. Dont add, remove, or change any characters. THIS IS DIFFERENT TO THE PRODUCT NAME
##Product name: The name of the product
##Product description: A description of the product
##Product justification: A justification of why the product would work

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name"
    "Product name": "product name"
    "Product description": "product description"
    "Product justification": "product justification"
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
    "Product name": (str, ...),
    "Product description": (str, ...),
    "Product justification": (str, ...),
}


class Summarise(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)


    def _save(self, summary):
        ws_name = summary.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        output_file = workspace / "summary.txt"
        output_file.write_text("\nSummary \n\nProduct: " + summary.instruct_content.dict()["Product name"] + "\n\nDescription: " + summary.instruct_content.dict()["Product description"] + "\n\n Justification: " + summary.instruct_content.dict()["Product justification"])
 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        summary = await self._aask_v1(prompt, "summary", OUTPUT_MAPPING, format=format)
        self._save(summary)
        return summary
