from metagpt.actions import BossRequirement, CreatePersonas, CreateJourneyMaps
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.config import CONFIG

class UserResearcher(Role):

    def __init__(
        self,
        name: str = "User Researcher",
        profile: str = "Diverging Learner",
        goal: str = "Imagine real people who would encounter use a given category of product",
        constraints: str = "You are a Diverging Learner. Use your knowledge base to create as detailed and realistic personas as possible",
    ) -> None:
        super().__init__(name, profile, goal, constraints)
        #Initialise associated actions
        self._init_actions([CreatePersonas,CreateJourneyMaps])
        #React to human input if not evaluating human ideas
        if CONFIG.human_ideas == False:
            self._watch({BossRequirement})
        self._set_react_mode("by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        #Get the needed context for the action
        background = self.get_memories()[0].instruct_content.dict()
        if self.get_memories()[-1].cause_by == CreatePersonas:
            needed_context = str("Product: \n" + background["Product"] + "\n\nPersonas: \n" + (self.get_memories()[-1]).content)
        else:
            needed_context = (self._rc.important_memory)
        #Run the action
        response = (await self._rc.todo.run(needed_context))
        logger.info(response)
        #Publish response to environment
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response.content, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg