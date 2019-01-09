from ..common_tools.abstract_objects import Parameter,ParameterDict,zero,I
import logging
logger = logging.getLogger(__name__)

# Parameter definitions
m = Parameter('m', info='scalar mass')

#Bundle it all up
parameters = ParameterDict([m,I,zero])