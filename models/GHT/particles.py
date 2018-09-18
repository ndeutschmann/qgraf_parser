from models.common_tools.abstract_objects import Particle
from models.GHT.parameters import parameters as p

H = Particle("H",mass=p.mh,spin=0)
t = Particle("t",mass=p.mt,spin=2)
g = Particle("g",mass=p.zero,spin=3)

