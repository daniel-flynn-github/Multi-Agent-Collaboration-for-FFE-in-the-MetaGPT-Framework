
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
        constraints: str = "If you have independent knowledge of the company or the field it is part of, incorporate it. If not, only use the context provided. Make assumptions and be bold with your responses.",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        self._set_react_mode("by_order")
        self.feasibilities = {}
        self.feasibility_scores = {}


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
            if context[-1].cause_by == AnalyseFeasibility: 
                needed_context = context[0].content + context[-2].content
            else:
                needed_context = context[0].content + context[-1].content
            response = await self._rc.todo.run(needed_context)
            # logger.info(response)
            if context[-1].cause_by == CreateSolutions:
                self.feasibilities = response.instruct_content.dict()["Feasibility"]
                for product in self.feasibilities:
                    self.feasibility_scores[product["Product name"][0]] = product["Average Score"][0]
                if isinstance(response, ActionOutput):
                    msg = Message(content=response.content, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
                self._rc.memory.add(msg)
            else:
                marketability_scores = {}
                marketability = response.instruct_content.dict()["Market Viability"]
                for product in marketability:
                    marketability_scores[product["Product name"][0]] = product["Average Score"][0]
                overall_scores = {}
                for product,mscore in marketability_scores.items():
                    overall_scores[product] = (float(self.feasibility_scores[product]) + float(mscore))/2
                best_product = max(overall_scores, key=overall_scores.get)
                logger.debug("The best product is: " + best_product)
                best_product_string = "The best product is: " + best_product + "\n"
                for product in self.feasibilities:
                    if product["Product name"][0] == best_product:
                        best_product_string += str(product) + "\n"
                for product in marketability:
                    if product["Product name"][0] == best_product:
                        best_product_string += str(product) + "\n"
                if isinstance(response, ActionOutput):
                    msg = Message(content=best_product_string, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=best_product_string, role=self.profile, cause_by=type(self._rc.todo))
            return msg