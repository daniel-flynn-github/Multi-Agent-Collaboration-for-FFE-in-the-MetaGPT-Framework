
from metagpt.actions import CreateIdeas, EvaluateTechnicalValue, EvaluateCustomerValue, EvaluateFinancialValue, EvaluateMarketValue, EvaluateSocialValue
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message





class Evaluator(Role):


    def __init__(
        self,
        name: str = "Bobylonathan",
        profile: str = "Evaluator",
        goal: str = "Given a product update idea and the context of a company, evaluate the idea",
        constraints: str = "If you have independent knowledge of the company or the field it is part of, incorporate it. If not, only use the context provided. Make assumptions and be bold with your responses.",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        self._set_react_mode("by_order")
        self.idea_scores = {}


        # Initialize actions specific to the Architect role
        self._init_actions([EvaluateTechnicalValue, EvaluateMarketValue, EvaluateFinancialValue, EvaluateCustomerValue,EvaluateSocialValue])

        # Set events or actions the Architect should watch or be aware of
        self._watch([CreateIdeas])

    
    async def _act(self) -> Message:
            # prompt = self.get_prefix()
            # prompt += ROLE_TEMPLATE.format(name=self.profile, state=self.states[self.state], result=response,
            #                                history=self.history)

            def get_scores(dict_string):
                values = response.instruct_content.dict()[dict_string]
                for idea in values:
                    self.idea_scores[idea["Idea name"][0]] += idea["AVERAGE SCORE"][1]
                if isinstance(response, ActionOutput):
                    msg = Message(content=response.content, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
                self._rc.memory.add(msg)
                return msg

            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            if context[-1].cause_by == EvaluateTechnicalValue: 
                needed_context = context[0].content + context[-2].content
            elif context[-1].cause_by == EvaluateMarketValue:
                needed_context = context[0].content + context[-3].content
            elif context[-1].cause_by == EvaluateFinancialValue:
                needed_context = context[0].content + context[-4].content
            elif context[-1].cause_by == EvaluateCustomerValue:
                needed_context = context[0].content + context[-5].content
            else:
                needed_context = context[0].content + context[-1].content
            response = await self._rc.todo.run(needed_context)
            logger.info(response)
            if context[-1].cause_by == CreateIdeas:
                technical_value = response.instruct_content.dict()["Technical value"]
                for idea in technical_value:
                    self.idea_scores[idea["Idea name"][0]] = idea["AVERAGE SCORE"][1]
                if isinstance(response, ActionOutput):
                    msg = Message(content=response.content, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
                self._rc.memory.add(msg)
            elif context[-1].cause_by == EvaluateTechnicalValue:
                msg = get_scores("Market value")
            elif context[-1].cause_by == EvaluateMarketValue:
                msg = get_scores("Financial value")
            elif context[-1].cause_by == EvaluateFinancialValue:
                msg = get_scores("Customer value")
            elif context[-1].cause_by == EvaluateCustomerValue:
                values = response.instruct_content.dict()["Social value"]
                for idea in values:
                    self.idea_scores[idea["Idea name"][0]] += idea["AVERAGE SCORE"][1]
                best_idea = max(self.idea_scores, key=self.idea_scores.get)
                logger.debug("The best idea is: " + best_idea)
                best_idea_string = "The best idea is: " + best_idea + "\n"
                for idea in values:
                    if idea["Idea name"][0] == best_idea:
                        best_idea_string += str(idea) + "\n"
                for c in reversed(context):
                    if c.cause_by == CreateIdeas:
                        break
                    values = c.instruct_content.dict()["Customer value"]
                    for idea in values:
                        if idea["Idea name"][0] == best_idea:
                            best_idea_string += str(idea) + "\n"
                if isinstance(response, ActionOutput):
                    msg = Message(content=best_idea_string, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=best_idea_string, role=self.profile, cause_by=type(self._rc.todo))
            return msg
    
