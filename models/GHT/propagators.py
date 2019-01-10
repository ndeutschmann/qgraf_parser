from ..common_tools.abstract_objects import Propagator,PropagatorDict
from ..GHT import feynman_rules as FR
from .particles import particles
import logging
logger = logging.getLogger(__name__)

gluon = particles['g']
top = particles['t']
topx = particles['tbar']
Higgs = particles['H']

# Propagators
#TODO This should be created dynamically when initializing Particle objects.
#TODO plan: have a self-conjugate option when initializing particles
#TODO when assigning a particle to a ParticleDict, it should scan this option and if it's False, create a new Particle
#TODO [possible refinement, have an attribute that sends to the anti-particle, or have a 'conjugation_convention' that
#TODO indicates when to add a 'bar', '~', or 'x' etc.]
#TODO Then the model.__init__.py should create the propagators automatically
#TODO To preserve the flexibility of feynman rules functions, the FR should be assigned to particles, or we can preserve
#TODO the propagators.py and have it only initialize propagators from a single particle.
ttx =Propagator([topx,top],FR.top_prop)
HH = Propagator([H,H],NotImplemented)

# Bundle it all up
propagators = PropagatorDict([ttx])