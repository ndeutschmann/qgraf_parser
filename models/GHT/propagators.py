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
ttx =Propagator([top,topx],None)

# Bundle it all up
propagators = PropagatorDict([])