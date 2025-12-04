import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import threading
import time

from src.models.configuration import SimulationConfiguration
from src.services.configuration_service import ConfigurationService
from src.services.logger_service import LoggerService
from src.simulation.consensus_model import ConsensusModel
from src.protocols.protocol_factory import ProtocolFactory

class SimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Consensus Simulation")
        
        self.simulation_running = False
        self.model = None
        self.thread = None
        
        self._create_widgets()
        self._setup_plot()

    def _create_widgets(self):
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Configuration")
        config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Number of Agents
        ttk.Label(config_frame, text="Number of Agents:").pack(pady=5)
        self.num_agents_var = tk.IntVar(value=10)
        ttk.Entry(config_frame, textvariable=self.num_agents_var).pack()

        # Topology
        ttk.Label(config_frame, text="Topology:").pack(pady=5)
        self.topology_var = tk.StringVar(value="random")
        ttk.Combobox(config_frame, textvariable=self.topology_var, 
                     values=["random", "ring", "fully_connected"]).pack()

        # Protocol
        ttk.Label(config_frame, text="Protocol:").pack(pady=5)
        self.protocol_var = tk.StringVar(value="linear")
        ttk.Combobox(config_frame, textvariable=self.protocol_var, 
                     values=["linear", "max_consensus"]).pack()

        # Epsilon
        ttk.Label(config_frame, text="Epsilon (Step Size):").pack(pady=5)
        self.epsilon_var = tk.DoubleVar(value=0.1)
        ttk.Entry(config_frame, textvariable=self.epsilon_var).pack()

        # Noise
        ttk.Label(config_frame, text="Noise Level:").pack(pady=5)
        self.noise_var = tk.DoubleVar(value=0.0)
        ttk.Entry(config_frame, textvariable=self.noise_var).pack()

        # Run Button
        self.run_btn = ttk.Button(config_frame, text="Run Simulation", command=self.start_simulation)
        self.run_btn.pack(pady=20)

        # Stop Button
        self.stop_btn = ttk.Button(config_frame, text="Stop", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

    def _setup_plot(self):
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Agent Values Over Time")
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def start_simulation(self):
        try:
            config = SimulationConfiguration(
                number_of_agents=self.num_agents_var.get(),
                topology=self.topology_var.get(),
                protocol_type=self.protocol_var.get(),
                epsilon=self.epsilon_var.get(),
                noise_level=self.noise_var.get(),
                max_steps=200 # Fixed for GUI run
            )
            ConfigurationService().set_configuration(config)
            
            self.model = ConsensusModel(ProtocolFactory())
            self.simulation_running = True
            self.run_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.agent_values_history = [[] for _ in range(config.number_of_agents)]
            self.steps = []
            
            # Start animation
            self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=100, blit=False, cache_frame_data=False)
            self.canvas.draw()
            
        except Exception as e:
            LoggerService.log_error(f"Error starting simulation: {e}")

    def stop_simulation(self):
        self.simulation_running = False
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def update_plot(self, frame):
        if self.simulation_running and self.model.running:
            self.model.step()
            
            current_step = self.model.step_count
            self.steps.append(current_step)
            
            # Collect values
            agents = sorted(self.model.agents, key=lambda a: a.unique_id)
            for i, agent in enumerate(agents):
                self.agent_values_history[i].append(agent.state.value)
            
            self.ax.clear()
            self.ax.set_title(f"Agent Values (Step {current_step})")
            self.ax.set_xlabel("Step")
            self.ax.set_ylabel("Value")
            
            for i in range(len(agents)):
                self.ax.plot(self.steps, self.agent_values_history[i], label=f"Agent {i}")
            
            # Only show legend if few agents
            if len(agents) <= 5:
                self.ax.legend()
                
            if not self.model.running:
                self.stop_simulation()
        return self.ax,

def run_gui():
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()
