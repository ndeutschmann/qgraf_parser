from models.common_tools.abstract_objects import Parameter,ParameterList,zero

g = Parameter('g', name='gs', info='strong coupling constant')
I = Parameter('i_', name='I', info='unit imaginary number')
mh = Parameter('mh', info='Higgs mass')
mt = Parameter('mt', info='Top mass')

parameters = ParameterList([I,g,mh,mt,zero])