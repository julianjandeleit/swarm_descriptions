#%%
from typing import Any
import xml.etree.ElementTree as ET
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
replace_placeholder_mut(root, "robots-placeholder", elements)
list(root.find("arena").find("distribute"))
# %%
