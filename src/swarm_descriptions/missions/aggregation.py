from swarm_descriptions.datamodel import *
from swarm_descriptions import utils
import random

from dataclasses import dataclass, field


@dataclass
class AggregationParams:
    agg_radius: float = 1.2
    light_1: tuple[float, float, float] = (0.5, 0.2, 0.0)
    light_2: tuple[float, float, float] = (-0.5, 0.75, 0.0)
    num_robots: int = 10
    env_size: tuple[float, float, float] = (10.0, 10.0, 2.0)
    walls_type: str = 'circular'
    wall_params: dict = field(default_factory=lambda: {
                              'radius': 2.0, 'num_walls': 8})


def sample_params():
    agg_radius = random.uniform(1.0, 2.0)
    light_1 = (random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0), 0.0)
    light_2 = (random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0), 0.0)
    num_robots = random.randint(5, 15)

    max_wall_size = max(random.uniform(5.0, 15.0), random.uniform(5.0, 15.0))

    env_size = (
        max(2 * max_wall_size, random.uniform(5.0, 15.0)),
        max(2 * max_wall_size, random.uniform(5.0, 15.0)),
        random.uniform(1.0, 3.0)
    )

    # Randomly choose between circular and square walls
    walls_type = 'circular' if random.random() < 0.5 else 'rectangular'

    if walls_type == 'circular':
        wall_params = {'radius': max_wall_size,
                       'num_walls': random.randint(4, 12)}
    else:
        wall_params = {'length': max_wall_size, 'width': max_wall_size}

    return AggregationParams(
        agg_radius=agg_radius,
        light_1=light_1,
        light_2=light_2,
        num_robots=num_robots,
        env_size=env_size,
        walls_type=walls_type,
        wall_params=wall_params
    )


def get_mission(params: AggregationParams = AggregationParams()):
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

    objective = ObjAggregation(params.agg_radius, "light_1")
    # objective = ObjFlocking(density=2.5, velocity=0.2)
    # objective = ObjForaging((0.25,0.25), 0.2, (0.1,0.1), 0.4)
    # objective = ObjDistribution((2.5,7.5), max_connection_distance=0.3)
    # objective = ObjConnection("light_1", "light_2", 0.2)

    mission = Mission(env, swarm, objective)
    return mission
