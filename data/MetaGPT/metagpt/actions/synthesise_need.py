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

Role: Your role in the team is to use your knowledge base to analyse a collection of issues and synthesise three fundamental needs. While a fundamental need does not need at assist with every issue in the collection, it should aim to capture the essence of as many as possible.Try to be analytical and profound, and go into detail. 
Requirements: According to the context and using the needs created within it, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design.

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters.
##Fundamental needs: Provided as a Python List[str]. A fundamental need should be unique and specific, not a vague encapsulating phrase. A fundamental need should also be a singular need, not a list of needs. A need should be a single sentence. Don't try to suggest a product. Make sure a fundamental need isn't an initiative, but rather a problem that needs a solution.
##Reasoning: Explain the reasoning behind each fundamental need, provided as a Python List[str] (where each list element is the reasoning behind a corresponding need)

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": ""
    "Fundamental needs": ["need1", "need2", "need3"]
    "Reasoning": ["need1 reasoning", "need2 reasoning", "need3 reasoning"]
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
    "Fundamental needs": (List[str],...),
    "Reasoning" : (List[str],...),
}


class SynthesiseNeed(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)



    def _save(self, f_need, response):
        ws_name = (f_need.instruct_content.dict()["Project name"]).lower().replace(" ","_")
        workspace = WORKSPACE_ROOT / ws_name
        f_need_path = workspace / "needs"
        f_need_file = f_need_path / "fundamental_need.txt"
        s = "Fundamental need: " + response["fundamental need"] + "\nReasoning: " + response["reasoning"]
        f_need_file.write_text(s)
 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        f_need = await self._aask_v1(prompt, "f_need", OUTPUT_MAPPING, format=format)
        print("Select which fundamental need you would like to focus on:\n")
        for i in range(len(f_need.instruct_content.dict()["Fundamental needs"])):
            print("Fundamental need: " + f_need.instruct_content.dict()["Fundamental needs"][i] + "\nReasoning: " + f_need.instruct_content.dict()["Reasoning"][i])
        choice = input("Enter a number 1, 2 or 3: ")
        while choice.strip() not in ("1","2","3"):
            choice = input("Invalid input. You must enter 1, 2 or 3")
        response = {"project name": f_need.instruct_content.dict()["Project name"],"fundamental need": f_need.instruct_content.dict()["Fundamental needs"][int(choice.strip())-1],"reasoning":f_need.instruct_content.dict()["Reasoning"][int(choice.strip())-1]}
        self._save(f_need,response)
        return str(response)
