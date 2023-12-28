from dataclasses import dataclass
from typing import Any, Optional, Tuple
from enum import Enum


@dataclass
class Sensor:
    # variables are the different distinct IRs in an IR array for example
    variables: list[str]
    values: list[str]  # the value each variable can take

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
    heading: tuple[float, float, float]


@dataclass
class Distribution:
    method: str
    method_params: dict[str, str]

    def get_uniform(min: str, max: str):
        """ e.g. min="-1,-1,0", max="1,1,0" """
        return Distribution(method="uniform", method_params={"min": min, "max": max})

    def get_gaussian(mean: str, stdev: str):
        """ e.g. mean="0,0,0", stdev=""360,0,0"" """
        return Distribution(method="gaussian", method_params={"mean": mean, "std_dev": stdev})


@dataclass
class Robot:
    sensors: dict[str, Sensor]
    actuators: dict[str, Actuator]


@dataclass
class Wall:
    size: tuple[float, float, float]
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
    size: tuple[float, float, float]
    lights: dict[str, Light]
    walls: dict[str, Wall]


@dataclass
class RobotSwarm:  # helper class, simpler version of swarm
    num_robots: int
    radius: float
    center: Tuple[float, float]

    def to_swarm(self):
        epuck = Robot(sensors={}, actuators={})
        swarm = Swarm(
            elements={"epuck":  (epuck, self.num_robots)})
        return swarm


@dataclass
class Swarm:
    # maps robot type(id) to list of robots of that type
    elements: dict[str, (Robot, int)]


@dataclass
class ObjectiveFunction:
    type: str
    grounds: dict[str, Ground]
    # spawn_radius: Optional[float]


class ObjAggregation(ObjectiveFunction):

    def __init__(self, radius: float, target_color: str, **kwds):
        super().__init__("aggregation", **kwds)
        self.radius = radius
        self.target = target_color


class ObjConnection(ObjectiveFunction):
    def __init__(self, conn_start: str, conn_end: str, connection_range: float, **kwds):
        super().__init__("connection", **kwds)
        self.conn_start = conn_start
        self.conn_end = conn_end
        self.connection_range = connection_range


class ObjDistribution(ObjectiveFunction):

    def __init__(self, area: tuple[float, float], max_connection_distance: float, **kwds):
        super().__init__(type="distribution", grounds=dict(),**kwds)
        self.area = area
        self.max_connection_dist = max_connection_distance


class ObjForaging(ObjectiveFunction):
    def __init__(self, start: str, end: str, grounds: dict[str, Ground], **kwds):
        super().__init__(type="foraging", grounds=grounds, **kwds)
        self.start_area = start
        self.target_area = end


@dataclass
class Mission:
    environment: Environment
    swarm: Swarm
    objective: ObjectiveFunction

    def __repr__(self) -> str:
        return f"({list(self.environment.lights.keys())},{list(self.environment.walls.keys())}, {list(self.swarm.elements.keys())}, {self.objective.type})"
