
from metagpt.actions import AnalyseMarketViability, CreateSolutions, Summarise
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
        self._init_actions([Summarise])

        # Set events or actions the Architect should watch or be aware of
        self._watch([AnalyseMarketViability])

    
    async def _act(self) -> Message:
            # prompt = self.get_prefix()
            # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
            #                                history=self.history)

            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            needed_context = ""
            best_product_string = context[-1].content
            lines = best_product_string.split("\n")
            best_product = lines[0].replace("The best product is: ", "")
            for c in context:
                 if c.cause_by == CreateSolutions:
                      needed_context += c.instruct_content.dict()["Project name"] + "\n"
                      solutions = c.instruct_content.dict()["Solutions"]
                      for product in solutions:
                           if product["Product name"]== best_product:
                                needed_context += str(product) + "\n"
            needed_context += best_product_string
            logger.debug("\n#######################################################\nSUMMARISATION NEEDED CONTEXT: ",needed_context,"\n#######################################################\n")
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