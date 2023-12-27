from swarm_descriptions.datamodel import *
from swarm_descriptions import utils
import random

from dataclasses import dataclass, field

from swarm_descriptions.utils import BaseMission, BaseParams


@dataclass
class ConnectionParams:
    conn_start: str = "white"
    conn_end: str = "black"
    conn_range: float = 0.2
    ground_area_1: tuple[tuple[float,float,float], float, str] = ((0.1,0.1,0.1),0.4, "white")
    ground_area_2: tuple[tuple[float,float,float], float, str] = ((0.9,0.9,0.9, 0.2, "black"))
    base_params: BaseParams = BaseParams.sample()


def sample_params():
    base_params = BaseParams.sample()
    avs = base_params.available_space()
    
    # sample objective
    conn_start, conn_end = random.sample([1,2], 2)
    c1, c2 = (GroundColor(c).name.lower() for c in random.sample([1,2], 2))
    agr1 = random.uniform(0.5, min((avs.max_x - avs.min_x) / 4, (avs.max_y - avs.min_y) / 4))
    agr2 = random.uniform(0.5, min((avs.max_x - avs.min_x) / 4, (avs.max_y - avs.min_y) / 4))
    ground_area_1 = ((random.uniform(avs.min_x,avs.max_x), random.uniform(avs.min_y, avs.max_y), random.uniform(avs.min_z, avs.max_z)), random.uniform(0.05, agr1), c1)
    ground_area_2 = ((random.uniform(avs.min_x,avs.max_x), random.uniform(avs.min_y, avs.max_y), random.uniform(avs.min_z, avs.max_z)), random.uniform(0.05, agr2), c2)
        
    # Sample connection range within a reasonable range
    distr_conn_range = random.uniform(0.05, 0.25)
    

    return ConnectionParams(
        conn_start=conn_start,
        conn_end=conn_end,
        conn_range=distr_conn_range,
        ground_area_1=ground_area_1,
        ground_area_2=ground_area_2,
        base_params=base_params
    )


def get_mission(params: ConnectionParams = ConnectionParams()):
   
    avs = params.base_params.available_space()
    base_mission = BaseMission.instantiate(params.base_params)
   
    # -- Objective --
    grounds = {"ground_1": Ground(params.ground_area_1[0], params.ground_area_1[1], GroundColor[params.ground_area_1[2].upper()]), "ground_2": Ground(params.ground_area_2[0], params.ground_area_2[1], GroundColor[params.ground_area_2[2].upper()])}
    objective = ObjConnection(GroundColor(params.conn_start).name.lower(),GroundColor(params.conn_end).name.lower(), params.conn_range, grounds=grounds, spawn_radius=min(avs.max_x-avs.min_x, avs.max_y-avs.min_y)/2.0)

    mission = Mission(base_mission.env, base_mission.swarm, objective)
    return mission
