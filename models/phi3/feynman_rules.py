#TODO for now only ttH interaction implemented
#TODO use parameters instead of string litterals!
#TODO use fields instead of ids in the input
"""Implementation of the vertices of the GHT model"""
#from ..common_tools.algebra_tools import *
from ..common_tools.standard_propagators import *
import logging
logger = logging.getLogger(__name__)

def phi3(field_index_mapper):
    return "1"

def phi_prop(from_field,to_field,momentum):
    """

    Parameters
    ----------
    FR_data_bundle : dict

    Returns
    -------
    str
    """
    return scalar_propagator(momentum,from_field.particle.mass)


