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
    agg_target: int = 1
    ground_area_1: tuple[tuple[float,float,float], float, str] = ((0.1,0.1,0.1),0.4, "white")
    ground_area_2: tuple[tuple[float,float,float], float, str] = ((0.9,0.9,0.9, 0.2, "black"))
    num_robots: int = 10
    num_lights: int = 10
    env_size: tuple[float, float, float] = (10.0, 10.0, 2.0)
    walls_type: str = 'circular'
    wall_params: dict = field(default_factory=lambda: {
                              'radius': 2.0, 'num_walls': 8})


def sample_params():
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

    min_x, max_x, min_y, max_y, min_z, max_z = calculate_available_space(env_size, walls_type, wall_params)
    
    
    # sample objective
    agg_target = random.randint(1,2)
    c1, c2 = (GroundColor(c).name.lower() for c in random.sample([1,2], 2))
    agr1 = random.uniform(0.5, min((max_x - min_x) / 4, (max_y - min_y) / 4))
    agr2 = random.uniform(0.5, min((max_x - min_x) / 4, (max_y - min_y) / 4))
    ground_area_1 = ((random.uniform(min_x,max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z)), random.uniform(0.05, agr1), c1)
    ground_area_2 = ((random.uniform(min_x,max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z)), random.uniform(0.05, agr2), c2)
    
    logging.debug(f"available space {min_x, max_x}, {min_y, max_y}, {min_z, max_z}")
    
    return AggregationParams(agg_target=agg_target, ground_area_1= ground_area_1, ground_area_2=ground_area_2, env_size=env_size, num_lights=num_lights, num_robots=num_robots, wall_params=wall_params, walls_type=walls_type)
    
def temp():

    # Calculate available space within walls
    min_x, max_x, min_y, max_y, min_z, max_z = calculate_available_space(env_size, walls_type, wall_params)

    # Sample lights within the available space
    num_lights = random.randint(0,5)


def get_mission(params: AggregationParams = AggregationParams()):
    
    # -- Environment --
    # -- walls
    if params.wall_params is None:
        params.wall_params = {}

    if params.walls_type == 'circular':
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_circular_walls(**params.wall_params))}
    else:
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_square_of_walls(**params.wall_params))}
        
        
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
        elements={"epuck":  (epuck, params.num_robots)},
        heading_distribution=Distribution.get_gaussian(
            mean="0,0,0", stdev="360,0,0"),
        pos_distribution=Distribution.get_uniform(min=f"{min_x},{min_y},0", max=f"{max_x},{max_y},0"))

    # -- Objective --
    oc = params.ground_area_1 if params.agg_target == 2 else params.ground_area_2
    grounds = {"ground_1": Ground(params.ground_area_1[0], params.ground_area_1[1], GroundColor[params.ground_area_1[2].upper()]), "ground_2": Ground(params.ground_area_2[0], params.ground_area_2[1], GroundColor[params.ground_area_2[2].upper()])}
    objective = ObjAggregation(radius=oc[1],target_color=oc[2], grounds=grounds)
    # objective = ObjFlocking(density=2.5, velocity=0.2)
    # objective = ObjForaging((0.25,0.25), 0.2, (0.1,0.1), 0.4)
    # objective = ObjDistribution((2.5,7.5), max_connection_distance=0.3)
    # objective = ObjConnection("light_1", "light_2", 0.2)

    mission = Mission(env, swarm, objective)
    return mission
