
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

Role: Your role is to evaluate the customer value of a proposed idea brings to a product for a company, using both the given context and your own knowledge base.
Requirements: Evaluate the change in customer value of all the ideas in the context with as much critical thought as possible. For each idea, you have to answer five questions; return a single sentence justification and a score on the scale of 1-9 (where 1 represents a low value, 5 represents a moderate value, and 9 represents a high value): 
    1) NECESSITY: How users will evaluate the necessity of products based on the idea?
    2) NOVELTY: How will users evaluate the novelty the idea introduced?
    3) USEFULNESS: How will users evaluate the usefulness the idea brought to the product?
    4) USABILITY: How will users evaluate the usability of the product?
    5) AVERAGE SCORE: Summarize the previous justifications in one sentence, and return the mean average of the scores for each idea.


Make sure reasoning is insightful. Don't say further research may be necessary, act with assurance and make assumptions. Rely on your knowledge as much as possible. Don't be scared to be critical.

Fill in the following missing information. Each section name is a key in the JSON. If the requirements are unclear, ensure minimum viability and avoid excessive design. Limit the response to 1500 tokens.

## Project name: Repeat the project name from the context exactly. Do not change anything or add any characters.
## Customer value: Provided as a Python List[Dict[str, List[str]]], where each element corresponds to each product. Each element should be a dictionary, where each question subject is a key and the corresponding value is a list. The list should contain the justification and the score out of 9 (as a string value) for the corresponding question.

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
    "Customer value": [
        {
            "Idea name": ["Idea 1 name", "0"],
            "NECESSITY": ["necessity justification for idea 1", ""],
            "NOVELTY": ["novelty justification for idea 1", ""],
            "USEFULNESS": ["usefulness justification for idea 1", ""],
            "USABILITY": ["usability justification for idea 1", ""],
            "AVERAGE SCORE": ["average score explanation for idea 1", ""]
        },
        {
            "Idea name": ["Idea 2 name", "0"],
            "NECESSITY": ["necessity justification for idea 2", ""],
            "NOVELTY": ["novelty justification for idea 2", ""],
            "USEFULNESS": ["usefulness justification for idea 2", ""],
            "USABILITY": ["usability justification for idea 2", ""],
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
    "Customer value": (List[Dict[str, List[str]]], ...),
}

class EvaluateCustomerValue(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, customer_value):
        ws_name = customer_value.instruct_content.dict()["Project name"]
        workspace = WORKSPACE_ROOT / ws_name
        ideas_path = workspace / "ideas"
        list_of_customer_value = customer_value.instruct_content.dict()["Customer value"]
        for customer_value in list_of_customer_value:
            solution_file = ideas_path / (customer_value['Idea name'][0].lower().replace(' ','_') + ".txt")
            with open(solution_file,"a") as file:
                file.write("\nNECESSITY:\n    Reasoning: " + customer_value['NECESSITY'][0] + "\n    Score: " + str(customer_value['NECESSITY'][1]) + "\nNOVELTY:\n    Reasoning: " + customer_value['NOVELTY'][0] + "\n    Score: " + str(customer_value['NOVELTY'][1]) + "\nUSEFULNESS:\n    Reasoning: " + customer_value['USEFULNESS'][0] + "\n    Score: " + str(customer_value['USEFULNESS'][1]) + "\nUSABILITY:\n    Reasoning: " + customer_value['USABILITY'][0] + "\n    Score: " + str(customer_value['USABILITY'][1]) + "\nAVERAGE SCORE:\n    Reasoning: " + customer_value['AVERAGE SCORE'][0] + "\n    Score: " + str(customer_value['AVERAGE SCORE'][1]))

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        customer_values = await self._aask_v1(prompt, "customer_values", OUTPUT_MAPPING, format=format)
        self._save(customer_values)
        return customer_values
    
    
