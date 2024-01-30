
from metagpt.actions import CreateSolutions, AnalyseFeasibility, AnalyseMarketViability, BossRequirement
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message



class FeasibilityAnalyst(Role):


    def __init__(
        self,
        name: str = "Bobylonathan",
        profile: str = "Feasibility Analyst",
        goal: str = "Given a product idea and the context of a company, decide if the idea is viable",
        constraints: str = "If you have independent knowledge of the company or the field it is part of, incorporate it. If not, only use the context provided. Make assumptions and be bold with your responses."
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        self._set_react_mode("by_order")


        # Initialize actions specific to the Architect role
        self._init_actions([AnalyseFeasibility, AnalyseMarketViability])

        # Set events or actions the Architect should watch or be aware of
        self._watch([CreateSolutions])

    
    async def _act(self) -> Message:
            # prompt = self.get_prefix()
            # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
            #                                history=self.history)

            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            if context[0].cause_by == AnalyseFeasibility:  
                needed_context = context[0].content + context[-2].content
                print("NEEDED CONTEXT: " + str(needed_context))
            else:
                needed_context = context[-1].content
                print("NEEDED CONTEXT: " + str(needed_context))
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