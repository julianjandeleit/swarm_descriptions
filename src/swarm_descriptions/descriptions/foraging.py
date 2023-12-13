from swarm_descriptions.missions.foraging import ForagingParams
from swarm_descriptions import utils
import random


def sample_describer():
    return random.choice([describer_1, describer_2, describer_3])


def describer_1(params: ForagingParams):
    desc = f"The mission of the swarm is foraging. It takes place inside an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"Inside of the environment are walls in a rectangular shape. The walls form a rectangle of size {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Inside of the environment are walls in a circular shape. The walls form a circle with radius {params.wall_params['radius']} made out of {params.wall_params['num_walls']} walls. "
    desc += f" Additionally, there are two lights inside of the environment. The first light is placed at {params.light_1}. The second light is placed at {(params.light_2)}. The swarm consists of {params.num_robots} robots. The objective of this foraging mission is to bring items from the white area to the black area. Both areas are a circle. The white area has a radius of {params.white_radius} and is placed at {params.white_pos}. The black area has a radius of {params.black_radius}. It is placed at {params.black_pos}. "
    return utils.truncate_floats(desc)


def describer_2(params: ForagingParams):
    desc = f"The swarm is performing a mission of item foraging in an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"The environment is enclosed by rectangular walls measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"The environment is surrounded by a circular wall with a radius of {params.wall_params['radius']}. The wall is composed of {params.wall_params['num_walls']} segments. "
    desc += f"There are lights in the environment. light_1 is positioned at {params.light_1}, and light_2 is located at {params.light_2}. The swarm comprises {params.num_robots} robots. The mission objective of the robots is to collect items from the white area located at {params.white_pos} and bring them to the black area at {params.black_pos}. The white area is a circle with radius {params.white_radius} and the black area a circle with radius {params.black_radius}. "
    return utils.truncate_floats(desc)


def describer_3(params: ForagingParams):
    desc = f"A cohesive swarm, comprised of {params.num_robots} robots, undertakes foraging mission within a {params.env_size} environment. "
    if params.walls_type == "rectangular":
        desc += f"The boundaries of this space are defined by rectangular walls, creating an enclosure measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Enveloping the area is a circular wall, meticulously crafted with a radius of {params.wall_params['radius']} and composed of {params.wall_params['num_walls']} segments. "
    desc += f"Within this setting, two lights illuminate the area: Light_1 at {params.light_1} and Light_2 at {params.light_2}. The swarm should collect items from {params.white_pos} to {params.black_pos}. The items can be collected within a radius of {params.white_radius} from the first position. There the ground is white. The target area where the robots should bring the items is marked black and has a radius of {params.black_radius}. "
    return utils.truncate_floats(desc)