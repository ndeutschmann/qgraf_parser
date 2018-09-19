#TODO change docstrings to numpy style
"""Basic tools for manipulating algebraic expressions in strings"""
import re

def parwrap(*args):
    """Wrap each term in a sequence of strings between parentheses
    :param *args: sequence of strings
    :returns: a list of wrapped strings
    """
    return ["("+arg+")" for arg in args]

def times(*args):
    """
    Write the string corresponding to the product of each term represented by a sequence of strings. Wrap each string between parentheses for safety
    :param *args: sequence of strings
    :returns: the product of each string
    """
    return "*".join(parwrap(*args))

def plus(*args):
    """
    Write the string corresponding to the sum of each term represented by a sequence of strings. Wrap each string between parentheses for safety
    :param *args: sequence of strings
    :returns: the sum of each string
    """
    return "+".join(parwrap(*args))

def minus(x):
    """
    Return the opposite of a string
    :param x: a string
    :return: -(x)
    """
    return "-"+parwrap(x)

def pparse(p):
    """Parse a momenta expressed as a sum of +/- individual momenta into each component, keeping the sign.
    Example: -p1+p2-p3 -> [-p1,+p2,-p3]

    :param p: a combination of momenta
    :type p: str
    :return: list of individual strings for each momentum
    """
    lp=re.split("[+-]",p)
    for mom in [x for x in lp if x!='']:
        p=p.replace(mom,mom+",")
    lp=p.split(",")
    return [x for x in lp if x!='']

def attach_indices(tensors,*indices):
    """
    Take a tensor T written as a linear combination (T = T1 - T2 + T3 ...) and attach an set of indices to each of them: T(mu1,b2,x3) = T1(mu1,b2,x3) - T2(mu1,b2,x3) + T3(mu1,b2,x3) ...
    TODO: This should work for LCs of the form Sum n_i*Tensor_i. However if the tensor is *not* the last object of each monomial, there will be trouble
    TODO: Find a way to perform checks
    :param tensors: string representing a linear combination of tensors
    :param indices: list of strings representing a set of indices to attach
    :return: A string representing the linear combination with the open indices specified
    """
    if tensors!="0":
        tensor_list = pparse(tensors)
        indices_between_parentheses = "({})".format(",".join(indices))
        for t in tensor_list:
            return tensors.replace(t, t + indices_between_parentheses)
    else:
        return tensors
