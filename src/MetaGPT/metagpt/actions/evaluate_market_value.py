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

Role: Your role is to evaluate the market value a proposed innovation idea brings to a category of products for a company, using both the given context and your own knowledge base.
Requirements: Evaluate the change in market value of all the ideas in the context with as much critical thought as possible. For each idea, you have to answer seven questions; return a two sentence justification and a score on the scale of 1-9 (where 1 represents a loss in value, 5 no change in value, and 9 is a positive change in value). Compare the idea to similar products to reason your justifications: 
    1) COMPETITION: How competitive will products using the idea be in relation competitor's product?
    2) BUYER: How will products using the idea meet customer expectations?
    3) MARKET: How will products using the idea meet the expectations of the market?
    4) AVERAGE SCORE: Summarize the previous justifications in one sentence and return the mean average of the scores.

Make sure reasoning is insightfull. Don't say further research may be necessary, act with assurance and make assumptions. Rely on your knowledge as much as possible. Don't be scared to be critical.

Fill in the following missing information. Each section name is a key in the JSON. If the requirements are unclear, ensure minimum viability and avoid excessive design. Limit the response to 1500 tokens.

## Project name: Repeat the project name from the context exactly. Do not change anything or add any characters.
## Values: Provided as a Python List[Dict[str, List[str]]], where each element corresponds to each product. Each element should be a dictionary, where each question subject is a key and the corresponding value is a list. The list should contain the justification and the score out of 9 (as a string value) for the corresponding question.

NOTE:
 - YOU MUST COMPUTE THE AVERAGE SCORE AS THE GEOMETRIC MEAN OF THE OTHER SCORES
 - YOU MUST ENTER THE COMPUTED SCORE AS THE SECOND ELEMENT OF THE LIST FOR AVERAGE SCORE
 - THE SCORE FOR THE IDEA NAME IS A PLACEHOLDER AND SHOULD ALWAYS BE ZERO
 - THE SCORES AND REASONING MUST BE DIFFERENT FOR EACH IDEA. 
 - THE SCORE MUST ALWAYS BE AN NUMBER. 

Output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like the format example, and only output the JSON inside this tag, nothing else.
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    "Project name": "project_name",
    "Values": [
        {
            "Idea name": ["Idea 1 name", "0"],
            "COMPETITION": ["competition justification for idea 1", ""],
            "BUYER": ["buyer justification for idea 1", ""],
            "MARKET": ["market justification for idea 1", ""],
            "AVERAGE SCORE": ["average score explanation for idea 1", ""]
        },
        {
            "Idea name": ["Idea 2 name", "0"],
            "COMPETITION": ["competition justification for idea 2", ""],
            "BUYER": ["buyer justification for idea 2", ""],
            "MARKET": ["market justification for idea 2", ""],
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
    "Values": (List[Dict[str, List[str]]], ...),
}

class EvaluateMarketValue(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, market_value):
        ws_name = market_value.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        list_of_market_value = market_value.instruct_content.dict()["Values"]
        for market_value in list_of_market_value:
            solution_file = ideas_path / (market_value['Idea name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\n\nMARKET VALUE:\n\n\tCompetition:\n\t\tScore: " + str(market_value['COMPETITION'][1]) + "\n\t\tReasoning: " + market_value['COMPETITION'][0] + "\n\tBuyer:\n\t\tScore: " + str(market_value['BUYER'][1]) + "\n\t\tReasoning: " + market_value['BUYER'][0] + "\n\tMarket:\n\t\tScore: " + str(market_value['MARKET'][1]) + "\n\t\tReasoning: " + market_value['MARKET'][0] + "\n\tAverage Score:\n\t\tScore: " + str(market_value['AVERAGE SCORE'][1]) + "\n\t\tReasoning: " + market_value['AVERAGE SCORE'][0] + "\n\nSummary: " + market_value['AVERAGE SCORE'][0] + "\n\tAverage Score: " + str(market_value['AVERAGE SCORE'][1]) + "\n")



    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        market_values = await self._aask_v1(prompt, "market_values", OUTPUT_MAPPING, format=format)
        self._save(market_values)
        return market_values
    
    
