

from metagpt.actions import SynthesiseNeed,CreateNeeds
from metagpt.roles import Role
from metagpt.schema import Message


class DesignManager(Role):


    def __init__(
        self,
        name: str = "Bobathan",
        profile: str = "Design Manager",
        goal: str = "Synthesis a fundamental need based on a collection of needs",
        constraints: str = "Try to ensure the fundamental is relevant to as many of the needs in the collection as possible",
    ) -> None:
        """Initializes the Architect with given attributes."""
        super().__init__(name, profile, goal, constraints)

        # Initialize actions specific to the Architect role
        self._init_actions([SynthesiseNeed])

        # Set events or actions the Architect should watch or be aware of
        #self._watch({CreateNeeds})
        

