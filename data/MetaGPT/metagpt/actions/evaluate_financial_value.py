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

Role: Your role is to evaluate the financial value of a proposed idea brings to a product for a company, using both the given context and your own knowledge base.
Requirements: Evaluate the change in financial value of all the ideas in the context with as much critical thought as possible. For each idea, you have to answer four questions; return a single sentence justification and a score on the scale of 1-9 (where 1 represents a negative impact, 5 no change, and 9 is a positive impact): 
    1) SALES VOLUME: What is the impact of the idea on the expected sales volume of the product?
    2) RATE OF RETURN: How does the idea affect the rate of return on investment?
    3) PAYBACK TIME: How does the idea affect the payback time?
    5) AVERAGE SCORE: Summarize the previous justifications in one sentence, and return the mean average of the scores for each idea.

Make sure reasoning is insightfull. Don't say further research may be necessary, act with assurance and make assumptions. Rely on your knowledge as much as possible. Don't be scared to be critical.

Fill in the following missing information. Each section name is a key in the JSON. If the requirements are unclear, ensure minimum viability and avoid excessive design. Limit the response to 1500 tokens.

## Project name: Repeat the project name from the context exactly. Do not change anything or add any characters.
## Financial value: Provided as a Python List[Dict[str, List[str]]], where each element corresponds to each product. Each element should be a dictionary, where each question subject is a key and the corresponding value is a list. The list should contain the justification and the score out of 9 (as a string value) for the corresponding question.

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
    "Financial value": [
        {
            "Idea name": ["Idea 1 name", "0"],
            "SALES VOLUME": ["sales volume justification for idea 1", ""],
            "RATE OF RETURN": ["rate of return justification for idea 1", ""],
            "PAYBACK TIME": ["payback time justification for idea 1", ""],
            "AVERAGE SCORE": ["average score explanation for idea 1", ""]
        },
        {
            "Idea name": ["Idea 2 name", "0"],
            "SALES VOLUME": ["sales volume justification for idea 2", ""],
            "RATE OF RETURN": ["rate of return justification for idea 2", ""],
            "PAYBACK TIME": ["payback time justification for idea 2", ""],
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
    "Financial value": (List[Dict[str, List[str]]], ...),
}

class EvaluateFinancialValue(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, financial_value):
        ws_name = financial_value.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        list_of_financial_value = financial_value.instruct_content.dict()["Financial value"]
        for financial_value in list_of_financial_value:
            solution_file = ideas_path / (financial_value['Idea name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\nSALES VOLUME:\n    Reasoning: " + financial_value['SALES VOLUME'][0] + "\n    Score: " + str(financial_value['SALES VOLUME'][1]) + "\nRATE OF RETURN:\n    Reasoning: " + financial_value['RATE OF RETURN'][0] + "\n    Score: " + str(financial_value['RATE OF RETURN'][1]) + "\nPAYBACK TIME:\n    Reasoning: " + financial_value['PAYBACK TIME'][0] + "\n    Score: " + str(financial_value['PAYBACK TIME'][1]) + "\nAVERAGE SCORE:\n    Reasoning: " + financial_value['AVERAGE SCORE'][0] + "\n    Score: " + str(financial_value['AVERAGE SCORE'][1]))

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        financial_values = await self._aask_v1(prompt, "financial_values", OUTPUT_MAPPING, format=format)
        self._save(financial_values)
        return financial_values
    
   
