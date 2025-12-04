from abc import ABC, abstractmethod
from typing import List
from src.models.agent_state import AgentState

class AbstractProtocol(ABC):
    """
    Interface for consensus protocols.
    """

    @abstractmethod
    def calculate_next_value(self, current_state: AgentState, neighbor_states: List[AgentState]) -> float:
        """
        Calculate the next value for an agent based on its current state and neighbors' states.
        
        Args:
            current_state: The current state of the agent.
            neighbor_states: A list of states of the agent's neighbors.
            
        Returns:
            The new value for the agent.
        """
        pass
