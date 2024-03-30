

from metagpt.actions import CreateJourneyMaps,CreatePainPoints, CreateDesignPrinciples
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class Analyst(Role):

    #Role Profile

    def __init__(
        self,
        name: str = "Assimilating Learner",
        profile: str = "Needs Analyst",
        goal: str = "Analyse the provided journey maps",
        constraints: str = "You are an Assimilating Learner. Be insightful to the deeper issue with painpoints and design principles.",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        #Action Selection Logic

        self._set_react_mode("by_order")

        #Initialise associated actions
        self._init_actions([CreatePainPoints,CreateDesignPrinciples])

        #Set Actions to watch for
        self._watch({CreateJourneyMaps})

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].instruct_content.dict()
        #Get the needed context for the action
        if self.get_memories()[-1].cause_by == CreatePainPoints:
            needed_context = str("Company Background: \n" + "Company Profile" + background["Company Profile"] +  "\nCurrent Product Range: " + background["Current Product Range"] + background["Company Mission"] + "\n\nJourney maps: \n" + (self._rc.important_memory[0]).content)
        else:
            needed_context = (self._rc.important_memory[0])
        #Run the action
        response = (await self._rc.todo.run(needed_context))
        logger.info(response)
        #Add the response to memory
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg
    
    #Custom Action Selection Logic to combine output of two Actions
    async def _act_by_order(self) -> Message:
        double_content = ""
        for i in range(len(self._states)):
            self._set_state(i)
            rsp = await self._act()
            double_content += rsp.content + "\n"
        rsp.content = double_content
        logger.info("DOUBLE CONTENT" + rsp.content)
        return rsp
        

