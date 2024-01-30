
from metagpt.actions import CreateSolutions, AnalyseFeasibility, AnalyseMarketViability, 
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message



class Demonstrator(Role):


    def __init__(
        self,
        name: str = "Bobylonathan",
        profile: str = "Demonstrator",
        goal: str = "Return a report summarising a product idea",
        constraints: str = ""
    ) -> None:
        super().__init__(name, profile, goal, constraints)


        # Initialize actions specific to the Architect role
        self._init_actions([AnalyseFeasibility])

        # Set events or actions the Architect should watch or be aware of
        self._watch([AnalyseFeasibility])

    
    async def _act(self) -> Message:
            # prompt = self.get_prefix()
            # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
            #                                history=self.history)

            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            if context[0].cause_by == AnalyseFeasibility:  
                needed_context = context[0].content + context[-2].content
            else:
                needed_context = context[-1].content
            response = await self._rc.todo.run(needed_context)
            # logger.info(response)
            if isinstance(response, ActionOutput):
                msg = Message(content=response.content, instruct_content=response.instruct_content,
                            role=self.profile, cause_by=type(self._rc.todo))
            else:
                msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
            self._rc.memory.add(msg)
            # logger.debug(f"{response}")

            return msg