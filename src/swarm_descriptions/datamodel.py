from dataclasses import dataclass

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

@dataclass
class Environment:
    size: tuple[float,float,float]
    lights: dict[str, Light]
    walls: dict[str, Wall] 

@dataclass
class Swarm:
    elements: dict[str,(Robot, int)] # maps robot type(id) to list of robots of that type
    pos_distribution: Distribution
    heading_distribution: Distribution

@dataclass
class ObjectiveFunction:
    type: str

@dataclass
class Mission:
    environment: Environment
    swarm: Swarm
    objective: ObjectiveFunction
    
    def __repr__(self) -> str:
        return f"({list(self.environment.lights.keys())},{list(self.environment.walls.keys())}, {list(self.swarm.elements.keys())}, {self.objective.type})"

