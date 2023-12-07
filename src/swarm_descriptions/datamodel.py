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
class Robot:
    sensors: dict[str,Sensor]
    actuators: dict[str,Actuator]

@dataclass
class EnvElement:
    type: str

@dataclass
class Environment:
    size: tuple[float,float,float]
    center: tuple[float,float,float]
    elements: dict[str,EnvElement]
    positions: dict[str,Pose]
    

@dataclass
class Swarm:
    elements: dict[str,Robot]
    positions: dict[str,Pose]

@dataclass
class ObjectiveFunction:
    type: str

@dataclass
class Mission:
    environment: Environment
    swarm: Swarm
    objective: ObjectiveFunction
    
    def __repr__(self) -> str:
        return f"({list(self.environment.elements.keys())}, {list(self.swarm.elements.keys())}, {self.objective.type})"

