# Linear Consensus Protocol Simulation

A modular, object-oriented Python implementation of linear consensus protocols in multi-agent systems, built with the MESA framework.

## Overview

This project simulates how a network of agents with imperfect measurements can reach an agreement (consensus) using distributed algorithms. It compares two protocols:
1.  **Linear Consensus**: Agents converge to the average value.
2.  **Max-Consensus**: Agents converge to the maximum value.

## Features

-   **Clean Architecture**: Separation of concerns (Domain, Models, Simulation, Protocols, UI).
-   **MESA Framework**: Robust agent-based modeling.
-   **Configurable Topologies**: Random, Ring, and Fully Connected graphs.
-   **Real-time Visualization**: Tkinter-based GUI.
-   **Verification**: Automated comparison scripts.

## Run the project

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the GUI
    To start the interactive simulation:
    ```bash
    python src/main.py
    ```

4. Run Verification
    To generate a comparison plot of the protocols:
    ```bash
    python src/verification.py
    ```

