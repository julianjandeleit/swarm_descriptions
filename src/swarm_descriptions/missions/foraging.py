from swarm_descriptions.datamodel import *
from swarm_descriptions import utils
import random

from dataclasses import dataclass, field


@dataclass
class ForagingParams:
    black_pos: tuple[float, float, float] = (0.4, 0.4, 0.0)
    white_pos: tuple[float, float, float] = (0.1, 0.3, 0.0)
    black_radius: float = 0.5
    white_radius: float = 0.2
    flocking_density: float = 1.2
    flocking_velocity: float = 0.2
    light_1: tuple[float, float, float] = (0.5, 0.2, 0.0)
    light_2: tuple[float, float, float] = (-0.5, 0.75, 0.0)
    num_robots: int = 10
    env_size: tuple[float, float, float] = (10.0, 10.0, 2.0)
    walls_type: str = 'circular'
    wall_params: dict = field(default_factory=lambda: {
                              'radius': 2.0, 'num_walls': 8})


def sample_params():
    # Sample lights and number of robots
    light_1 = (random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0), 0.0)
    light_2 = (random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0), 0.0)
    num_robots = random.randint(5, 15)

    # Determine maximum wall size for arena
    max_wall_size = max(random.uniform(5.0, 15.0), random.uniform(5.0, 15.0))

    # Sample environment size
    env_size = (
        max(2 * max_wall_size, random.uniform(5.0, 15.0)),
        max(2 * max_wall_size, random.uniform(5.0, 15.0)),
        random.uniform(1.0, 3.0)
    )

    # Randomly choose between circular and square walls
    walls_type = 'circular' if random.random() < 0.5 else 'rectangular'

    # Sample wall parameters
    if walls_type == 'circular':
        wall_params = {'radius': max_wall_size,
                       'num_walls': random.randint(4, 12)}
    else:
        wall_params = {'rect_length': random.uniform(0.2, max_wall_size),
                       'rect_width': random.uniform(0.2, max_wall_size)}

    # Ensure that black and white areas fit inside the arena and walls
    black_radius = random.uniform(0.2, min(env_size[0] / 2, env_size[1] / 2, max_wall_size / 2))
    white_radius = random.uniform(0.1, black_radius)

    # Sample positions for black and white areas
    black_pos = (
        random.uniform(-env_size[0] / 2 + black_radius, env_size[0] / 2 - black_radius),
        random.uniform(-env_size[1] / 2 + black_radius, env_size[1] / 2 - black_radius),
        0.0
    )

    white_pos = (
        random.uniform(-env_size[0] / 2 + white_radius, env_size[0] / 2 - white_radius),
        random.uniform(-env_size[1] / 2 + white_radius, env_size[1] / 2 - white_radius),
        0.0
    )

    return ForagingParams(
        black_pos=black_pos,
        black_radius=black_radius,
        white_pos=white_pos,
        white_radius=white_radius,
        light_1=light_1,
        light_2=light_2,
        num_robots=num_robots,
        env_size=env_size,
        walls_type=walls_type,
        wall_params=wall_params
    )


def get_mission(params: ForagingParams = ForagingParams()):
    epuck = Robot(sensors={}, actuators={})

    if params.wall_params is None:
        params.wall_params = {}

    if params.walls_type == 'circular':
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_circular_walls(**params.wall_params))}
    else:
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_square_of_walls(**params.wall_params))}

    light_1 = Light(Pose(params.light_1, (360, 0, 0)))
    light_2 = Light(Pose(params.light_2, (360, 0, 0)))

    env = Environment(size=params.env_size, walls=walls, lights={
                      "light_1": light_1, "light_2": light_2})

    swarm = Swarm(
        elements={"epuck":  (epuck, params.num_robots)},
        heading_distribution=Distribution.get_gaussian(
            mean="0,0,0", stdev="360,0,0"),
        pos_distribution=Distribution.get_uniform(min="-1,-1,0", max="1,1,0"))

    objective = ObjForaging(params.black_pos, params.black_radius, params.white_pos, params.white_radius)
    # objective = ObjDistribution((2.5,7.5), max_connection_distance=0.3)
    # objective = ObjConnection("light_1", "light_2", 0.2)

    mission = Mission(env, swarm, objective)
    return mission
