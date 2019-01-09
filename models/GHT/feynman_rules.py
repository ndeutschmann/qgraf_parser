#TODO for now only ttH interaction implemented
#TODO use parameters instead of string litterals!
#TODO use fields instead of ids in the input
"""Implementation of the vertices of the GHT model"""
from ..common_tools.algebra_tools import *
from ..common_tools.standard_propagators import *
import logging
logger = logging.getLogger(__name__)

# def txtg(field_index_mapper,*,line=None):#TODO Refactor for no lines and fields
#     try:
#         assert line is not None
#     except AssertionError:
#         message = "Line unspecified in txtg vertex"
#         logger.error(message)
#         raise ValueError(message)
#     g = field_index_mapper['g'][0]
#     tx =field_index_mapper['tbar'][0]
#     t = field_index_mapper['t'][0]
#     prefactor = "i_*g"
#     gamma_mu3 = "g_({},mu{})".format(line,g)
#     T_b3_i1_i2 = "T(b{},col{},col{})".format(g,tx,t)
#     return times(prefactor,gamma_mu3,T_b3_i1_i2)

def txtH(field_index_mapper):
    """Feynman rule for the top Yukawa interaction

    Parameters
    ----------
    field_index_mapper : (dict of str : qgraf_parser.diagram_elements.DiagramField)
        maps a particle name to a list of fields corresponding to that particle

    Returns
    -------
    str
        The FORM expression for the Feynman rule
    """
    tx =field_index_mapper['tbar'][0]
    t = field_index_mapper['t'][0]
    prefactor = '(-i_)*Y'
    delta_i1_i2 = "d_(col{},col{})".format(tx.id,t.id) # color delta
    delta_s1_s2 = "d_(s{},s{})".format(tx.id,t.id)# Dirac algebra delta
    return times(prefactor,delta_i1_i2,delta_s1_s2)

# def ggg(field_index_mapper,line=None):#TODO Refactor for no lines and fields
#     gluons = field_index_mapper['g']
#     prefactor = 'g'
#     f_b1_b2_b3 = 'f(b{},b{},b{})'.format(gluons[0],gluons[1],gluons[2])
#     all_p_i1_minus_p_i2 = []
#     for i in range(0, 3):
#         j = (i + 1) % 3
#         k = (i + 2) % 3
#         p1 = vertex.momenta[i]
#         p2 = vertex.momenta[j]
#         lp1 = pparse(p1)
#         lp2 = pparse(p2)
#         # add the index k to each individual momentum and then p-k
#         p1 = attach_indices(p1,"mu"+gluons[k])
#         p2 = attach_indices(p2,"mu"+gluons[k])
#         p = plus(p1,minus(p2))
#         delta_i1_i2 = "d_(mu{},mu{})".format(gluons[i],gluons[j])
#         all_p_i1_minus_p_i2.append(times(delta_i1_i2,p))
#     return times(prefactor,f_b1_b2_b3,*all_p_i1_minus_p_i2)
#
def top_prop(field_index_mapper):#TODO refactor propagators to label fields with the from/to information provided in the XML input (motivated by error mitigation)
    """

    Parameters
    ----------
    field_index_mapper : dict of {str : qgraf_parser.diagram_elements.DiagramField}

    Returns
    -------

    """
    tx =field_index_mapper['tbar'][0]
    t = field_index_mapper['t'][0]
    return quark_propagator(t.id,tx.id,t.mass,t.momentum)


