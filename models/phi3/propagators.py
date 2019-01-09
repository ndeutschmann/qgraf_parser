from ..common_tools.abstract_objects import Propagator,PropagatorDict
from ..phi3 import feynman_rules as FR
from .particles import particles
import logging
logger = logging.getLogger(__name__)

phi = particles['phi']


# Propagators
phiphi = Propagator([phi,phi],FR.phi_prop)

# Bundle it all up
propagators = PropagatorDict([phiphi])