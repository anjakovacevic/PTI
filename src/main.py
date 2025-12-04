import sys
import os

# Add the project root to the python path
# We need to go up one level from 'src' to get to the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.gui import run_gui

if __name__ == "__main__":
    run_gui()
