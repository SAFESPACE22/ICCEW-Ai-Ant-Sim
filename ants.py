import math
import random

import neat
import pygame

WIDTH = 2880
HEIGHT = 1800

ANT_SIZE_X = 30    
ANT_SIZE_Y = 30

BORDER_COLOR = (34, 177, 76) # Color To Crash on Hit

current_generation = 0 # Generation counter

class Ant:
    def __init__(self):
        """
        Initialize method for the ant object.

        This method initializes various attributes of the ant object, such as loading the ant sprite image, setting its initial position,
        angle, and speed, calculating its center, initializing radar lists, and setting flags for default speed and whether the ant is alive.

        Parameters:
            None

        Returns:
            None
        """
        # Load Car Sprite and Rotate
        self.ant = pygame.image.load('ai-ant/ant.png').convert() # Convert Speeds Up A Lot
        self.ant = pygame.transform.scale(self.ant, (ANT_SIZE_X, ANT_SIZE_Y))
        self.rotated_ant = self.ant 
        #self.position = [1000, 980] # Starting Position map
        self.position = [100, 936] # Starting Position map1

        self.angle = 0
        self.speed = 0

        self.speed_set = False # Flag For Default Speed Later on

        self.center = [self.position[0] + ANT_SIZE_X / 2, self.position[1] + ANT_SIZE_Y / 2] # Calculate Center

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn

        self.alive = True # Boolean To Check If Car is Crashed

        self.distance = 0 # Distance Driven
        self.time = 0 # Time Passed
    
    def draw(self, screen):
        """
        Method to draw the ant on the screen.

        This method blits (draws) the rotated ant sprite onto the given screen at its current position.

        Parameters:
            screen (object): The Pygame screen object to draw the ant on.

        Returns:
            None
        """
        screen.blit(self.rotated_ant, self.position)

    def check_ant_collision(self, game_map):
        """
        Method to check for collisions between the ant and the game map borders.

        This method checks each corner of the ant's bounding box to see if it touches the border color on the game map,
        indicating a collision. If a collision is detected, it sets the 'alive' attribute of the ant to False.

        Parameters:
            game_map (object): The game map object containing information about the game environment.

        Returns:
            None
        """
        for point in self.corners:
        # Assumes the ant's shape is a rectangle
        # Check if any corner touches border color, indicating a collision
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break
    
    def check_radar(self, degree, game_map):
        """
        Method to scan the surroundings of the ant at a specific degree angle.

        This method calculates the position of the ant's radar beam at a given degree angle, then scans the environment
        until it either reaches the border of the game map or reaches a maximum scanning length of 300 pixels.
        Upon completion of the scan, it calculates the distance to the border and appends this information along with
        the position to the ant's radar list.

        Parameters:
            degree (int): The degree angle at which to scan the surroundings.
            game_map (object): The game map object containing information about the game environment.

        Returns:
            None
        """
        # Initialize the variables
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Continue scanning until hitting BORDER_COLOR or reaching max length of 300
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate distance to the border and append to radars list
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        """
        Update method for the ant object.

        This method handles updating the position and state of the ant on the game map. It adjusts the ant's speed,
        calculates its new position, checks for collisions, and updates its radar readings. Additionally, it computes
        the new center and corner positions of the ant based on its rotation angle.
    
        Parameters:
            game_map (object): The game map object containing information about the game environment.

        Returns:
            None
        """
        # Initialize speed to 10 when having 4 output nodes for speed control
        if not self.speed_set:
            self.speed = 10
            self.speed_set = True

        # Rotate the ant and move it in the x-direction, ensuring it stays within bounds
        self.rotated_ant = self.rotate_center(self.ant, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1
        
        # Move the ant in the y-direction, ensuring it stays within bounds
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate new center and corners of the ant
        self.center = [int(self.position[0]) + ANT_SIZE_X / 2, int(self.position[1]) + ANT_SIZE_Y / 2]
        length = 0.5 * ANT_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_ant_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)
    
    def get_data(self):
        """
        Method to retrieve sensor data from the ant.

        This method collects distances from the ant's radar sensors to the nearest obstacle and normalizes these distances.
        The normalized distances are returned as a list of values.

        Parameters:
            None

        Returns:
            list: A list of normalized distances to obstacles as sensed by the ant's radar sensors.
        """
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
           
        # Normalize distances and store in return_values list
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        """
        Method to check if the ant is alive.

        This method returns a boolean value indicating whether the ant is alive (True) or not (False).

        Parameters:
            None

        Returns:
            bool: True if the ant is alive, False otherwise.
        """
        return self.alive

    def get_reward(self):
        """
        Method to calculate the reward for the ant.

        This method calculates the reward based on the distance traveled by the ant relative to its size.

        Parameters:
            None

        Returns:
            float: The reward value based on the distance traveled.
        """
        return self.distance / (ANT_SIZE_X / 2)
    
    def rotate_center(self, image, angle):
        """
        Method to rotate an image around its center.

        This method takes an image and rotates it by a specified angle around its center point.

        Parameters:
            image (object): The Pygame image object to be rotated.
            angle (float): The angle (in degrees) by which to rotate the image.

        Returns:
            object: The rotated Pygame image object.
        """
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        # Create a copy of the rectangle with updated center coordinates
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        # Extract the rotated portion of the image based on the new rectangle and return it
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

def run_simulation(genomes, config):
    """
    Function to run the simulation of ant movement using neural networks.

    This function initializes the Pygame environment, creates neural networks for each genome in the population,
    and simulates the movement of ants controlled by these neural networks. Ants move based on neural network outputs,
    with their fitness being evaluated based on how far they travel without colliding with obstacles.

    Parameters:
        genomes (list): List of genomes, each representing a neural network controlling an ant.
        config (object): Configuration object for NEAT algorithm.

    Returns:
        None
    """
    # Empty Collections For Nets and ants
    nets = []
    ants = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        ants.append(Ant())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('./ai-ant/map1.png').convert() # Convert Speeds Up A Lot.
    
    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Ant Get The Acton It Takes
        for i, ant in enumerate(ants):
            output = nets[i].activate(ant.get_data())
            choice = output.index(max(output))
            if choice == 0:
                ant.angle += 10 # Left
            elif choice == 1:
                ant.angle -= 10 # Right
            elif choice == 2:
                if(ant.speed - 2 >= 12):
                    ant.speed -= 2 # Slow Down
            else:
                ant.speed += 2 # Speed Up
        
        # Check If Ant Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, ant in enumerate(ants):
            if ant.is_alive():
                still_alive += 1
                ant.update(game_map)
                genomes[i][1].fitness += ant.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40: # Stop After About 20 Seconds
            break

        # Draw Map And All Ants That Are Alive
        screen.blit(game_map, (0, 0))
        for ant in ants:
            if ant.is_alive():
                ant.draw(screen)
        
        # Display Info
        text = generation_font.render("Number of Generations: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Ants Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60) # 60 FPS

if __name__ == "__main__":
    """
    Main function to start the simulation.

    This function loads the NEAT configuration, creates a population of neural networks,
    and runs the simulation for a maximum of 1000 generations.

    Parameters:
        None

    Returns:
        None
    """
    # Load Config
    config_path = "./ai-ant/config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
