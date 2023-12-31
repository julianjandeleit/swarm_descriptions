from dataclasses import dataclass
from typing import Protocol

from swarm_descriptions.datamodel import *
import xml.etree.ElementTree as ET
from copy import deepcopy
import logging
from xml.dom import minidom
from xml.dom.minidom import parseString
from swarm_descriptions.utils import truncate_floats
# convenience functions


def get_element(root, tag) -> ET.Element | None:
    return next(iter(list(root.iter(tag))), None)


def get_parent(root, element) -> ET.Element | None:
    parent_map = {c: p for p in root.iter() for c in p}
    return parent_map.get(element, None)


def replace_placeholder_mut(root, placeholder_tag: ET.Element, elements: list[ET.Element]):
    placeholder = get_element(root, placeholder_tag)
    parent = get_parent(root, placeholder)
    parent.remove(placeholder)
    for element in elements:
        parent.append(element)


def t2s(t: [float, float, float]) -> str:
    if isinstance(t, str):
        return t
    if isinstance(t, float):
        return str(t)
    if len(t) == 3:
        return f"{t[0]},{t[1]},{t[2]}"
    if len(t) == 2:
        return f"{t[0]},{t[1]}"
    logging.critical(f"t2s not implemented for {t}")
    exit(1)
# element builders


def build_entity(id: str, num: int):
    epuck = ET.Element("e-puck", attrib={"id": id})
    epuck.append(ET.Element("controller", attrib={"config": "automode_bt"}))

    entity = ET.Element(
        "entity", attrib={"quantity": str(num), "max_trials": "100"})
    entity.append(epuck)
    return entity


def uniform_builder(min: str, max: str):
    return {"method": "uniform", "min": min, "max": max}


def gaussian_builder(mean: str, stdev: str):
    return {"method": "gaussian", "mean": mean, "std_dev": stdev}


def general_builder(method, **kwds):
    for i, v in kwds.items():
        kwds[i] = t2s(v)
    return {"method": method, **kwds}


def build_position(distr_builder):
    return ET.Element("position", attrib=distr_builder())


def build_orientation(distr_builder):
    return ET.Element("orientation", attrib=distr_builder())


def build_light(id: str,  position: str, orientation: str) -> ET.Element:
    position = t2s(position)
    orientation = t2s(orientation)
    return ET.Element("light", attrib={"id": id, "position": position, "orientation": orientation, "color": "yellow", "intensity": "5.0", "medium": "leds"})


def build_wall(id: str, size: str, position: str, orientation: str) -> ET.Element:
    size = t2s(size)
    position = t2s(position)
    orientation = t2s(orientation)
    wall = ET.Element(
        "box", attrib={"id": id, "size": size, "movable": "false"})
    wall.append(ET.Element("body", attrib={
                "position": position, "orientation": orientation}))
    return wall


def build_size(size: tuple[float, float, float]) -> ET.Element:
    return ET.Element("arena-attrib", attrib={"size": t2s(size)})

# SML Visitors


def objective_visitor(obj: ObjectiveFunction) -> list[ET.Element]:
    loop_data = """<T>
            <params dist_radius="1.2" number_robots="20"/>
            <circle position="0,0.6" radius="0.3" color="white"/>
            <circle position="0,-0.6" radius="0.3" color="black"/>
            <spawnCircle position="0,0" radius="1.227894"/>
    </T>"""
    loop = ET.fromstring(loop_data)
    loop = list(loop)

    el_obj = ET.Element("objective", attrib={"type": obj.type})

    if isinstance(obj, ObjAggregation):
        op = ET.Element("objective-params",
                        attrib={"light": obj.light, "radius": str(obj.radius)})
        el_obj.append(op)

    if isinstance(obj, ObjFlocking):
        op = ET.Element(
            "objective-params", attrib={"density": str(obj.density), "velocity": str(obj.velocity)})
        el_obj.append(op)

    if isinstance(obj, ObjForaging):
        op = ET.Element("objective-params")
        op.append(ET.Element("circle", attrib={"position": t2s(
            obj.black_position), "radius": str(obj.black_radius), "color": "black"}))
        op.append(ET.Element("circle", attrib={"position": t2s(
            obj.white_position), "radius": str(obj.white_radius), "color": "white"}))
        el_obj.append(op)

    if isinstance(obj, ObjDistribution):
        op = ET.Element("objective-params", attrib={"area": t2s(
            obj.area), "connection_range": str(obj.max_connection_dist)})
        el_obj.append(op)

    if isinstance(obj, ObjConnection):
        op = ET.Element("objective-params", attrib={"light1": obj.light1,
                        "light2": obj.light2, "connection_range": t2s(obj.connection_range)})
        el_obj.append(op)

    loop.append(el_obj)

    return loop


def env_visitor(env: Environment) -> list[ET.Element]:
    elems = []
    for id, light in env.lights.items():
        elems.append(build_light(id, light.pose.position, light.pose.heading))

    for id, wall in env.walls.items():
        elems.append(build_wall(
            id, wall.size, wall.pose.position, wall.pose.heading))

    elems.append(build_size(env.size))
    return elems


def swarm_visitor(swarm: Swarm) -> list[ET.Element]:
    elems = []

    elems.append(build_position(lambda: general_builder(
        swarm.pos_distribution.method, **swarm.pos_distribution.method_params)))
    elems.append(build_orientation(lambda: general_builder(
        swarm.heading_distribution.method, **swarm.heading_distribution.method_params)))

    for id, (rob, num) in swarm.elements.items():
        elems.append(build_entity(id, num))

    return elems


def config_to_string(config: ET.Element) -> ET.Element:
    # https://stackoverflow.com/a/14493981
    def pretty_print(data):
        return '\n'.join([line for line in parseString(data).toprettyxml(indent=' '*2).split('\n') if line.strip()])
    xmlstr = minidom.parseString(
        ET.tostring(config)).toprettyxml(indent="   ")
    return truncate_floats(pretty_print(xmlstr))


@dataclass
class Configurator:

    def generate_config(self, skeleton_root: ET.Element, mission: Mission) -> ET.Element:
        swarm_elems = swarm_visitor(mission.swarm)
        env_elems = env_visitor(mission.environment)
        objective_elems = objective_visitor(mission.objective)

        root = deepcopy(skeleton_root)
        replace_placeholder_mut(root, "loop-placeholder", objective_elems)
        replace_placeholder_mut(root, "environment-placeholder", env_elems)
        replace_placeholder_mut(root, "robots-placeholder", swarm_elems)

        # merge arena-attrib to arena attrib
        arena = get_element(root, "arena")
        arena_attrib = get_element(root, "arena-attrib")

        for key, value in arena_attrib.items():
            arena.attrib[key] = value
        arena.remove(arena_attrib)

        return root
