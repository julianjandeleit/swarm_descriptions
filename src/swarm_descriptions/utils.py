from swarm_descriptions.datamodel import *
import math
import re
import random


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
