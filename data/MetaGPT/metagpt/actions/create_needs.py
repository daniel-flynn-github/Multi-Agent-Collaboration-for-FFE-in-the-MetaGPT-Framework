from typing import List,Dict,Tuple
import shutil
import numpy as np
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

Role: Your role is to analyse product journey maps of individuals and come up with issues they are likely to experience specific to them. Try to keep the pain point to a maximium of four words long. Once you have created each pain point point, rank each pain point on two metrics: impact (how commonly experienced is the pain point?) and difficulty (how hard to fix is it likely to be, factoring in the context of company provided in the context). Each metric should be an integer score out of 100. A high score should mean larger impact, and highly difficult for the two metrics respectively.
Requirements: According to the context and using the already created personas within it, fill in the following missing information, each section name is a key in json ,If the requirements are unclear, ensure minimum viability and avoid excessive design. The response should be as close to 1500 tokens long as possible

##Project name: Repeat the project name from the context exactly. Dont change anything and don't add any characters
##Persona specfic pain points: Provided as Python Dict[str, List[str]], the key is persona name, and the value is alist of persona issues. Create 7 pain points for each persona.
##Ranked pain points: Provided as Python Dict[str,List[int]], the key is the pain point, the value is a list of integers where the first entry is the impact score, and the second entry is the difficulty score.

output a properly formatted JSON, wrapped inside [CONTENT][/CONTENT] like format example,
and only output the json inside this tag, nothing else
""",
    "FORMAT_EXAMPLE": """
[CONTENT]
{
    ""Project name": "project_name"
    ""Persona specific pain points": "{persona name: [persona pain point 1, persona pain point 2]}"
    ""Ranked pain points": "{pain point 1:[8,42], pain point 2:[87,23]}
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
    "Persona specific pain points": (Dict[str, List[str]],...),
    "Ranked pain points": (Dict[str,List[int]],...)
}

class CreateNeeds(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)



    def _save(self, needs, s):
        ws_name = (needs.instruct_content.dict()["Project name"]).lower().replace(" ","_")
        workspace = WORKSPACE_ROOT / ws_name
        needs_path = workspace / "pain points"
        needs_path.mkdir(parents=True, exist_ok=True)
        dict_of_needs = needs.instruct_content.dict()["Persona specific pain points"]
        for persona, pain_points in dict_of_needs.items():
            need_file = needs_path / (persona.lower().replace(' ','_') + ".txt")
            need_file.write_text("\n".join(pain_points))
        ranked_file = needs_path / "ranked.txt"
        ranked_file.write_text(s)
        

 

    async def run(self, context, format=CONFIG.prompt_format, *args, **kwargs) -> ActionOutput:
        prompt_template, format_example = get_template(templates, format)
        prompt = prompt_template.format(context=context, format_example=format_example)
        logger.debug(prompt)
        needs = await self._aask_v1(prompt, "needs", OUTPUT_MAPPING, format=format)
        dict_of_rankings = needs.instruct_content.dict()["Ranked pain points"]
        dtype = [('pain_point', "U1000"), ('impact', np.intc), ('difficulty', np.intc), ('overall', np.single)]
        rankings = np.empty(len(dict_of_rankings), dtype=dtype)
        for i,(pp,scores) in enumerate(dict_of_rankings.items()):
            rankings[i] = (pp, scores[0], scores[1], ((scores[0]-(scores[1]-100))/2))
        rankings = rankings[np.argsort(-rankings['overall'])]
        s = ""
        for x,i in enumerate(rankings):
            s += ("{n}. Pain Point: {p} Impact = {i} Difficulty = {d} Overall = {o} \n").format(n = str(x+1), p = str(i[0]), i = str(i[1]), d = str(i[2]), o = str(np.round(i[3], 4)))
        self._save(needs,s)
        output_string = ("Project name: {p}\nPain point to be addressed: {r}").format(p = needs.instruct_content.dict()["Project name"], r = rankings[0]['pain_point'])
        return output_string
