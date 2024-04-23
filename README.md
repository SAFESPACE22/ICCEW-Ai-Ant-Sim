# NEAT Ant Simulation
This project simulates the movement of ants using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. Ants are controlled by neural networks trained through genetic algorithms to navigate a map environment without colliding with obstacles.

## Requirements
Python 3.x
Pygame
NEAT-Python
## Installation
Clone or download this repository to your local machine.
Install the required Python packages using pip:
bash
Copy code
pip install pygame
pip install neat-python
## Usage
Run the simulation script:
bash
Copy code
python ant_simulation.py
The simulation will start, and you'll see ants navigating the environment. The simulation runs for a maximum of 1000 generations.
## Configuration
The configuration for the NEAT algorithm is provided in the config.txt file. You can adjust parameters such as population size, mutation rates, and compatibility threshold to customize the algorithm's behavior.

Customization
You can modify the map layout by replacing the map1.png file in the project directory with your own map image.
Adjust the size and speed of ants by modifying the ANT_SIZE_X, ANT_SIZE_Y, and speed attributes in the script.
## Credits
This project is inspired by NEAT-Python and Pygame.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to adjust or expand upon this README to suit your needs!
