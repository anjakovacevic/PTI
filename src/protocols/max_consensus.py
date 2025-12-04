from typing import List
from src.domain.abstract_protocol import AbstractProtocol
from src.models.agent_state import AgentState

class MaxConsensus(AbstractProtocol):
    """
    Max-Consensus Protocol: x_i(k+1) = max(x_i(k), max(x_j(k)))
    """
    def calculate_next_value(self, current_state: AgentState, neighbor_states: List[AgentState]) -> float:
        if not neighbor_states:
            return current_state.value

        # Find the maximum value among neighbors
        max_neighbor_val = max(neighbor.value for neighbor in neighbor_states)
        
        # Update rule: take the max of self and neighbors
        return max(current_state.value, max_neighbor_val)
