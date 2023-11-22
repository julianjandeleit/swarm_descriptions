from dataclasses import dataclass
import numpy as np
import logging

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

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    proximity = Sensor(
        variables=["prox0","prox1","prox2","prox3","prox4","prox5","prox6","prox7"],
        values=[str(v) for v in np.linspace(0,1,num=100)])
    
    light = Sensor(
        variables=[f"light{i}" for i in range(7)],
        values=[str(v) for v in np.linspace(0,1,num=100)])
    
    ground = Sensor(
        variables=[f"ground{i}" for i in range(3)],
        values=["black", "gray", "white"]
    )
    
    wheels = Actuator(
        variables=["vl", "vr"],
        values=[str(v) for v in np.linspace(-0.12,0.12,num=100)]
    )
    
    epuck = Robot(
        sensors={
            "proximity": proximity,
            "light": light,
            "ground": ground,
        },
        actuators={
            "wheels": wheels
        })
    
    logging.debug(epuck)
    
    
    obstacle = EnvElement(type="obstacle")
    
    env = Environment(size=(10.0,10.0,2.0), center=(0.0,0.0,0.0),
                      elements={"obs1": obstacle}, positions={"obs1": Pose((1.0,1.0,0.0), (0.0,0.0,0.0))})
    
    
    swarm = Swarm(elements={"r1": epuck, "r2": epuck}, positions={
        "r1": Pose((1.0,0.0,0.0),(0.0,0.0,0.0)),
        "r2": Pose((0.0,1.0,0.0),(0.0,0.0,0.0))
    })
    
    objective = ObjectiveFunction("aggregation")
    
    mission = Mission(env, swarm, objective)
    
    logging.debug(mission)
    