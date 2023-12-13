from swarm_descriptions.missions.flocking import FlockingParams
from swarm_descriptions import utils
import random


def sample_describer():
    return random.choice([describer_1, describer_2, describer_3])


def describer_1(params: FlockingParams):
    desc = f"The mission of the swarm is flocking. It takes place inside an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"Inside of the environment are walls in a rectangular shape. The walls form a rectangle of size {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Inside of the environment are walls in a circular shape. The walls form a circle with radius {params.wall_params['radius']} made out of {params.wall_params['num_walls']} walls. "
    desc += f" Additionally, there are two lights inside of the environment. The first light is placed at {params.light_1}. The second light is placed at {(params.light_2)}. The swarm consists of {params.num_robots} robots. The objective of this coordinated motion mission is to move into the same direction with velocity {params.flocking_velocity} m/s while keeping a density of {params.flocking_density} robots per m². "
    return utils.truncate_floats(desc)


def describer_2(params: FlockingParams):
    desc = f"The swarm is performing a mission of coordinated motion in an environment of size {params.env_size}. "
    if params.walls_type == "rectangular":
        desc += f"The environment is enclosed by rectangular walls measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"The environment is surrounded by a circular wall with a radius of {params.wall_params['radius']}. The wall is composed of {params.wall_params['num_walls']} segments. "
    desc += f"There are lights in the environment. light_1 is positioned at {params.light_1}, and light_2 is located at {params.light_2}. The swarm comprises {params.num_robots} robots. The mission objective of the robots is to flock together with {params.flocking_density} robots in every square meter and move together into a common direction with {params.flocking_velocity} meters per second. "
    return utils.truncate_floats(desc)


def describer_3(params: FlockingParams):
    desc = f"A cohesive swarm, comprised of {params.num_robots} robots, undertakes an coordinated motion mission within a {params.env_size} environment. "
    if params.walls_type == "rectangular":
        desc += f"The boundaries of this space are defined by rectangular walls, creating an enclosure measuring {params.wall_params['length']} by {params.wall_params['width']}. "
    elif params.walls_type == "circular":
        desc += f"Enveloping the area is a circular wall, meticulously crafted with a radius of {params.wall_params['radius']} and composed of {params.wall_params['num_walls']} segments. "
    desc += f"Within this setting, two lights illuminate the area: Light_1 at {params.light_1} and Light_2 at {params.light_2}. The swarm should move together with a velocity {params.flocking_velocity} while maintaining robot distances so that there are {params.flocking_density} robots each m². "
    return utils.truncate_floats(desc)
