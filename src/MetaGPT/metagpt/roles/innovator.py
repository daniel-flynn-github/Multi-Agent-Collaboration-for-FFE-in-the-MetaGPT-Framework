
from metagpt.actions import CreateDesignPrinciples, CreateIdeas, BossRequirement
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.config import CONFIG
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message




class Innovator(Role):


    def __init__(
        self,
        name: str = "Innovator",
        profile: str = "Accomodating Learner",
        goal: str = "Come up with ideas to update a product to address a pain point, considering the project background provided",
        constraints: str = "You are an Accomodating Learner. Be as realistic and detailed as possible. Only suggest ideas that can be created with currently existing or soon to be exisiting technologies"
    ) -> None:
        super().__init__(name, profile, goal, constraints)

    
        #Initialise an watch actions depending on the configuration (evaluating human ideas or llm generated ideas)
        self._init_actions([CreateIdeas])
        print("CONFIG.human_ideas: ", CONFIG.human_ideas)
        if CONFIG.human_ideas == False:
            self._watch({CreateDesignPrinciples})
        else:
            self._watch({BossRequirement})

    async def _act(self) -> Message:
        #Get required context from the environment
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        background = self.get_memories()[0].content
        needed_context = background + "\n" + (self._rc.important_memory[0]).content
        #Run the action
        response = (await self._rc.todo.run(needed_context))
        logger.info(response)
        #Publish response to environment
        if isinstance(response, ActionOutput):
            msg = Message(content=response.content, instruct_content=response.instruct_content,
                        role=self.profile, cause_by=type(self._rc.todo))
        else:
            msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)
        return msg