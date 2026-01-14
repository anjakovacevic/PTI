from pydantic import BaseModel, Field
from typing import Literal


class SimulationConfiguration(BaseModel):
    """
    Configuration parameters for the consensus simulation.
    """

    number_of_agents: int = Field(
        ..., gt=1, description="Number of agents in the simulation"
    )
    topology: Literal["random", "ring", "fully_connected"] = Field(
        "random", description="Network topology"
    )
    connection_probability: float = Field(
        0.3, ge=0.0, le=1.0, description="Probability of connection for random graph"
    )
    protocol_type: Literal["linear", "max_consensus"] = Field(
        "linear", description="Consensus protocol to use"
    )
    noise_level: float = Field(
        0.0, ge=0.0, description="Standard deviation of measurement noise"
    )
    max_steps: int = Field(100, gt=0, description="Maximum number of simulation steps")
    epsilon: float = Field(
        0.1, gt=0.0, le=1.0, description="Step size for linear consensus"
    )
