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

Role: Your role is to summarise the innovation idea in the context passed to you. The summary should consist of the name of the idea, a description of it, and a justification of why it would work. In the justification, highlight and explain particulary high or low scores from the evaluation process.
Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible. Be as detailed as possible in your responses, and make them as long as possible while staying under the token limit.

##Project name: Copy the project name in the context exactly. Dont add, remove, or change any characters. THIS IS DIFFERENT TO THE IDEA NAME
##Idea name: The name of the idea
##Idea description: A description of the idea
##Idea justification: A justification of why the idea is good why it is an appropriate solution to the original scenario.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name"
    "Idea name": "idea name"
    "Idea description": "idea description"
    "Idea justification": "idea justification"
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
    "Idea name": (str, ...),
    "Idea description": (str, ...),
    "Idea justification": (str, ...),
}


class Summarise(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)


    def _save(self, summary):
        ws_name = summary.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        workspace.mkdir(parents=True, exist_ok=True)
        output_file = workspace / "summary.txt"
        output_file.write_text("\nSummary \n\Idea: " + summary.instruct_content.dict()["Idea name"] + "\n\nIdea Description: " + summary.instruct_content.dict()["Idea description"] + "\n\n Idea Justification: " + summary.instruct_content.dict()["Idea justification"])
 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        summary = await self._aask_v1(prompt, "summary", OUTPUT_MAPPING, format=format)
        self._save(summary)
        return summary
