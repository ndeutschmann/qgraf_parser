#TODO use parameters instead of string litterals!
#TODO use the info on the particle ids based
"""Implementation of the vertices of the GHT model"""
from qgraf_parser.models.common_tools.algebra_tools import *

def txtg(vertex):
    prefactor = "i_*g"
    gamma_mu3 = "g_({},mu{})".format(vertex.line,vertex.fields[2])
    T_b3_i1_i2 = "T(b{},col{},col{})".format(fields[2],fields[0],fields[1])
    return times(prefactor,gamma_mu3,T_b3_i1_i2)

def txtH(vertex):
    prefactor = '(-i_)*Y'
    delta_i1_i2 = "d_(col{},col{})".format(vertex.fields[0],vertex.fields[1])
    return times(prefactor,delta_i1_i2)

def ggg(vertex):
    prefactor = 'g'
    f_b1_b2_b3 = 'f(b{},b{},b{})'.format(vertex.fields[0],vertex.fields[1],vertex.fields[2])
    all_p_i1_minus_p_i2 = []
    for i in range(0, 3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        p1 = vertex.momenta[i]
        p2 = vertex.momenta[j]
        lp1 = pparse(p1)
        lp2 = pparse(p2)
        # add the index k to each individual momentum and then p-k
        p1 = attach_indices(p1,"mu"+vertex.fields[k])
        p2 = attach_indices(p2,"mu"+vertex.fields[k])
        p = plus(p1,minus(p2))
        delta_i1_i2 = "d_(mu{},mu{})".format(vertex.fields[i],vertex.fields[j])
        all_p_i1_minus_p_i2.append(times(delta_i1_i2,p))
    return times(prefactor,f_b1_b2_b3,*all_p_i1_minus_p_i2)





