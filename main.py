# enhanced-task-manager-design/main.py
import sys
import os

# Add the project root to the Python path so the 'src' package can be imported.
# (task_manager.py / data_persistence.py use relative imports like "from .task import Task",
#  so they must be imported as part of the 'src' package.)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main components of our application
from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    """
    Main entry point for the Enhanced Task Manager application.
    Initializes TaskManager and CLIInterface, then starts the CLI loop.
    """
    manager = TaskManager()  # Initialize the core logic manager
    cli = CLIInterface(manager)  # Initialize the CLI interface, passing the manager
    cli.run()  # Start the main command-line interaction loop


if __name__ == "__main__":
    main()
