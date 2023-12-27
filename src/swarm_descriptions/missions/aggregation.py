from swarm_descriptions.datamodel import *
from swarm_descriptions import utils
import random
import math
import logging
from dataclasses import dataclass, field
from swarm_descriptions.utils import BaseMission, BaseParams
from swarm_descriptions.utils import generate_wall_params
from swarm_descriptions.utils import calculate_available_space


@dataclass
class AggregationParams:
    agg_target: int = 1
    ground_area_1: tuple[tuple[float,float,float], float, str] = ((0.1,0.1,0.1),0.4, "white")
    ground_area_2: tuple[tuple[float,float,float], float, str] = ((0.9,0.9,0.9, 0.2, "black"))
    base_params: BaseParams = BaseParams.sample()


def sample_params():
    base_params = BaseParams.sample()
    min_x, max_x, min_y, max_y, min_z, max_z = utils.calculate_available_space(base_params.env_size, base_params.walls_type, base_params.wall_params)
    
    
    # sample objective
    agg_target = random.randint(1,2)
    c1, c2 = (GroundColor(c).name.lower() for c in random.sample([1,2], 2))
    agr1 = random.uniform(0.5, min((max_x - min_x) / 4, (max_y - min_y) / 4))
    agr2 = random.uniform(0.5, min((max_x - min_x) / 4, (max_y - min_y) / 4))
    ground_area_1 = ((random.uniform(min_x,max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z)), random.uniform(0.05, agr1), c1)
    ground_area_2 = ((random.uniform(min_x,max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z)), random.uniform(0.05, agr2), c2)
    
    logging.debug(f"available space {min_x, max_x}, {min_y, max_y}, {min_z, max_z}")
    
    return AggregationParams(agg_target=agg_target, ground_area_1= ground_area_1, ground_area_2=ground_area_2, base_params=base_params)

def get_mission(params: AggregationParams = AggregationParams()):

    base_mission = BaseMission.instantiate(params.base_params)
    avs = params.base_params.available_space()

    # -- Objective --
    oc = params.ground_area_1 if params.agg_target == 2 else params.ground_area_2
    grounds = {"ground_1": Ground(params.ground_area_1[0], params.ground_area_1[1], GroundColor[params.ground_area_1[2].upper()]), "ground_2": Ground(params.ground_area_2[0], params.ground_area_2[1], GroundColor[params.ground_area_2[2].upper()])}
    objective = ObjAggregation(radius=oc[1],target_color=oc[2], grounds=grounds, spawn_radius=avs.radius()) # width of robot

    mission = Mission(base_mission.env, base_mission.swarm, objective)
    return mission
