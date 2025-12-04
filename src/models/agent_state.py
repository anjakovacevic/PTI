from pydantic import BaseModel, Field
from typing import List

class AgentState(BaseModel):
    """
    Represents the state of a single agent.
    """
    agent_id: int = Field(..., description="Unique identifier of the agent")
    value: float = Field(..., description="Current value held by the agent")
    neighbors: List[int] = Field(default_factory=list, description="List of neighbor agent IDs")
