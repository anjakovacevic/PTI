from mesa import Agent
from src.models.agent_state import AgentState
from src.domain.abstract_protocol import AbstractProtocol
from src.services.logger_service import LoggerService

class ConsensusAgent(Agent):
    """
    Agent participating in the consensus simulation.
    """
    def __init__(self, unique_id: int, model, initial_value: float, protocol: AbstractProtocol):
        super().__init__(model)
        self.unique_id = unique_id
        self.state = AgentState(
            agent_id=unique_id,
            value=initial_value,
            neighbors=[]
        )
        self.protocol = protocol
        self.next_value = initial_value

    def step(self):
        """
        Prepare the next state based on current state and neighbors.
        """
        # Get neighbors from the model's grid/network
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        neighbor_states = [n.state for n in neighbors if isinstance(n, ConsensusAgent)]
        
        # Update own neighbor list in state for record-keeping
        self.state.neighbors = [n.unique_id for n in neighbors]

        # Calculate next value using the protocol
        self.next_value = self.protocol.calculate_next_value(self.state, neighbor_states)
        
    def advance(self):
        """
        Apply the calculated next state.
        """
        self.state.value = self.next_value
