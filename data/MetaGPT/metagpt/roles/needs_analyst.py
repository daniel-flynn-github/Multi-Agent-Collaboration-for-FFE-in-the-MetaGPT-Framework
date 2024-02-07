

from metagpt.actions import CreateJourneyMaps,CreateNeeds
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class NeedsAnalyst(Role):

    def __init__(
        self,
        name: str = "Bob",
        profile: str = "Needs Analyst",
        goal: str = "Given a description of a person generate issues they are likely to encounter",
        constraints: str = "Come up with issues that are not already addressed by products on the market",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([CreateNeeds])

        # Set events or actions the Architect should watch or be aware of
        self._watch({CreateJourneyMaps})

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].instruct_content.dict()
        needed_context = str("Company Background: \n" + "Company Profile" + background["Company Profile"] +  "\nCurrent Product Range: " + background["Current Product Range"] + "\n\nJourney maps: \n" + (self._rc.important_memory[0]).content)
        logger.debug("\n#######################################################\nNEEDS NEEDED CONTEXT: " + needed_context + "\n#######################################################\n")
        response = (await self._rc.todo.run(needed_context))
        #logger.info(response)
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg
        

