
from metagpt.actions import CreateIdeas, EvaluateTechnicalValue, EvaluateCustomerValue, EvaluateFinancialValue, EvaluateMarketValue, EvaluateSocialValue, CreatePersonas
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message





class Evaluator(Role):

    #Role Profile
    def __init__(
        self,
        name: str = "Expert",
        profile: str = "Evaluator",
        goal: str = "Given a innovation idea and the context of a company, evaluate the idea",
        constraints: str = "If you have independent knowledge of the company or the field it is part of, incorporate it. If not, only use the context provided. Make assumptions and be bold with your responses.",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        #Action Selection Logic
        self._set_react_mode("by_order")
        self.idea_scores = {}


        #Initialise associated actions
        self._init_actions([EvaluateTechnicalValue, EvaluateMarketValue, EvaluateFinancialValue, EvaluateCustomerValue,EvaluateSocialValue])

        #Set Actions to watch for
        self._watch([CreateIdeas])

    
    async def _act(self) -> Message:

            #Method to extract idea scores from each evaluation action
            def get_scores():
                values = response.instruct_content.dict()["Values"]
                for idea in values:
                    self.idea_scores[idea["Idea name"][0]] += idea["AVERAGE SCORE"][1]
                if isinstance(response, ActionOutput):
                    msg = Message(content=response.content, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
                self._rc.memory.add(msg)
                return msg
            #Provide each evaluation Action with the needed contextual information from memory
            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            if context[-1].cause_by == EvaluateTechnicalValue: 
                needed_context = context[0].content + context[-2].content
            elif context[-1].cause_by == EvaluateMarketValue:
                needed_context = context[0].content + context[-3].content
            elif context[-1].cause_by == EvaluateFinancialValue:
                if context[1].cause_by == CreatePersonas:
                    needed_context = context[0].content + context[-4].content + context[1].content
                else:
                    needed_context = context[0].content + context[-4].content
            elif context[-1].cause_by == EvaluateCustomerValue:
                if context[1].cause_by == CreatePersonas:
                    needed_context = context[0].content + context[-5].content + context[1].content
                else:
                    needed_context = context[0].content + context[-5].content
            else:
                needed_context = context[0].content + context[-1].content
            response = await self._rc.todo.run(needed_context)
            logger.info(response)
            #Extract and store idea scores from each evaluation Action
            if context[-1].cause_by == CreateIdeas:
                technical_value = response.instruct_content.dict()["Values"]
                for idea in technical_value:
                    self.idea_scores[idea["Idea name"][0]] = idea["AVERAGE SCORE"][1]
                if isinstance(response, ActionOutput):
                    msg = Message(content=response.content, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
                self._rc.memory.add(msg)
            elif context[-1].cause_by in [EvaluateTechnicalValue, EvaluateMarketValue, EvaluateFinancialValue]:
                msg = get_scores()
            elif context[-1].cause_by == EvaluateCustomerValue:
                #Calculate the best idea
                values = response.instruct_content.dict()["Values"]
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
                    values = c.instruct_content.dict()["Values"]
                    for idea in values:
                        if idea["Idea name"][0] == best_idea:
                            best_idea_string += str(idea) + "\n"
                #Publish the best idea to the environment
                if isinstance(response, ActionOutput):
                    msg = Message(content=best_idea_string, instruct_content=response.instruct_content,
                                role=self.profile, cause_by=type(self._rc.todo))
                else:
                    msg = Message(content=best_idea_string, role=self.profile, cause_by=type(self._rc.todo))
            return msg
    
