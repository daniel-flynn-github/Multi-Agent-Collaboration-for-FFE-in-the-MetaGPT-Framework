

from metagpt.actions import CreatePersonas,CreateJourneyMaps
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class ExperienceAnalyst(Role):

    def __init__(
        self,
        name: str = "Experience Analyst",
        profile: str = "Converging Learner",
        goal: str = "You work for on a design team for the company given in the context, your role is to analyse customer personas",
        constraints: str = "You are a Converging Learner. Use your existing technical, user, and market knowledge of the real world",
    ) -> None:
        super().__init__(name, profile, goal, constraints)
        
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].instruct_content.dict()
        needed_context = str("Product: \n" + background["Product"] + "\n\nPersonas: \n" + (self._rc.important_memory[0]).content)
        response = (await self._rc.todo.run(needed_context))
        logger.info(response)
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response.content, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg
        

