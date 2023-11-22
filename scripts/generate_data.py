from dataclasses import dataclass
import numpy as np
import logging
from typing import Any, Callable, Protocol
from abc import ABC, abstractmethod

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

class RobotDescriber(Protocol):
    def __call__(self, robot: Robot) -> str: pass

class EnvironmentDescriber(Protocol):
    def __call__(self, environment: Environment) -> str: pass
    
class SwarmDescriber(Protocol):
    def __call__(self, swarm: Swarm, rob_desc: RobotDescriber) -> str: pass
    
class ObjectiveDescriber(Protocol):
    def __call__(self, obj: ObjectiveFunction) -> str: pass

class MissionDescriber(Protocol):
    def __call__(self,mission: Mission,env_desc: EnvironmentDescriber, swarm_desc: SwarmDescriber, obj_desc: ObjectiveDescriber, rob_desc: RobotDescriber) -> str: pass
    
@dataclass
class Describer:
    robot_describer: RobotDescriber
    environment_describer: EnvironmentDescriber
    swarm_describer: SwarmDescriber
    objective_describer: ObjectiveDescriber
    mission_describer: MissionDescriber
    
    def describe(self, mission: Mission) -> str:
        return self.mission_describer(mission, self.environment_describer, self.swarm_describer, self.objective_describer, self.robot_describer)
    
    
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
    
    def mission_describer_1(mission: Mission,env_desc: EnvironmentDescriber, swarm_desc: SwarmDescriber, obj_desc: ObjectiveDescriber, rob_desc: RobotDescriber) -> str:
        s1 = "We define a mission in the following way: "
        s2 = env_desc(mission.environment)
        s3 = swarm_desc(mission.swarm, rob_desc)
        s4 = obj_desc(mission.objective)
        
        return s1+s2+s3+s4
    
    def objective_describer_1(obj: ObjectiveFunction) -> str:
        s1 = f"The objective of the robots is to perform the behavior {obj.type}."
        
        return s1
    
    def swarm_describer_1(swarm: Swarm, rob_desc: RobotDescriber) -> str:
        s1 = "The swarm consists of the following robots:"
        robs = []
        for rob in swarm.elements.keys():
            r = rob_desc(swarm.elements[rob])
            robs.append(f"A robot called {rob}. {r}")
            
        robs = " ".join(robs)
        
        positions = []
        for rob in swarm.elements.keys():
            r1 = f"The robot {rob} is located at {swarm.positions[rob].position} and rotated by {swarm.positions[rob].heading}."
            positions.append(r1)
            
        positions = " ".join(positions)
        
        return s1 + robs + positions
    
    def robot_describer_1(robot: Robot) -> str:
        s1 = "The robot has the following actuators."
        actuators = []
        for act in robot.actuators.keys():
            actuators.append(f"Actuator {act} that has the form {robot.actuators[act]}.")
            
        sensors = []
        for sen in robot.sensors.keys():
            sensors.append(f"Sensor {sen}, of the form {robot.sensors[sen]}.")
            
        actuators = " ".join(actuators)
        sensors = " ".join(sensors)
        
        return s1 + actuators + sensors
    
    def environment_describer_1( environment: Environment) -> str:
        s1 = f"The environment is centered at {environment.center} and has the dimensions {environment.size}."
        s2 = f"It consists of the following elements:"
        elems = []
        for e in environment.elements.keys():
            elems.append(f"An element {e} of type {environment.elements[e].type} located at {(environment.positions[e].position,environment.positions[e].heading)}.")
            
        elems = " ".join(elems)
        
        return s1+s2+elems
    
    md : MissionDescriber = mission_describer_1
    od: ObjectiveDescriber = objective_describer_1
    sd: SwarmDescriber = swarm_describer_1
    rd: RobotDescriber = robot_describer_1
    ed: EnvironmentDescriber = environment_describer_1
    
    describer = Describer(rd, ed, sd, od, md)
    
    description = describer.describe(mission)
    logging.info(description)