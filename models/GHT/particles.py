from ..common_tools.abstract_objects import Particle,ParticleDict
from .parameters import parameters as p

# Particle definitions
H    = Particle("H",mass=p["mh"],spin=0)
t    = Particle("t",mass=p["mt"],spin=2)
tbar = Particle("t",mass=p["mt"],spin=2)
g    = Particle("g",mass=p["zero"],spin=3)

# Bundle it all up
particles = ParticleDict([H,t,tbar,g])

###############
# NOTES
###############

# Having tbar as separate makes me want to implement a anti_particle attribute
# TODO start refactoring main code and see if Particle.anti_particle is desirable