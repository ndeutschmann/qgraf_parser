from ..phi3 import feynman_rules as FR
from .particles import particles
from ..common_tools.abstract_objects import Interaction, InteractionDict
import logging
logger = logging.getLogger(__name__)

# Particle names
phi = particles['phi']


# Interactions
phi3 =Interaction([phi,phi,phi],FR.phi3)

# Bundle it all up
# interactions = InteractionDict([ggg,txtg,txtH])
interactions = InteractionDict([phi3])

