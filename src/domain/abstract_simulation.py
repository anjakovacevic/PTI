from abc import ABC, abstractmethod

class AbstractSimulation(ABC):
    """
    Abstract base class for a cooperative game/simulation.
    """

    @abstractmethod
    def run(self):
        """
        Run the simulation to completion.
        """
        pass

    @abstractmethod
    def step(self):
        """
        Advance the simulation by one step.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset the simulation to its initial state.
        """
        pass
