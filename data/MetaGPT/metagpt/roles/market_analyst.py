
from metagpt.actions import BossRequirement, CreateSolutions, AnalyseMarketViability
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class MarketAnalyst(Role):


    def __init__(
        self,
        name: str = "Bobylonathanson",
        profile: str = "Market Analyst",
        goal: str = "Given a product idea and the context of a company, decide if the idea will perform well in a market",
        constraints: str = "If you have independent knowledge of the company, incorporate it. If not, only use the context provided"
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([AnalyseMarketViability])

        # Set events or actions the Architect should watch or be aware of
        self._watch([])

    async def _act(self) -> Message:
        # prompt = self.get_prefix()
        # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
        #                                history=self.history)

        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        context = self.get_memories()
        print("CONTEXT: " + str(context))
        if context[0].cause_by == AnalyseMarketViability:  
            needed_context = context[1].content + context[-1].content
            print("NEEDED CONTEXT: " + str(needed_context))
        else:
            needed_context = context[0].content + context[-1].content
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
        