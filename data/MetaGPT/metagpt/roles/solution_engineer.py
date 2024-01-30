
from metagpt.actions import CreateNeeds, CreateSolutions
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message




class SolutionEngineer(Role):


    def __init__(
        self,
        name: str = "Bobylonian",
        profile: str = "Solution Engineer",
        goal: str = "Come up with product solutions to a pain point, considering the project background provided",
        constraints: str = "Be as realistic and detailed as possible. Only suggest products that can be created with currently existing or soon to be exisiting technologies"
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([CreateSolutions])

        # Set events or actions the Architect should watch or be aware of
        self._watch({CreateNeeds})

    async def _act(self) -> Message:
        # prompt = self.get_prefix()
        # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
        #                                history=self.history)

        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].content
        response = background + "\n" + (await self._rc.todo.run(self._rc.important_memory)).content
        # logger.info(response)
        msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        logger.debug(f"{response}")

        return msg