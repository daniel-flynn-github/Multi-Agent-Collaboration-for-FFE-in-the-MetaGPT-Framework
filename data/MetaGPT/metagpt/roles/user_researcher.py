from metagpt.actions import BossRequirement, CreatePersonas
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message

class UserResearcher(Role):
    """
    Represents a Product

    Attributes:
        name (str): Name of the product manager.
        profile (str): Role profile, default is 'Product Manager'.
        goal (str): Goal of the product manager.
        constraints (str): Constraints or limitations for the product manager.
    """

    def __init__(
        self,
        name: str = "Time",
        profile: str = "User Researcher",
        goal: str = "Create user personas describing people who would encounter a given topic in their lives",
        constraints: str = "Use your knowledge base to create as detailed and realistic personas as possible",
    ) -> None:
        super().__init__(name, profile, goal, constraints)
        self._init_actions([CreatePersonas])
        self._watch([BossRequirement])