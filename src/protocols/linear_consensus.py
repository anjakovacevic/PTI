import random
from typing import List
from src.domain.abstract_protocol import AbstractProtocol
from src.models.agent_state import AgentState
from src.services.configuration_service import ConfigurationService


class LinearConsensus(AbstractProtocol):
    """
    Standard Linear Consensus Protocol: x_i(k+1) = x_i(k) + epsilon * sum(x_j - x_i)
    """

    def __init__(self):
        self.config = ConfigurationService().get_configuration()

    def calculate_next_value(
        self, current_state: AgentState, neighbor_states: List[AgentState]
    ) -> float:
        if not neighbor_states:
            return current_state.value

        # Calculate the sum of differences
        diff_sum = sum(
            neighbor.value - current_state.value for neighbor in neighbor_states
        )

        # Add noise if configured
        noise = 0.0
        if self.config.noise_level > 0:
            noise = random.gauss(0, self.config.noise_level)

        # Update rule
        next_val = current_state.value + self.config.epsilon * diff_sum + noise
        return next_val
