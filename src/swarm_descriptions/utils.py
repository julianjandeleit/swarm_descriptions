from swarm_descriptions.datamodel import *
import math
import re
import random
import pandas as pd
from importlib import import_module
import logging
from copy import deepcopy
from dataclasses import asdict

def generate_square_of_walls(rect_length, rect_width):
    """
    Generate a square of walls with the specified length and width.

    Parameters:
    - length (float): The length of the square.
    - width (float): The width of the square.

    Returns:
    - list: A list of Wall objects forming a square.
    """

    wall_size_length = (0.01, rect_length, 0.1) # width, length, height
    wall_size_width = (0.01, rect_width, 0.1) # width, length, height

    # Walls forming a square
    half_length = rect_length / 2
    half_width = rect_width / 2

    #wall_0 = Wall(size=(0.1,0.1,1.0), pose=Pose((0,0,0),(0,0,0))) # center
    #logging.debug(wall_size)
    wall_1 = Wall(size=wall_size_length, pose=Pose((0,-half_width, 0.0), (90.0, 0.0, 0.0))) # right
    wall_2 = Wall(size=wall_size_width, pose=Pose((half_length, 0, 0.0), (0.0, 0.0, 0.0))) # top
    wall_3 = Wall(size=wall_size_length, pose=Pose((0, half_width, 0), (90.0, 0.0, 0.0))) # left
    wall_4 = Wall(size=wall_size_width, pose=Pose((-half_length, 0, 0), (0, 0.0, 0.0))) # bottom

    # Create a list of walls
    walls = [wall_1, wall_2, wall_3, wall_4]
    return walls

def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier

def round_down(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier

def generate_circular_walls(radius, num_walls):
    """
    Generate an n-gon of walls with the specified radius and number of sides.

    Parameters:
    - radius (float): The radius of the n-gon.
    - num_sides (int): The number of sides of the n-gon.

    Returns:
    - list: A list of Wall objects forming an n-gon.
    """
    angle_increment = 360.0 / num_walls
    side_length = 2 * radius * math.sin(math.radians(angle_increment / 2))
    wall_size = (0.01, side_length, 0.1)  # width, length, height

    # Create a list of walls forming an n-gon
    walls = []
    for i in range(num_walls):
        start_angle = i * angle_increment
        end_angle = (i + 1) * angle_increment

        start_x = radius * math.cos(math.radians(start_angle))
        start_y = radius * math.sin(math.radians(start_angle))

        end_x = radius * math.cos(math.radians(end_angle))
        end_y = radius * math.sin(math.radians(end_angle))

        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        angle = math.atan2(mid_y, mid_x) * (180 / math.pi)

        # Encode angle in the first dimension of Pose
        wall = Wall(size=wall_size, pose=Pose((mid_x, mid_y, 0), (angle, 0, 0)))
        walls.append(wall)

    return walls

def truncate_floats(input_string):
    def truncate(match):
        # Extract the matched float value
        float_value = match.group(0)

        # Truncate after the second digit after the decimal point
        truncated_float = "{:.2f}".format(float(float_value))

        return truncated_float

    # Define a regular expression to match floating-point numbers
    float_pattern = r'\b\d+\.\d+\b'

    # Use re.sub() to replace matched floats with truncated versions
    result_string = re.sub(float_pattern, truncate, input_string)

    return result_string

def calculate_available_space(env_size, walls_type, wall_params):
    if walls_type == 'circular':
        radius = wall_params['radius']
        # Calculate the largest rectangle that fits inside the circle
        side_length = math.sqrt(2) * radius
        min_x = -side_length / 2.0
        max_x = side_length / 2.0
        min_y = -side_length / 2.0
        max_y = side_length / 2.0
    else:
        length = wall_params['rect_length']
        width = wall_params['rect_width']
        min_x = -length / 2.0
        max_x = length / 2.0
        min_y = -width / 2.0
        max_y = width / 2.0

    min_z = 0
    max_z = env_size[2] / 2.0  # other half goes downwards but we do not want to place anything there

    return min_x, max_x, min_y, max_y, min_z, max_z

def generate_wall_params(env_size):
    walls_type = 'circular' if random.random() < 0.5 else 'rectangular'

    if walls_type == 'circular':
        radius = random.uniform(0.2, min(env_size[0] / 2, env_size[1] / 2, 15.0))
        num_walls = random.randint(4, 12)
        wall_params = {'radius': radius, 'num_walls': num_walls}
    else:
        max_wall_length = min(env_size[0], random.uniform(5.0, 15.0))
        max_wall_width = min(env_size[1], random.uniform(5.0, 15.0))
        rect_length = random.uniform(0.2, max_wall_length)
        rect_width = random.uniform(0.2, max_wall_width)
        wall_params = {'rect_length': rect_length, 'rect_width': rect_width}

    return walls_type, wall_params

def sample_describer_missions(dm_modules: list):
    """Get describer and mission params from list of describer-mission modules.
    dm_modules should contain pairs of corresponding modules
    that can be used together. 
    First element is aggregation module, second is description module.

    Example: [(missions.aggregation, descriptions.aggregation)]
    """
    selected_pair = random.choice(dm_modules)
    describer_function = selected_pair[1].sample_describer()

    # Sample parameters based on the selected module
    params = selected_pair[0].sample_params()
    
    get_mission = selected_pair[0].get_mission
    mission_types = selected_pair[0], selected_pair[1]
    # Return both the describer function and the sampled parameters
    return describer_function, get_mission, params, mission_types



def save_mission_dataset(path, dataset: pd.DataFrame):
    required_columns = {"describer", "get_mission", "params_type", "params", "mission_type", "description_type"}
    if not (required_columns.issubset(dataset.columns) and len(dataset.columns) == len(required_columns)):
        logging.error(f"saving mission dataset with invalid data. Required columns (exact): {required_columns}. ")
        exit(1)
    dataset = dataset.copy() # to avoid mutating out of function
    dataset.describer = dataset.describer.map(lambda x: x.__name__)
    dataset.get_mission = dataset.get_mission.map(lambda x: x.__name__)
    dataset.params_type = dataset.params_type.map(lambda x: x.__class__.__name__)
    dataset.params = dataset.params.map(asdict)
    dataset.mission_type = dataset.mission_type.map(lambda x: x.__name__)
    dataset.description_type = dataset.description_type.map(lambda x: x.__name__)
        
    dataset.to_feather(path)

def load_mission_dataset(path):
    df = pd.read_feather(path)
    import_from = lambda row: getattr(row.iloc[1],row.iloc[0])

    def instantiate_dict(row):
            dct = row.iloc[0]
            # to_feather makes dict contain keys that were not originally present
            for k,v  in list(dct.items()):
                if v is None:
                    del dct[k]

            return row.iloc[1](**dct)

    df.mission_type = df.mission_type.map(import_module)
    df.description_type = df.description_type.map(import_module)
    df.describer = df[["describer", "description_type"]].apply(import_from, axis=1)
    df.get_mission = df[["get_mission", "mission_type"]].apply(import_from, axis=1)
    df.params_type = df[["params_type", "mission_type"]].apply(import_from, axis=1)
    df.params = df[["params", "params_type"]].apply(instantiate_dict,axis=1)
    
    return df



from dataclasses import dataclass, field
import random
from swarm_descriptions.utils import generate_wall_params

@dataclass
class AvailableSpace:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float
    max_z: float
    
    def radius(self):
        avs = self
        return min(avs.max_x-avs.min_x, avs.max_y-avs.min_y)/2.0

@dataclass
class BaseParams:
    num_robots: int = 10
    num_lights: int = 10
    env_size: tuple[float, float, float] = (10.0, 10.0, 2.0)
    walls_type: str = 'circular'
    wall_params: dict = field(default_factory=lambda: {
                              'radius': 2.0, 'num_walls': 8})
    
    def sample():
        # Sample number of elements
        num_robots = random.randint(5, 15)
        num_lights = random.randint(0, 3)

        # Sample environment and walls
        env_size = (
            random.uniform(5.0, 15.0),
            random.uniform(5.0, 15.0),
            random.uniform(1.0, 3.0)
        )

        walls_type, wall_params = generate_wall_params(env_size)

        return BaseParams(num_robots, num_lights, env_size, walls_type, wall_params)
    
    def available_space(self):
        min_x, max_x, min_y, max_y, min_z, max_z = calculate_available_space(self.env_size, self.walls_type, self.wall_params)
        logging.debug(f"available space: {(min_x, max_x, min_y, max_y, min_z, max_z)}")
        return AvailableSpace(min_x, max_x, min_y, max_y, min_z, max_z)
    
@dataclass
class BaseMission:
    swarm: Swarm
    env: Environment
    
    def instantiate(params: BaseParams):
        # -- Environment --
        # -- walls
        if params.wall_params is None:
            params.wall_params = {}

        if params.walls_type == 'circular':
            walls = {f"wall_{i}": w for i, w in enumerate(
                generate_circular_walls(**params.wall_params))}
        else:
            walls = {f"wall_{i}": w for i, w in enumerate(
                generate_square_of_walls(**params.wall_params))}
            
            
        # -- lights
        min_x, max_x, min_y, max_y, min_z, max_z = calculate_available_space(params.env_size, params.walls_type, params.wall_params)
        lights = [(
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            0.00,
            random.uniform(2.0, 8.0)
        ) for n in range(params.num_lights)]
        lights = [Light(Pose(light[:3], (360, 0, 0)), light[3]) for light in lights]


        env = Environment(size=params.env_size, walls=walls, lights={
                            f"light_{i}": light for i, light in enumerate(lights)})



        # -- Swarm --
        epuck = Robot(sensors={}, actuators={})
        swarm = Swarm(
            elements={"epuck":  (epuck, params.num_robots)})
        
        return BaseMission(swarm, env)