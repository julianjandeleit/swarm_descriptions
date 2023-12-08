from dataclasses import dataclass

from swarm_descriptions.datamodel import Mission
import xml.etree.ElementTree as ET

@dataclass
class Configurator:
    
    def generate_config(self, mission: Mission) -> ET:
        pass
    