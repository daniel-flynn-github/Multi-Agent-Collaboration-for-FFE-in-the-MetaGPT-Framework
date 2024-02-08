

from typing import List, Dict, Tuple

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

Role: Your role is to evaluate the social value of a proposed idea for a product. Use both the given context and your own knowledge base to assess the impact of the idea on the users. For each idea, you have to answer five questions and provide a single sentence justification and a score on a scale of 1-9 (where 1 represents low value, 5 represents moderate value, and 9 represents high value): 
    1) IMPORTANCE: How much will the idea contribute to the importance of the product for users?
    2) EMPHASIS: How will the idea contribute to highlighting the product by the user?
    3) COMMITMENT: How will the idea contribute to commitment from the users?
    4) AFFORDABILITY: How does the idea contribute to the affordability of the product?
    5) AVERAGE SCORE: Summarize the previous justifications in one sentence, and return the mean average of the scores for each idea.

Ensure your reasoning is insightful and confident. Rely on your knowledge as much as possible and don't be afraid to be critical.

Fill in the following missing information. Each section name is a key in the JSON. If the requirements are unclear, ensure minimum viability and avoid excessive design. Limit the response to 1500 tokens.

## Project name: Repeat the project name from the context exactly. Do not change anything or add any characters.
## Social value: Provided as a Python List[Dict[str, List[str]]], where each element corresponds to each idea. Each element should be a dictionary, where each question subject is a key and the corresponding value is a list. The list should contain the justification and the score out of 9 (as a string value) for the corresponding question.

NOTE:
 - YOU MUST COMPUTE THE AVERAGE SCORE AS THE GEOMETRIC MEAN OF THE OTHER SCORES
 - THE SCORE FOR THE IDEA NAME IS A PLACEHOLDER AND SHOULD ALWAYS BE ZERO
 - THE SCORES AND REASONING MUST BE DIFFERENT FOR EACH IDEA. 
 - THE SCORE MUST ALWAYS BE AN NUMBER. 
 - LIMIT THE JUSTIFICATION TO ONE SENTENCE MAX

Output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like the format example, and only output the JSON inside this tag, nothing else.
""",
        "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name",
    "Social value": [
        {
            "Idea name": ["Idea 1 name", "0"],
            "IMPORTANCE": ["importance justification for idea 1", ""],
            "EMPHASIS": ["emphasis justification for idea 1", ""],
            "COMMITMENT": ["commitment justification for idea 1", ""],
            "AFFORDABILITY": ["affordability justification for idea 1", ""],
            "AVERAGE SCORE": ["average score explanation for idea 1", ""]
        },
        {
            "Idea name": ["Idea 2 name", "0"],
            "IMPORTANCE": ["importance justification for idea 2", ""],
            "EMPHASIS": ["emphasis justification for idea 2", ""],
            "COMMITMENT": ["commitment justification for idea 2", ""],
            "AFFORDABILITY": ["affordability justification for idea 2", ""],
            "AVERAGE SCORE": ["average score explanation for idea 2", ""]
        }
    ]
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
    "Social value": (List[Dict[str, List[str]]], ...),
}

class EvaluateSocialValue(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, social_value):
        ws_name = social_value.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        list_of_social_value = social_value.instruct_content.dict()["Social value"]
        for social_value in list_of_social_value:
            solution_file = ideas_path / (social_value['Idea name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\nIMPORTANCE:\n    Reasoning: " + social_value['IMPORTANCE'][0] + "\n    Score: " + str(social_value['IMPORTANCE'][1]) + "\nEMPHASIS:\n    Reasoning: " + social_value['EMPHASIS'][0] + "\n    Score: " + str(social_value['EMPHASIS'][1]) + "\nCOMMITMENT:\n    Reasoning: " + social_value['COMMITMENT'][0] + "\n    Score: " + str(social_value['COMMITMENT'][1]) + "\nAFFORDABILITY:\n    Reasoning: " + social_value['AFFORDABILITY'][0] + "\n    Score: " + str(social_value['AFFORDABILITY'][1]) + "\nAVERAGE SCORE:\n    Reasoning: " + social_value['AVERAGE SCORE'][0] + "\n    Score: " + str(social_value['AVERAGE SCORE'][1]))

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        social_values = await self._aask_v1(prompt, "social_values", OUTPUT_MAPPING, format=format)
        self._save(social_values)
        return social_values
 