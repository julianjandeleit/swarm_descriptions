from swarm_descriptions.missions.connection import ConnectionParams
from swarm_descriptions import utils
import random


def sample_describer():
    return random.choice([describer_1, describer_2, describer_3])


def describer_1(params: ConnectionParams):
    desc = f"The mission of the swarm is connection. It takes place inside an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"Inside of the environment are walls in a rectangular shape. The walls form a rectangle of size {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Inside of the environment are walls in a circular shape. The walls form a circle with radius {params.wall_params['radius']} made out of {params.wall_params['num_walls']} walls. "
    desc += f" Additionally, there are two lights inside of the environment. The first light is placed at {params.light_1}. The second light is placed at {(params.light_2)}. The swarm consists of {params.num_robots} robots. The objective of this mission is to connect {params.conn_start} with {params.conn_end} by forming a line of robots between those. Robots should not be too close in order to be a proper line. Robots are to close if their distance is below {params.conn_range}. "
    return utils.truncate_floats(desc)


def describer_2(params: ConnectionParams):
    desc = f"The swarm is performing a mission of connection in an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"The environment is enclosed by rectangular walls measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"The environment is surrounded by a circular wall with a radius of {params.wall_params['radius']}. The wall is composed of {params.wall_params['num_walls']} segments. "
    desc += f"There are lights in the environment. light_1 is positioned at {params.light_1}, and light_2 is located at {params.light_2}. The swarm comprises {params.num_robots} robots. The objective of this connection mission is to connect the first light with the second light by forming a line. Robots should keep a distance of {params.conn_range} to each other. "
    return utils.truncate_floats(desc)


def describer_3(params: ConnectionParams):
    desc = f"A cohesive swarm, comprised of {params.num_robots} robots, undertakes a connection mission within a {params.env_size} environment. "
    if params.walls_type == "rectangular":
        desc += f"The boundaries of this space are defined by rectangular walls, creating an enclosure measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Enveloping the area is a circular wall, meticulously crafted with a radius of {params.wall_params['radius']} and composed of {params.wall_params['num_walls']} segments. "
    desc += f"Within this setting, there are two lights. Light_1 at {params.light_1} and Light_2 at {params.light_2}. The swarm should connect {params.conn_start} with {params.conn_end}. Individual robots shoul be {params.conn_range} m apart. "
    return utils.truncate_floats(desc)