

from metagpt.actions import CreatePersonas,CreateJourneyMaps
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class ExperienceAnalyst(Role):

    def __init__(
        self,
        name: str = "Bob",
        profile: str = "Experience Analyst",
        goal: str = "You work for on a design team for the company given in the context, your role is to analyse customer personas and create journey maps of how they would experience a given product type",
        constraints: str = "",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([CreateJourneyMaps])

        # Set events or actions the Architect should watch or be aware of
        self._watch({CreatePersonas})

    async def _act(self) -> Message:
        # prompt = self.get_prefix()
        # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
        #                                history=self.history)

        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].instruct_content.dict()
        logger.info("JOURNEY MAP BACKGROUND: " + str("Product topic: \n" + background["Topic"] + "\n\nPersonas: \n" + (self._rc.important_memory[0]).content))
        response = (await self._rc.todo.run("Product topic: \n" + background["Topic"] + "\n\nPersonas: \n" + (self._rc.important_memory[0]).content))
        # logger.info(response)
        print("HERE")
        msg = Message(content=response.content, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        logger.debug(f"{response}")

        return msg
        

