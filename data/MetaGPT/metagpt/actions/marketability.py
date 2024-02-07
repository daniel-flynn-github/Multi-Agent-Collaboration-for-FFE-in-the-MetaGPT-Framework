from typing import List,Dict,Tuple
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

Role: Your role is to analyse how well a product could perform on the market for a company, using both the context you are given and any context you know from your own knowledge base.
Requirements: Analyse the how well the product could perform on the market for all the products in the context with as much critical thought as possible. For each product, you have to analyse four features, describe how feasible they are in terms of each feature, and give the feature a score out of 100 (where 100 is best and 0 is worst): 1) Potential Market Size: How much of the market will the product be able to capture given the resources the company would have, the budget for the whole project, and the timeframe for the whole project, and your knowledge of the market. 2) Potential Attractive Returns: What are the potential returns from creating this product and selling it, and how good are they? 3) Protectable Advantage: What advantages does this product have over similair competing products in the market, and how protectable are they? 4) Likelihood of disruptive impact: Is the product likely to be able to either disrupt pre-existing markets or create a new one? FINALLY FILL IN THE AVERAGE SCORE as the mean average of all the scores (rounded to the nearest two decimal places). Leave the text for average score as it is in the template. fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. LIMIT THE RESPONSE TO 1500 tokens

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Market Viability: Provided as Python List[Dict[str,List[str]]], a list where each element corresponds to each product. Each element should contain be a dictionary, where each feature is a key and the corresponding value is a list. The list should contain first a string analysis of the market viability of the product in terms of that feature, and then a score out of 100 (a str value) for that feature. NOTE -> The score for the product name is a placeholder and SHOULD ALWAYS BE ZERO
THE AVERAGE SCORE LIST SHOULD ONLY CONTAIN A SINGLE ELEMENT THAT IS A NUMBER
THE SCORES AND REASONING MUST BE DIFFERENT FOR EACH PRODUCT. THE SCORE MUST ALWAYS BE AN NUMBER.
LIMIT THE ANALYSIS TO TWO SENTENCES MAX


output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Market Viability": "[{"Product name":["Product1 name",0],
                         "Potential Market Size":["Potential Market Size for product 1",],
                         "Potential Attractive Returns":["Potential Attractive Returns for product 1"], 
                         "Protectable Advantage":["Protectable Advantage for product 1",], 
                         "Likelihood of disruptive impact":["Likelihood of disruptive impact for product 1",],
                         "Average Score": [""]},
                         {"Product name":["Product2 name",0], 
                         "Potential Market Size":["Potential Market Size for product 2",], 
                         "Potential Attractive Returns":["Potential Attractive Returns for product 2",], 
                         "Protectable Advantage":["Protectable Advantage for product 2",], 
                         "Likelihood of disruptive impact":["Likelihood of disruptive impact for product 2",],
                         "Average Score": [""]}]"
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
    "Market Viability": (List[Dict[str,List[str]]], ...),
}


class AnalyseMarketViability(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, market_viabilities):
        ws_name = market_viabilities.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        product_path = workspace / "product"
        list_of_market_viabilities = market_viabilities.instruct_content.dict()["Market Viability"]
        solutions_path = product_path / "product_ideas"
        for market_viability in list_of_market_viabilities:
            solution_file = solutions_path / (market_viability['Product name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\n\n\nMarket Viability Analysis: \n  Potential Market Size:\n         Reasoning: " + market_viability['Potential Market Size'][0] + "\n      Score: " + str(market_viability['Potential Market Size'][1]) + "\n  Potential Attractive Returns:\n         Reasoning: " + market_viability['Potential Attractive Returns'][0] + "\n      Score: " + str(market_viability['Potential Attractive Returns'][1]) + "\n  Protectable Advantage:\n         Reasoning: " + market_viability['Protectable Advantage'][0] + "\n      Score: " + str(market_viability['Protectable Advantage'][1]) + "\n  Likelihood of disruptive impact with Company:\n         Reasoning: " + market_viability['Likelihood of disruptive impact'][0] + "\n      Score: " + str(market_viability['Likelihood of disruptive impact'][1]) + "\n" + "Average score: " + str(market_viability['Average Score'][0]))

 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        market_viabilities = await self._aask_v1(prompt, "market_viabilities", OUTPUT_MAPPING, format=format)
        self._save(market_viabilities)
        return market_viabilities
