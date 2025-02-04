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

Role: Your role is to evaluate the technical value a proposed idea brings to a category of products for a company, using both the context you are given and any context you know from your own knowledge base.
Requirements: Evaluate the change in technical value of all the ideas in the context with as much critical thought as possible. For each idea, you have to answer seven questions; return a two sentence justification and a score on the scale of 1-9 (where 1 represents a loss in value, 5 no change in value, and 9 is a positive change in value). Compare the idea to similar products to reason your justifications: 
    1) PRODUCTIVITY: How the idea affects the possibility to production? 
    2) FUNCTIONALITY: How the idea affects the functionality compared to existing products? 
    3) RELIABILITY: How the idea affects the reliability compared to existing products? 
    4) SAFETY: How the idea affects the safety compared to existing products? 
    5) ECOLOGICALLY: Does the idea affect the environment?
    6) AESTHETICS: Does the idea affect the aesthetics compared to existing products?
    5) AVERAGE SCORE: Summarize the previous justifications in one sentence, and return the mean average of the scores for each idea.

Make sure reasoning is insightfull. Don't say further research may be necessary, act with assurance and make assumptions. Rely on your knowledge as much as possible. Don't be scared to be critical.

Fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. LIMIT THE RESPONSE TO 1500 tokens

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Values: Provided as Python List[Dict[str,List[str]]], a list where each element corresponds to each product. Each element should contain be a dictionary, where each question subject is a key and the corresponding value is a list. The list should contain first the one justification and then the score out of 9 (a str value) for the corresponding question.

NOTE:
 - YOU MUST COMPUTE THE AVERAGE SCORE AS THE GEOMETRIC MEAN OF THE OTHER SCORES
 - YOU MUST ENTER THE COMPUTED SCORE AS THE SECOND ELEMENT OF THE LIST FOR AVERAGE SCORE
 - THE SCORE FOR THE IDEA NAME IS A PLACEHOLDER AND SHOULD ALWAYS BE ZERO
 - THE SCORES AND REASONING MUST BE DIFFERENT FOR EACH IDEA. 
 - THE SCORE MUST ALWAYS BE AN NUMBER.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Values": [{"Idea name":["Idea 1 name",0], 
                       "PRODUCTIVITY":["productivity justification for idea 1",""],
                       "FUNCTIONALITY":["functionality justification for idea 1",""], 
                       "RELIABILITY":["reliability justification for idea 1",""], 
                       "SAFETY":["safety justification for idea 1",""],
                       "ECOLOGICALLY":["ecologically justification for idea 1",""],
                       "AESTHETICS":["aesthetics justification for idea 1",""],
                       "AVERAGE SCORE": ["average score explanation for idea 1", ""]
                       {"Idea name":["Idea 1 name",0], 
                       "PRODUCTIVITY":["productivity justification for idea 2",""], 
                       "FUNCTIONALITY":["functionality justification for idea 2",""], 
                       "RELIABILITY":["reliability justification for idea 2",""], 
                       "SAFETY":["safety justification for idea 2",""],
                       "ECOLOGICALLY":["ecologically justification for idea 2",""],
                       "AESTHETICS":["aesthetics justification for idea 2",""],
                       "AVERAGE SCORE": ["average score explanation for idea 2", ""]
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
    "Values": (List[Dict[str,List[str]]], ...),
}



class EvaluateTechnicalValue(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, technical_value):
        ws_name = technical_value.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        list_of_technical_value = technical_value.instruct_content.dict()["Values"]
        for technical_value in list_of_technical_value:
            solution_file = ideas_path / (technical_value['Idea name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\n\nTECHNICAL VALUE:\n\n\tProductivity:\n\t\tScore: " + str(technical_value['PRODUCTIVITY'][1]) + "\n\t\tReasoning: " + technical_value['PRODUCTIVITY'][0] + "\n\tFunctionality:\n\t\tScore: " + str(technical_value['FUNCTIONALITY'][1]) + "\n\t\tReasoning: " + technical_value['FUNCTIONALITY'][0] + "\n\tReliability:\n\t\tScore: " + str(technical_value['RELIABILITY'][1]) + "\n\t\tReasoning: " + technical_value['RELIABILITY'][0] + "\n\tSafety:\n\t\tScore: " + str(technical_value['SAFETY'][1]) + "\n\t\tReasoning: " + technical_value['SAFETY'][0] + "\n\tEcologically:\n\t\tScore: " + str(technical_value['ECOLOGICALLY'][1]) + "\n\t\tReasoning: " + technical_value['ECOLOGICALLY'][0] + "\n\tAesthetics:\n\t\tScore: " + str(technical_value['AESTHETICS'][1]) + "\n\t\tReasoning: " + technical_value['AESTHETICS'][0] + "\n\nSummary: " + technical_value['AVERAGE SCORE'][0] + "\n\tAverage Score: " + str(technical_value['AVERAGE SCORE'][1] + "\n"))


    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        technical_values = await self._aask_v1(prompt, "technical_values", OUTPUT_MAPPING, format=format)
        self._save(technical_values)
        return technical_values


