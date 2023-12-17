from swarm_descriptions.datamodel import *
from swarm_descriptions import utils
import random
import math
import logging
from dataclasses import dataclass, field
from swarm_descriptions.utils import generate_wall_params
from swarm_descriptions.utils import calculate_available_space


@dataclass
class AggregationParams:
    agg_radius: float = 1.2
    light_1: tuple[float, float, float] = (0.5, 0.2, 0.0)
    light_2: tuple[float, float, float] = (-0.5, 0.75, 0.0)
    num_robots: int = 10
    robot_dist_min: tuple[float,float,float] = (-1.0,-1.0,0.0)
    robot_dist_max: tuple[float,float,float] = (1.0,1.0,0.0)
    env_size: tuple[float, float, float] = (10.0, 10.0, 2.0)
    walls_type: str = 'circular'
    wall_params: dict = field(default_factory=lambda: {
                              'radius': 2.0, 'num_walls': 8})


def sample_params():
    # Sample number of robots
    num_robots = random.randint(5, 15)

    # Sample environment size
    env_size = (
        random.uniform(5.0, 15.0),
        random.uniform(5.0, 15.0),
        random.uniform(1.0, 3.0)
    )

    # Generate wall parameters
    walls_type, wall_params = generate_wall_params(env_size)

    # Calculate available space within walls
    min_x, max_x, min_y, max_y, min_z, max_z = calculate_available_space(env_size, walls_type, wall_params)

    # Sample lights within the available space
    light_1 = (
        random.uniform(min_x, max_x),
        random.uniform(min_y, max_y),
        random.uniform(min_z, max_z)
    )
    light_2 = (
        random.uniform(min_x, max_x),
        random.uniform(min_y, max_y),
        random.uniform(min_z, max_z)
    )
    
    logging.debug(f"available space {min_x, max_x}, {min_y, max_y}, {min_z, max_z}")
    logging.debug(f"lights {light_1}, {light_2}")

    # Sample aggregation radius within the constraint
    agg_radius = random.uniform(0.5, min((max_x - min_x) / 4, (max_y - min_y) / 4))

    return AggregationParams(
        agg_radius=agg_radius,
        light_1=light_1,
        light_2=light_2,
        num_robots=num_robots,
        robot_dist_min=(min_x, min_y, 0.0),
        robot_dist_max=(max_x, max_y, 0.0),
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


    logging.debug(f"{params.robot_dist_min} {params.robot_dist_max},{params.robot_dist_min}, {params.robot_dist_max}")
    swarm = Swarm(
        elements={"epuck":  (epuck, params.num_robots)},
        heading_distribution=Distribution.get_gaussian(
            mean="0,0,0", stdev="360,0,0"),
        pos_distribution=Distribution.get_uniform(min=f"{params.robot_dist_min[0]},{params.robot_dist_min[1]},{params.robot_dist_min[2]}", max=f"{params.robot_dist_max[0]},{params.robot_dist_max[1]},{params.robot_dist_max[2]}"))

    objective = ObjAggregation(params.agg_radius, "light_1")
    # objective = ObjFlocking(density=2.5, velocity=0.2)
    # objective = ObjForaging((0.25,0.25), 0.2, (0.1,0.1), 0.4)
    # objective = ObjDistribution((2.5,7.5), max_connection_distance=0.3)
    # objective = ObjConnection("light_1", "light_2", 0.2)

    mission = Mission(env, swarm, objective)
    return mission
