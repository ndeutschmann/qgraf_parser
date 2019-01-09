from ..common_tools.abstract_objects import Particle,ParticleDict
from .parameters import parameters as p
import logging
logger = logging.getLogger(__name__)

# Particle definitions
phi = Particle("phi",mass=p["m"],spin=0)

# Bundle it all up
particles = ParticleDict([phi])
