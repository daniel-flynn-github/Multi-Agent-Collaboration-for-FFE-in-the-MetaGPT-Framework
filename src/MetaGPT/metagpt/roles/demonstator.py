
from metagpt.actions import EvaluateSocialValue, CreateIdeas, Summarise
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
        goal: str = "Return a report summarising an innovation idea",
        constraints: str = ""
    ) -> None:
        super().__init__(name, profile, goal, constraints)


        #Initialise associated actions
        self._init_actions([Summarise])

        #Set Actions to watch for
        self._watch([EvaluateSocialValue])

    
    async def _act(self) -> Message:
            logger.info(f"{self._setting}: ready to {self._rc.todo}")
            context = self.get_memories()
            needed_context = ""
            #Look for best idea from evaluations
            best_idea_string = context[-1].content
            #Look back through memory for steps taken to generate and select the best idea
            lines = best_idea_string.split("\n")
            best_idea = lines[0].replace("The best idea is: ", "")
            for c in context:
                 if c.cause_by == CreateIdeas:
                      needed_context += c.instruct_content.dict()["Project name"] + "\n"
                      ideas = c.instruct_content.dict()["Ideas"]
                      for idea in ideas:
                           if idea["Idea name"]== best_idea:
                                needed_context += str(idea) + "\n"
            needed_context += best_idea_string
            needed_context += ("\n\n Original Brief: \n" + context[0].content)
            logger.debug("\n#######################################################\nSUMMARISATION NEEDED CONTEXT: ",needed_context,"\n#######################################################\n")
            #Run Summarise action
            response = await self._rc.todo.run(needed_context)
            logger.info(response)
            #Publish response
            if isinstance(response, ActionOutput):
                msg = Message(content=response.content, instruct_content=response.instruct_content,
                            role=self.profile, cause_by=type(self._rc.todo))
            else:
                msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
            self._rc.memory.add(msg)

            return msg