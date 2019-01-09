from ..GHT import feynman_rules as FR
from .particles import particles
from ..common_tools.abstract_objects import Interaction, InteractionDict
import logging
logger = logging.getLogger(__name__)

# Particle names
gluon = particles['g']
top = particles['t']
topx = particles['tbar']
Higgs = particles['H']

# Interactions
txtH =Interaction([topx,top,Higgs],FR.txtH)
ggg = Interaction([gluon,gluon,gluon],FR.ggg)
txtg = Interaction([topx,top,gluon],FR.txtg)

# Bundle it all up
interactions = InteractionDict([ggg,txtg,txtH])

