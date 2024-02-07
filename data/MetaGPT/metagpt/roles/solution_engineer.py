
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

        self._init_actions([CreateSolutions])

        self._watch({CreateNeeds})

    async def _act(self) -> Message:
        # prompt = self.get_prefix()
        # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
        #                                history=self.history)

        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].content
        needed_context = background + "\n" + (self._rc.important_memory[0]).content
        logger.debug("\n#######################################################\nSOLUTIONS NEEDED CONTEXT: ",needed_context,"\n#######################################################\n") 
        response = (await self._rc.todo.run(needed_context))
        # logger.info(response)
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg