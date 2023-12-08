#%%
from typing import Any
import xml.etree.ElementTree as ET
from copy import deepcopy
#%% [markdown]
# # Demonstrate usage of ElementTree
#%%

tree = ET.parse("/opt/argos/custom/aac.argos")
#%% 
tree
# %%
root = tree.getroot()
# %%
root.tag
# %%
list(root) # children
# %%
root.append(ET.Element("newtag", attrib={"attrib1": True}))
# %%
list(tree.getroot()) # does NOT get modified
# %%
list(ET.ElementTree(root).getroot().iter()) # instead build new tree first.
# %%
list(root.iter("epuck")) # indirect child of root
# %%
newtag = list(root.iter("newtag"))[0]
newtag.attrib
# %%
newtag.attrib["test"] = "value"
newtag.tag = "newtag-mod"
newtag.tag, newtag.attrib
# %%
[(c.tag, c.attrib) for c in root] # root does get updated
# %% [markdown]
# # Demonstrate templating in xml
# %%
skeleton = ET.parse("../ressources/skeleton.argos")
root = skeleton.getroot()
list(root)
# %%
def get_element(root, tag) -> ET.Element | None:
    return next(iter(list(root.iter(tag))), None)

def get_parent(root, element) -> ET.Element | None:
    parent_map = {c: p for p in root.iter() for c in p}
    return parent_map.get(element, None)

def replace_placeholder_mut(root, placeholder_tag: ET.Element, elements: list[ET.Element]):
    placeholder = get_element(root, placeholder_tag)
    parent = get_parent(root,placeholder)
    parent.remove(placeholder)
    for element in elements:
        parent.append(element)
    
# %%
tag = get_element(root, "robots-placeholder")
parent = get_parent(root, tag)
parent, tag
# %%
elements = [ET.Element("a"), ET.Element("b")]
_root = deepcopy(root)
replace_placeholder_mut(_root, "robots-placeholder", elements)
list(_root.find("arena").find("distribute"))
# %%
list(root.find("arena").find("distribute"))
# %%
def build_entity():
    epuck = ET.Element("e-puck", attrib={"id":"epuck"})
    epuck.append(ET.Element("controller", attrib={"config": "automode_bt"}))
    
    entity = ET.Element("entity", attrib={"quantity": "20", "max_trials":"100"})
    entity.append(epuck)
    return entity

position = ET.Element("position", attrib={"method": "uniform", "min": "-1,-1,0", "max": "1,1,0"})
orientation = ET.Element("orientation", attrib={"method": "gaussian", "mean": "0,0,0", "std_dev":"360,0,0"})
entity = build_entity()
robots = [position, orientation, entity]
robots
# %%
def build_wall(id: str, size: str, position: str, orientation: str) -> ET.Element:
    wall = ET.Element("box", attrib={"id": id,"size": size, "movable":"false"})
    wall.append(ET.Element("body", attrib={"position": position, "orientation": orientation}))
    return wall


walls_data = [
    {"id": "wall_1", "size": "0.01,0.66,0.08", "position": "1.23,0,0", "orientation": "0,0,0"},
    {"id": "wall_2", "size": "0.01,0.66,0.08", "position": "0,1.23,0", "orientation": "90,0,0"},
    {"id": "wall_3", "size": "0.01,0.66,0.08", "position": "0.615,1.07,0", "orientation": "60,0,0"},
    {"id": "wall_4", "size": "0.01,0.66,0.08", "position": "1.07,0.615,0", "orientation": "30,0,0"},
    {"id": "wall_5", "size": "0.01,0.66,0.08", "position": "1.07,-0.615,0", "orientation": "-30,0,0"},
    {"id": "wall_6", "size": "0.01,0.66,0.08", "position": "0.615,-1.07,0", "orientation": "-60,0,0"},
    {"id": "wall_7", "size": "0.01,0.66,0.08", "position": "0,-1.23,0", "orientation": "90,0,0"},
    {"id": "wall_8", "size": "0.01,0.66,0.08", "position": "-1.07,-0.615,0", "orientation": "30,0,0"},
    {"id": "wall_9", "size": "0.01,0.66,0.08", "position": "-0.615,-1.07,0", "orientation": "60,0,0"},
    {"id": "wall_10", "size": "0.01,0.66,0.08", "position": "-1.23,0,0", "orientation": "0,0,0"},
    {"id": "wall_11", "size": "0.01,0.66,0.08", "position": "-1.07,0.615,0", "orientation": "-30,0,0"},
    {"id": "wall_12", "size": "0.01,0.66,0.08", "position": "-0.615,1.07,0", "orientation": "-60,0,0"}
]

walls = [build_wall(**d) for d in walls_data]
list(walls)
# %%
# <light id="light" position="0,-1.35,0.45" orientation="0,0,0" color="yellow" intensity="5.0" medium="leds"/>
lights = [ET.Element("light", attrib={"id":"light_1", "position": "0,-1.35,0.45", "orientation":"0,0,0", "color":"yellow", "intensity":"5.0", "medium":"leds"})]
lights
# %%
loop_data = """<T>
        <params dist_radius="1.2" number_robots="20"/>
        <circle position="0,0.6" radius="0.3" color="white"/>
        <circle position="0,-0.6" radius="0.3" color="black"/>
        <spawnCircle position="0,0" radius="1.227894"/>
</T>"""
loop = ET.fromstring(loop_data)
loop = list(loop)
loop
# %% [markdown]
# ## Apply placeholder replacement
# %%
replace_placeholder_mut(root, "loop-placeholder", loop)
replace_placeholder_mut(root, "environment-placeholder", lights + walls)
replace_placeholder_mut(root, "robots-placeholder", robots)
# %%
print(ET.tostring(root, encoding="ascii", xml_declaration=True).decode("ascii"))
# %%
