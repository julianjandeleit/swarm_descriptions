from swarm_descriptions.datamodel import *
from swarm_descriptions.recursive_describer import *


def mission_describer_1(mission: Mission, env_desc: EnvironmentDescriber, swarm_desc: SwarmDescriber, obj_desc: ObjectiveDescriber, rob_desc: RobotDescriber) -> str:
    s1 = "We define a mission in the following way: "
    s2 = env_desc(mission.environment)
    s3 = swarm_desc(mission.swarm, rob_desc)
    s4 = obj_desc(mission.objective)

    return s1+s2+s3+s4


def objective_describer_1(obj: ObjectiveFunction) -> str:
    s1 = f"The objective of the robots is to perform the behavior '{obj.type}': "

    s2 = ""
    if isinstance(obj, ObjAggregation):
        s2 = f"The robots should aggregate at light {obj.light} within a radius of {obj.radius}m. "

    if isinstance(obj, ObjFlocking):
        s2 = f"The robots should move together in a coordinated way with velocity {obj.velocity} m/s and a density of {obj.density} robots per m². "

    if isinstance(obj, ObjForaging):
        s2 = f"The robots should bring objects from the black area located at {obj.black_position} to the white area located at {obj.white_position}. The white area has a radius of {obj.white_radius}. The black area has a radius of {obj.black_radius}. "

    if isinstance(obj, ObjDistribution):
        s2 = f"The robots should cover an area of dimensions {obj.area} while staying connected to each other. Two robots count as connected, when their distance is not larger than {obj.max_connection_dist}m . "

    if isinstance(obj, ObjConnection):
        s2 = f"The robots should connect light '{obj.light1}' with light '{obj.light2}' by forming a line between the lights. The robots should not be clustered. This would not form a line. Their pairwise distance should not be below the connection range {obj.connection_range}m. "
    return s1 + s2


def swarm_describer_1(swarm: Swarm, rob_desc: RobotDescriber) -> str:
    s1 = "The swarm consists of the following robots:"
    robs = []
    for id, (rob, num) in swarm.elements.items():
        r = rob_desc(swarm.elements[id][0])
        robs.append(
            f"{num} robots of type {id}. {id} robots are built the following way: {r}")

    robs = " ".join(robs)

    r1 = f"The robots are distributed inside the area with a {swarm.pos_distribution.method} distribution with the parameters {swarm.pos_distribution.method_params}."
    r2 = f" Their orientations are distributed with {swarm.heading_distribution} with {swarm.heading_distribution.method_params}."

    return s1 + robs + r1 + r2


def robot_describer_1(robot: Robot) -> str:
    s1 = "The robot has the following actuators."
    actuators = []
    for act in robot.actuators.keys():
        actuators.append(
            f"Actuator {act} that has the form {robot.actuators[act]}.")

    sensors = []
    for sen in robot.sensors.keys():
        sensors.append(f"Sensor {sen}, of the form {robot.sensors[sen]}.")

    actuators = " ".join(actuators)
    sensors = " ".join(sensors)

    return s1 + actuators + sensors


def environment_describer_1(environment: Environment) -> str:
    s1 = f"The environment has the dimensions {environment.size}."
    s2 = f"It consists of the following elements:"
    elems = []
    for e in environment.lights.keys():
        elems.append(
            f"An light {e} located at {environment.lights[e].pose.position} with the orientation {environment.lights[e].pose.heading}.")

    elems = " ".join(elems)

    return s1+s2+elems


def get_describer():
    md: MissionDescriber = mission_describer_1
    od: ObjectiveDescriber = objective_describer_1
    sd: SwarmDescriber = swarm_describer_1
    rd: RobotDescriber = robot_describer_1
    ed: EnvironmentDescriber = environment_describer_1

    describer = Describer(rd, ed, sd, od, md)
    return describer
