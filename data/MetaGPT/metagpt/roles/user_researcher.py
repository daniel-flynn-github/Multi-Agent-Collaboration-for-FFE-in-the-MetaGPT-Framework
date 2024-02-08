from metagpt.actions import BossRequirement, CreatePersonas
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.config import CONFIG

class UserResearcher(Role):

    def __init__(
        self,
        name: str = "Time",
        profile: str = "User Researcher",
        goal: str = "Create user personas describing people who would encounter a given topic in their lives",
        constraints: str = "Use your knowledge base to create as detailed and realistic personas as possible",
    ) -> None:
        super().__init__(name, profile, goal, constraints)
        self._init_actions([CreatePersonas])
        if CONFIG.human_ideas == False:
            self._watch({BossRequirement})