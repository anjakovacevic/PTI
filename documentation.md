# Analysis and Implementation of Linear Consensus Protocols in Multi-Agent Systems

**Abstract**
This project explores the implementation and simulation of consensus algorithms in networked multi-agent systems. Specifically, we analyze the standard Linear Consensus Protocol and compare it against a Max-Consensus strategy. The system is implemented using the MESA framework in Python, adhering to clean architecture principles to ensure modularity and extensibility. Simulation results demonstrate the convergence properties of both protocols under various network topologies.

## 1. Introduction
In the field of distributed control and multi-agent systems (MAS), consensus problems—where a group of agents must agree on a shared value—are fundamental. Applications range from formation control of UAVs to distributed sensor networks. As discussed by Olfati-Saber et al. in *Consensus and Cooperation in Networked Multi-Agent Systems*, algorithms that facilitate rapid agreement are critical for effective teamwork.

This project aims to simulate these dynamics, allowing agents with imperfect local measurements to communicate with neighbors and converge to a common state.

## 2. Methodology

### 2.1 Linear Consensus Protocol
The primary protocol implemented is the discrete-time linear consensus algorithm. For an agent $i$ with state $x_i$ at time $k$, the update rule is given by:

$$ x_i(k+1) = x_i(k) + \epsilon \sum_{j \in N_i} (x_j(k) - x_i(k)) $$

Where:
- $N_i$ is the set of neighbors of agent $i$.
- $\epsilon$ is the step size (0 < $\epsilon$ < $1/\Delta_{max}$).
- The system converges to the average of the initial states: $\bar{x} = \frac{1}{N} \sum x_i(0)$.

### 2.2 Max-Consensus Protocol
As an alternative for comparison, we implemented a Max-Consensus protocol. This is a non-linear strategy often used for leader election or extrema finding. The update rule is:

$$ x_i(k+1) = \max(x_i(k), \max_{j \in N_i} x_j(k)) $$

Agents simply adopt the largest value observed in their local neighborhood. The system converges to the global maximum of the initial states.

### 2.3 Network Topologies and Their Influence
The network topology dictates how information flows between agents, directly impacting the **convergence rate** (how fast they agree). This project implements three distinct topologies:

1.  **Random Graph (Erdős-Rényi)**
    -   **Structure**: Agents are connected randomly with a probability $p$ (default 0.3).
    -   **Influence**: This models realistic ad-hoc networks. The convergence speed is generally fast, governed by the "algebraic connectivity" (the second smallest eigenvalue of the Laplacian matrix). As long as the graph is connected, agents will reach consensus relatively quickly.

2.  **Ring Lattice**
    -   **Structure**: Agents are arranged in a circle, connected only to their immediate left and right neighbors.
    -   **Influence**: This topology has a large **diameter** (distance between farthest nodes). Information travels slowly, hop-by-hop. Consequently, convergence is **very slow**, especially for Linear Consensus, as values diffuse gradually across the ring.

3.  **Fully Connected**
    -   **Structure**: Every agent is connected to every other agent.
    -   **Influence**: The diameter is 1.
        -   For **Max-Consensus**, convergence is instantaneous (1 step), as every agent immediately sees the global maximum.
        -   For **Linear Consensus**, convergence is extremely rapid because the "mixing" of values happens globally in every iteration.

## 3. System Architecture
The software is engineered following **Clean Architecture** and **Object-Oriented Programming (OOP)** principles to ensure separation of concerns.

### 3.1 Layered Design
- **Domain Layer**: Defines abstract base classes (`AbstractSimulation`, `AbstractProtocol`) representing the core business logic independent of implementation details.
- **Models Layer**: Uses **Pydantic** for rigorous data validation of configuration and agent states.
- **Simulation Layer**: Built on the **MESA** framework. `ConsensusAgent` and `ConsensusModel` handle the agent-based modeling logic.
- **Protocols Layer**: Implements the **Strategy Pattern** via a `ProtocolFactory`, allowing dynamic switching between consensus algorithms without modifying agent code.
- **Services Layer**: **Singleton** services for Configuration and Logging ensure consistent global state management.
- **UI Layer**: A **Tkinter**-based GUI provides real-time visualization of agent states.

### 3.2 The MESA Framework
MESA is a modular framework for building, analyzing, and visualizing agent-based models in Python. It allows users to create agent-based models using built-in core components (such as spatial grids and agent schedulers) or custom implementations. In this project, MESA provides the backbone for the simulation:
- **Model Class**: Manages the global state, time stepping, and the environment (the graph topology).
- **Agent Class**: The base class for `ConsensusAgent`, handling unique IDs and model references.
- **NetworkGrid**: Manages the topological connections between agents, allowing efficient neighbor queries essential for consensus protocols.
- **Data Collection**: (Implicitly used) MESA facilitates tracking agent states over time, which we manually aggregate for the GUI and verification plots.

## 4. Implementation Details
The project is developed in Python 3.12. 

- **Agent Logic**: Each `ConsensusAgent` maintains a local state and a reference to a protocol strategy. In every step, it queries its neighbors via the MESA grid and applies the protocol's update rule.
- **Noise Handling**: To simulate real-world sensors, Gaussian noise can be injected into the linear consensus updates, allowing analysis of protocol robustness.

## 5. Results and Discussion
Simulations were conducted with $N=10$ to $N=100$ agents.

- **Linear Consensus**: Agents successfully converged to the average value. Convergence time increased with the sparsity of the graph (e.g., Ring topology took significantly longer than Random Graph).
- **Max-Consensus**: Convergence was extremely rapid, propagating the maximum value across the network diameter in $D$ steps, where $D$ is the graph diameter.

The comparison highlights the trade-off between the type of agreement (average vs. extremum) and the speed of convergence.

## 6. Conclusion
We successfully implemented a modular simulation environment for consensus protocols. The use of design patterns like Factory and Strategy allowed for seamless comparison of different algorithms. The results validate the theoretical convergence properties of Linear and Max-Consensus protocols. Future work could extend this framework to include leader-follower dynamics or switching topologies.

## References
1. R. Olfati-Saber, J. A. Fax and R. M. Murray, "Consensus and Cooperation in Networked Multi-Agent Systems," in *Proceedings of the IEEE*, vol. 95, no. 1, pp. 215-233, Jan. 2007.
