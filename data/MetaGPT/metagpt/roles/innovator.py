
from metagpt.actions import SynthesiseNeed, CreateInitiatives
from metagpt.roles import Role


class Innovator(Role):


    def __init__(
        self,
        name: str = "Bobylon",
        profile: str = "Innovator",
        goal: str = "Given a need, come up with product initiatives",
        constraints: str = "Strictly try to solve the need, be creative and detailed in your response"
    ) -> None:
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([CreateInitiatives])

        # Set events or actions the Architect should watch or be aware of
        self._watch({SynthesiseNeed})