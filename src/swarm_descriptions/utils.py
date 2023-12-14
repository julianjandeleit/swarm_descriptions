from swarm_descriptions.datamodel import *
import math
import re
import random
import pandas as pd
from importlib import import_module
import logging
from copy import deepcopy
from dataclasses import asdict

def generate_square_of_walls(length, width):
    """
    Generate a square of walls with the specified length and width.

    Parameters:
    - length (float): The length of the square.
    - width (float): The width of the square.

    Returns:
    - list: A list of Wall objects forming a square.
    """
    wall_size = (0.01, length, width)

    # Walls forming a square
    wall_1 = Wall(size=wall_size, pose=Pose((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
    wall_2 = Wall(size=wall_size, pose=Pose(
        (length, 0.0, 0.0), (0.0, 0.0, 90.0)))
    wall_3 = Wall(size=wall_size, pose=Pose(
        (length, width, 0.0), (0.0, 0.0, 180.0)))
    wall_4 = Wall(size=wall_size, pose=Pose(
        (0.0, width, 0.0), (0.0, 0.0, -90.0)))

    # Create a list of walls
    walls = [wall_1, wall_2, wall_3, wall_4]
    return walls


def generate_circular_walls(radius, num_walls, wall_size=(0.01, 0.5, 0.08)):
    """
    Generate a circular arrangement of walls with the specified radius and number of walls.

    Parameters:
    - radius (float): The radius of the circle.
    - num_walls (int): The number of walls in the circular arrangement.

    Returns:
    - list: A list of Wall objects forming a circular arrangement.
    """
    walls = []
    angle_increment = 360.0 / num_walls

    for i in range(num_walls):
        angle = math.radians(i * angle_increment)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        wall_pose = Pose((x, y, 0.0), (0.0, 0.0, math.degrees(angle)))
        walls.append(Wall(size=wall_size, pose=wall_pose))

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