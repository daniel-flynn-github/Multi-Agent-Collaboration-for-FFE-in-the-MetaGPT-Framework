

from metagpt.actions import CreateJourneyMaps,CreateNeeds
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import ActionOutput
from metagpt.logs import logger
from metagpt.schema import Message


class NeedsAnalyst(Role):

    def __init__(
        self,
        name: str = "Bob",
        profile: str = "Needs Analyst",
        goal: str = "Given a description of a person generate issues they are likely to encounter",
        constraints: str = "Come up with issues that are not already addressed by products on the market",
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([CreateNeeds])

        # Set events or actions the Architect should watch or be aware of
        self._watch({CreateJourneyMaps})

        

