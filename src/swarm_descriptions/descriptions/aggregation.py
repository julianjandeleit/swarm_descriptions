from swarm_descriptions.missions.aggregation import AggregationParams
from swarm_descriptions import utils
import random


def sample_describer():
    return random.choice([describer_1, describer_2, describer_3])


def describer_1(params: AggregationParams):
    desc = f"The mission of the swarm is aggregation. It takes place inside an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"Inside of the environment are walls in a rectangular shape. The walls form a rectangle of size {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Inside of the environment are walls in a circular shape. The walls form a circle with radius {params.wall_params['radius']} made out of {params.wall_params['num_walls']} walls. "
    desc += f" Additionally, there are two lights inside of the environment. light_1 is placed at {params.light_1}. The second light is placed at {(params.light_2)}. The swarm consists of {params.num_robots} robots. The objective of this aggregation mission is to meet within a range of {params.agg_radius} of the first light."
    return utils.truncate_floats(desc)


def describer_2(params: AggregationParams):
    desc = f"The swarm is on an aggregation mission in an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"The environment is enclosed by rectangular walls measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"The environment is surrounded by a circular wall with a radius of {params.wall_params['radius']}. The wall is composed of {params.wall_params['num_walls']} segments. "
    desc += f"There are two lights within the environment. Light_1 is positioned at {params.light_1}, and Light_2 is located at {params.light_2}. The swarm comprises {params.num_robots} robots. The mission objective is aggregation, with the goal of gathering within a range of {params.agg_radius} of Light_1."
    return utils.truncate_floats(desc)


def describer_3(params: AggregationParams):
    desc = f"A cohesive swarm, comprised of {params.num_robots} robots, undertakes an aggregation mission within a {params.env_size} environment. "
    if params.walls_type == "rectangular":
        desc += f"The boundaries of this space are defined by rectangular walls, creating an enclosure measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Enveloping the area is a circular wall, meticulously crafted with a radius of {params.wall_params['radius']} and composed of {params.wall_params['num_walls']} segments. "
    desc += f"Within this setting, two lights illuminate the surroundings: Light_1 at {params.light_1} and Light_2 at {params.light_2}. The mission unfolds with the objective of aggregating within a range of {params.agg_radius} around Light_1."
    return utils.truncate_floats(desc)
