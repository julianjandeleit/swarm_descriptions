import numpy as np
import logging
from swarm_descriptions.datamodel import *
from swarm_descriptions.description import *
from swarm_descriptions.configfiles import *

def mission_describer_1(mission: Mission,env_desc: EnvironmentDescriber, swarm_desc: SwarmDescriber, obj_desc: ObjectiveDescriber, rob_desc: RobotDescriber) -> str:
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
        robs.append(f"{num} robots of type {id}. {id} robots are built the following way: {r}")
        
    robs = " ".join(robs)
    
    r1 = f"The robots are distributed inside the area with a {swarm.pos_distribution.method} distribution with the parameters {swarm.pos_distribution.method_params}."
    r2 = f" Their orientations are distributed with {swarm.heading_distribution} with {swarm.heading_distribution.method_params}."
    
    return s1 + robs + r1 + r2

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
    s1 = f"The environment has the dimensions {environment.size}."
    s2 = f"It consists of the following elements:"
    elems = []
    for e in environment.lights.keys():
        elems.append(f"An light {e} located at {environment.lights[e].pose.position} with the orientation {environment.lights[e].pose.heading}.")
        
    elems = " ".join(elems)
    
    return s1+s2+elems

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Print generated data')
    parser.add_argument('output',
                        help='"description" or "config"')
    args = parser.parse_args()
    
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
    
    
    obstacle = Wall(size=(0.01,0.66,0.08),pose=Pose((1.0,1.0,0.0), (0.0,0.0,0.0)))
    
    light_1 = Light(Pose((0.5,0.2,0.0,),(360,0,0)))
    light_2 = Light(Pose((-0.5,0.75,0.0,),(220,0,0)))
    
    env = Environment(size=(10.0,10.0,2.0),
                      walls={"wall_1": obstacle}, lights={"light_1": light_1, "light_2": light_2})
    
    
    swarm = Swarm(
        elements={"epuck":  (epuck, 5)}, 
        heading_distribution=Distribution.get_gaussian(mean="0,0,0", stdev="360,0,0"),
        pos_distribution=Distribution.get_uniform(min="-1,-1,0", max="1,1,0"))
    
    objective = ObjAggregation(1.2, "light_1")
    #objective = ObjFlocking(density=2.5, velocity=0.2)
    #objective = ObjForaging((0.25,0.25), 0.2, (0.1,0.1), 0.4)
    #objective = ObjDistribution((2.5,7.5), max_connection_distance=0.3)
    #objective = ObjConnection("light_1", "light_2", 0.2)
    
    
    mission = Mission(env, swarm, objective)
    
    logging.debug(mission)
    
    
    if args.output == "description":
        md : MissionDescriber = mission_describer_1
        od: ObjectiveDescriber = objective_describer_1
        sd: SwarmDescriber = swarm_describer_1
        rd: RobotDescriber = robot_describer_1
        ed: EnvironmentDescriber = environment_describer_1
        
        
        
        describer = Describer(rd, ed, sd, od, md)
        
        description = describer.describe(mission)
        
        print(description)
        
    else:
        skeleton = ET.parse("../ressources/skeleton.argos").getroot()
        config = Configurator().generate_config(skeleton, mission)
        xml = ET.tostring(config).decode("ascii")
        print(xml)
    