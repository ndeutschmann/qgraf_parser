from ..GHT import feynman_rules as FR
from .particles import particles
from ..common_tools.abstract_objects import Interaction, InteractionDict

# Particle names
gluon = particles['g']
top = particles['t']
topx = particles['tbar']
Higgs = particles['H']

# Interactions
ggg = Interaction([gluon,gluon,gluon],FR.ggg)
txtg = InteractionDict([topx,top,gluon],FR.txtg)
txtH =InteractionDict([topx,top,Higgs],FR.txtH)

# Bundle it all up
interactions = InteractionDict([ggg,txtg,txtH])

