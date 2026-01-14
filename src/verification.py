import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from src.models.configuration import SimulationConfiguration
from src.services.configuration_service import ConfigurationService
from src.simulation.consensus_model import ConsensusModel
from src.protocols.protocol_factory import ProtocolFactory


def run_simulation(protocol_type, steps=50):
    config = SimulationConfiguration(
        number_of_agents=10,
        topology="random",
        protocol_type=protocol_type,
        epsilon=0.1,
        noise_level=0.0,
        max_steps=steps,
    )
    ConfigurationService().set_configuration(config)
    model = ConsensusModel(ProtocolFactory())

    history = []
    model.run()

    # Re-initialize for manual stepping
    model = ConsensusModel(ProtocolFactory())
    step_data = []

    for _ in range(steps):
        model.step()
        values = [a.state.value for a in model.agents]
        step_data.append(values)

    return step_data


def verify():
    print("Running Linear Consensus...")
    linear_data = run_simulation("linear")

    print("Running Max Consensus...")
    max_data = run_simulation("max_consensus")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Linear Plot
    for i in range(len(linear_data[0])):
        agent_vals = [step[i] for step in linear_data]
        ax1.plot(agent_vals)
    ax1.set_title("Linear Consensus")
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Value")

    # Max Plot
    for i in range(len(max_data[0])):
        agent_vals = [step[i] for step in max_data]
        ax2.plot(agent_vals)
    ax2.set_title("Max Consensus")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Value")

    plt.tight_layout()
    plt.savefig("comparison_plot.png")
    print("Comparison plot saved to comparison_plot.png")


if __name__ == "__main__":
    verify()
