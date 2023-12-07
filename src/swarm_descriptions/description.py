from swarm_descriptions.datamodel import Robot, Environment, Swarm, ObjectiveFunction, Mission
from typing import Protocol
from dataclasses import dataclass

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
    