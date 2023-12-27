from dataclasses import dataclass
from typing import Any
from enum import Enum

@dataclass
class Sensor:
    variables: list[str] # variables are the different distinct IRs in an IR array for example
    values: list[str] # the value each variable can take

    def __repr__(self) -> str:
        return f"({self.variables[0]}..{self.variables[-1]}, {self.values[0]}..{self.values[-1]})"

@dataclass
class Actuator:
    variables: list[str]
    values: list[str]
    

    def __repr__(self) -> str:
        return f"({self.variables[0]}..{self.variables[-1]}, {self.values[0]}..{self.values[-1]})"

@dataclass
class Pose:
    position: tuple[float, float, float]
    heading: tuple[float,float,float]
    
@dataclass
class Distribution:
    method: str
    method_params: dict[str, str]
    
    def get_uniform(min: str, max: str):
        """ e.g. min="-1,-1,0", max="1,1,0" """
        return Distribution(method="uniform",method_params={"min": min, "max": max})

    def get_gaussian(mean: str, stdev: str):
        """ e.g. mean="0,0,0", stdev=""360,0,0"" """
        return Distribution(method="gaussian",method_params={"mean": mean, "std_dev": stdev})



@dataclass
class Robot:
    sensors: dict[str,Sensor]
    actuators: dict[str,Actuator]

@dataclass
class Wall:
    size: tuple[float,float,float]
    pose: Pose
    
@dataclass
class Light:
    pose: Pose
    intensity: float = 5.0
   

class GroundColor(Enum):
    BLACK = 1
    WHITE = 2
    
@dataclass
class Ground:
    position: tuple[float, float, float]
    radius: float
    color: GroundColor

@dataclass
class Environment:
    size: tuple[float,float,float]
    lights: dict[str, Light]
    walls: dict[str, Wall]

@dataclass
class Swarm:
    elements: dict[str,(Robot, int)] # maps robot type(id) to list of robots of that type

@dataclass
class ObjectiveFunction:
    type: str
    spawn_radius: float
    grounds: dict[str, Ground] 
    
class ObjAggregation(ObjectiveFunction):

    def __init__(self,radius: float, target_color: str, **kwds):
        super().__init__("aggregation,",**kwds)
        self.radius = radius
        self.target = target_color
    
class ObjFlocking(ObjectiveFunction):
    def __init__(self, density: float, velocity: float, **kwds):
        super().__init__(**kwds)
        self.type = "flocking"
        self.density = density
        self.velocity = velocity
    
class ObjForaging(ObjectiveFunction):
    def __init__(self, black_pos: (float,float,float), black_r: float, white_pos: (float,float,float), white_r: float, **kwds):
        super().__init__(**kwds)
        self.type = "foraging"
        self.black_position = black_pos
        self.black_radius = black_r
        self.white_position = white_pos
        self.white_radius = white_r
    
class ObjDistribution(ObjectiveFunction):
    
    def __init__(self, area: tuple[float,float], max_connection_distance: float, **kwds):
        super().__init__(**kwds)
        self.type = "distribution"
        self.area = area
        self.max_connection_dist = max_connection_distance
    
class ObjConnection(ObjectiveFunction):
    def __init__(self, light1_id: str, light2_id: str, connection_range: float, **kwds):
        super().__init__(**kwds)
        self.type = "connection"
        self.light1 = light1_id
        self.light2 = light2_id
        self.connection_range = connection_range
        

@dataclass
class Mission:
    environment: Environment
    swarm: Swarm
    objective: ObjectiveFunction
    
    def __repr__(self) -> str:
        return f"({list(self.environment.lights.keys())},{list(self.environment.walls.keys())}, {list(self.swarm.elements.keys())}, {self.objective.type})"

