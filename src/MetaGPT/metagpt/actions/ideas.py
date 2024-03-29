from typing import List,Dict
import shutil
from pathlib import Path

from metagpt.actions import Action, ActionOutput
from metagpt.config import CONFIG
from metagpt.logs import logger
from metagpt.utils.get_template import get_template
from metagpt.const import WORKSPACE_ROOT

def get_manual_template(manual):
    print("MANUAL: " + str(manual))
    if not manual:
        templates = {
            "json": {
        "PROMPT_TEMPLATE": """ 


        # Context
        ## Original Issue
        {issue}

        ## Format example
        {format_example}

        Role: Your role is to use your knowledge to create innovation ideas to address three given pain points. This means the idea MUST be a either new form of or a way to improve (depending on what is most suitable in the scenario) the original product given in the context, NOT an entirely new product or platform. PAY SPECIAL ATTENTION TO THE ORIGINAL PRODUCT AND THE REQUIREMENTS IN THE BRIEF. Come up with two ideas for each pain point. Remember to consider the project background provided and only generate ideas that are suitable. The ideas MUST address a pain point, and the descriptions must be explicit in how they address the pain point. The description must entail at least some of the technical details as to how the idea would be implemented. The idea MUST respect the requirements given in the context, and should use the suggested features to give direction. The idea should follow the design principles outlined in the context. Be as detailed as possible. The ideas MUST be NEW, i.e. they are not already provided by similair products on the market. IMPORTANT: A GOOD WAY TO COME UP WITH NEW IDEAS IS CONSIDERING HOW TECHNOLOGIES OR IDEAS FROM DIFFERENT FIELDS CAN BE APPLIED TO THE PROBLEM.
        Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible.

        ##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters.
        ##Ideas: Provided as Python List[Dict[str,str]], each element in the list should be an idea represented as a dictionary. The dictionary should contain the name of the idea and a description of the idea. The idea name should only include alphabetical characters and spaces. Create 6 ideas.

        output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
        and only output the json inside this tag, nothing else.
        """,
            "FORMAT_EXAMPLE": """
        [CONTENT]
        {
            "Project name": "project_name"
            "Ideas": [{"Idea name":"", "Description":""},
                    {"Idea name":"", "Description":""}]
        }
        [/CONTENT]

        """,
            },
            "markdown": {
                "PROMPT_TEMPLATE": """ You are a test prompt, return 'in markdown mode'

        """,

            },
        }
    else:
        templates = {
            "json": {
        "PROMPT_TEMPLATE": """ 
        # Context
        ## Original Issue
        {issue}

        ## Format example
        {format_example}
        {issue}
        Role: Your role is to repeat back the idea(s) given to you in the context, not adding any of your own input in the slightest. They should be repeated back exactly as they were given to you.
        Requirements: According to the context, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible
        ##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters.
        ##Ideas: Provided as Python List[Dict[str,str]], each element in the list should be an idea represented as a dictionary. The dictionary should contain the name of the idea and the description of the idea.

        output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
        and only output the json inside this tag, nothing else.
        """,
            "FORMAT_EXAMPLE": """
        [CONTENT]
        {
            "Project name": "project_name"
            "Ideas": [{"Idea name":"", "Description":""},
                    {"Idea name":"", "Description":""}]
        }
        [/CONTENT]

        """,
            },
            "markdown": {
                "PROMPT_TEMPLATE": """ You are a test prompt, return 'in markdown mode'

        """,

            },
        }
    return templates
OUTPUT_MAPPING = {
    "Project name": (str, ...),
    "Ideas": (List[Dict[str,str]], ...),
}


class CreateIdeas(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, ideas):
        ws_name = ideas.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        ideas_path.mkdir(parents=True, exist_ok=True)
        list_of_ideas = ideas.instruct_content.dict()["Ideas"]
        for idea in list_of_ideas:
            idea_file = ideas_path / (idea['Idea name'].lower().replace(' ','_') + ".txt")
            idea_file.write_text("Idea: " + idea["Idea name"] + "\nIdea Description: " + idea["Description"])
 

    async def run(self, issue, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        templates = get_manual_template(CONFIG.human_ideas)
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(issue=issue, format_example=format_example)
        logger.debug(prompt)
        ideas = await self._aask_v1(prompt, "ideas", OUTPUT_MAPPING, format=format)
        self._save(ideas)
        return ideas
