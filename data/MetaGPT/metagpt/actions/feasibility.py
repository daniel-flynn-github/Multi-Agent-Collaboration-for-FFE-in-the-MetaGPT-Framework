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

Role: Your role is to analyse the feasability of a product for a company, using both the context you are given and any context you know from your own knowledge base.
Requirements: Analyse the feasability of all the products in the context with as much critical thought as possible. THE SCORES AND REASONING MUST BE DIFFERENT FOR EACH PRODUCT. For each product, you have to analyse four features; describe how feasible each product is in terms of each feature, and give the feature a score out of 100 (where 100 is most feasible and 0 is least feasable): 1) Research and Development: How feasible is it that the product can be researched and developed given the resources the company would have, the budget for the whole project, and the timeframe for the whole project. 2) Go to Market: How effectively will the company be able to establish the product in the market, given the companies resources, the budget for the project, and the timeframe for the project. 3) Required Partners: Are lots of partners necessary, and if so how feasible is it that the company will be able to work with them given the company, budget, and timeframe. 4) Compatibility: How compatible is the product with the company?. Make sure reasoning is insightfull. Don't say further research may be necessary, act with assurance and make assumptions. Rely on your knowledge as much as possible. Don't be scared to be critical if an idea is bad. Limit the reasoning to two sentences. fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. Limit the reasoning to one sentence.

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Feasibility: Provided as Python List[Dict[str,List[str]]], a list where each element corresponds to each product. Each element should contain be a dictionary, where each feature is a key and the corresponding value is a tuple. The tuple should contain first a string analysis of the feasibility of the product in terms of that feature, and then a score out of 100 (a str value) for that feature. NOTE -> The score for the product name is a placeholder and SHOULD ALWAYS BE ZERO
Partners
output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Feasibility": [{"Product name":["Product1 name",0], 
                       "Research and Development":["Research and development feasibility analysis for product 1",],
                       "Go to Market":["Go to market feasibility analysis for product 1",], 
                       "Required Partners":["Partner feasibility analysis for product 1",], 
                       "Compatibility":["Compatibility feasibility analysis for product 1",],
                       {"Product name":["Product2 name",0], 
                       "Research and Development":["Research and development feasibility analysis for product 2",], 
                       "Go to Market":["Go to market feasibility analysis for product 2",], 
                       "Required Partners":["Partner feasibility analysis for product 2",], 
                       "Compatibility":["Compatibility feasibility analysis for product 2",]}]
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
    "Feasibility": (List[Dict[str,List[str]]], ...),
}


class AnalyseFeasibility(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, feasibilities):
        ws_name = feasibilities.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        product_path = workspace / "product"
        list_of_feasibilities = feasibilities.instruct_content.dict()["Feasibility"]
        solutions_path = product_path / "product_ideas"
        for feasibility in list_of_feasibilities:
            solution_file = solutions_path / (feasibility['Product name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\nFeasibility Analysis: \n  Research and Development:\n         Reasoning: " + feasibility['Research and Development'][0] + "\n      Score: " + str(feasibility['Research and Development'][1]) + "\n  Go to Market:\n         Reasoning: " + feasibility['Go to Market'][0] + "\n      Score: " + str(feasibility['Go to Market'][1]) + "\n  Required Partners:\n         Reasoning: " + feasibility['Required Partners'][0] + "\n      Score: " + str(feasibility['Required Partners'][1]) + "\n  Compatibility with Company:\n         Reasoning: " + feasibility['Compatibility'][0] + "\n      Score: " + str(feasibility['Compatibility'][1]) + "\n")



 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        feasibilities = await self._aask_v1(prompt, "feasibilities", OUTPUT_MAPPING, format=format)
        self._save(feasibilities)
        return feasibilities


