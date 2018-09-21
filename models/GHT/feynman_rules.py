#TODO use parameters instead of string litterals!
#TODO use the info on the particle ids based
"""Implementation of the vertices of the GHT model"""
from ..common_tools.algebra_tools import *

def txtg(field_index_mapper,*,line=None):
    if line is None:
        raise ValueError("Line unspecified in txtg vertex")
    g = field_index_mapper['g'][0]
    tx =field_index_mapper['tbar'][0]
    t = field_index_mapper['t'][0]
    prefactor = "i_*g"
    gamma_mu3 = "g_({},mu{})".format(line,g)
    T_b3_i1_i2 = "T(b{},col{},col{})".format(g,tx,t)
    return times(prefactor,gamma_mu3,T_b3_i1_i2)

def txtH(field_index_mapper,line=None):
    tx =field_index_mapper['tbar'][0]
    t = field_index_mapper['t'][0]
    prefactor = '(-i_)*Y'
    delta_i1_i2 = "d_(col{},col{})".format(tx,t)
    return times(prefactor,delta_i1_i2)

def ggg(field_index_mapper,line=None):
    gluons = field_index_mapper['g']
    prefactor = 'g'
    f_b1_b2_b3 = 'f(b{},b{},b{})'.format(gluons[0],gluons[1],gluons[2])
    all_p_i1_minus_p_i2 = []
    for i in range(0, 3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        p1 = vertex.momenta[i]
        p2 = vertex.momenta[j]
        lp1 = pparse(p1)
        lp2 = pparse(p2)
        # add the index k to each individual momentum and then p-k
        p1 = attach_indices(p1,"mu"+gluons[k])
        p2 = attach_indices(p2,"mu"+gluons[k])
        p = plus(p1,minus(p2))
        delta_i1_i2 = "d_(mu{},mu{})".format(gluons[i],gluons[j])
        all_p_i1_minus_p_i2.append(times(delta_i1_i2,p))
    return times(prefactor,f_b1_b2_b3,*all_p_i1_minus_p_i2)





