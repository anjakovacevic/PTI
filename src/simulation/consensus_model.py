from mesa import Model
from mesa.space import NetworkGrid
import networkx as nx
import random

from src.domain.abstract_simulation import AbstractSimulation
from src.simulation.consensus_agent import ConsensusAgent
from src.services.logger_service import LoggerService
from src.services.configuration_service import ConfigurationService


class ConsensusModel(Model, AbstractSimulation):
    """
    MESA Model for the consensus simulation.
    """

    def __init__(self, protocol_factory):
        super().__init__()
        self.config = ConfigurationService().get_configuration()
        self.protocol_factory = protocol_factory
        # self.schedule = SimultaneousActivation(self) # Removed in Mesa 3.x
        self.running = True
        self.step_count = 0

        self._initialize_network()
        self._create_agents()

    def _initialize_network(self):
        if self.config.topology == "random":
            self.G = nx.erdos_renyi_graph(
                n=self.config.number_of_agents, p=self.config.connection_probability
            )
        elif self.config.topology == "ring":
            self.G = nx.cycle_graph(n=self.config.number_of_agents)
        elif self.config.topology == "fully_connected":
            self.G = nx.complete_graph(n=self.config.number_of_agents)
        else:
            # Default to random if unknown
            LoggerService.log_warning(
                f"Unknown topology {self.config.topology}, defaulting to random."
            )
            self.G = nx.erdos_renyi_graph(n=self.config.number_of_agents, p=0.3)

        self.grid = NetworkGrid(self.G)

    def _create_agents(self):
        for i, node in enumerate(self.G.nodes()):
            # Initialize with random value between 0 and 100
            initial_value = random.uniform(0, 100)

            # Create protocol instance for this agent
            protocol = self.protocol_factory.create_protocol()

            agent = ConsensusAgent(
                unique_id=i, model=self, initial_value=initial_value, protocol=protocol
            )

            self.grid.place_agent(agent, node)

    def step(self):
        self.agents.do("step")
        self.agents.do("advance")

        self.step_count += 1
        if self.step_count >= self.config.max_steps:
            self.running = False

    def run(self):
        while self.running:
            self.step()

    def reset(self):
        self.step_count = 0
        self.running = True

        if hasattr(self, "agents"):
            self.agents.remove(self.agents)
        self._initialize_network()
        self._create_agents()
