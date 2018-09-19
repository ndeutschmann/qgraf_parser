from itertools import permutations

class AbstractObjectDict(object):
    """Dictionnary-like class with iteration over values

    This is a meta class which fails upon instantiation. Daughter classes should specify the class attribute _type as a class objet for the thing to be contained in a <type>Dict. It is necessary that the type in question have an attribute "name".

    New item should be added using the method append which creates a key using the item's name attribute.
    This class can be iterated over and the iteration returns the *values* in the dictionary, *not the keys*.

    Methods
    -------
    append(obj)

    Attributes
    ----------
    internal_dict: dict
        the dictionary in which data is stored
    _type: type
        the type of the objects contained here
    """

    _type = None

    def append(self,obj):
        if not isinstance(obj, self._type):
            raise TypeError("All elements in a " + str(type(self)) + " need to be of type " + _type)
        if obj.name in self.internal_dict:
            raise KeyError("This object name exists already!")
        self.internal_dict[obj.name]=obj

    def __init__(self,list_of_objects):
        if self._type is None:
            raise NotImplementedError("Use a specific daughter class of AbstractObjectDictionnary")
        self.internal_dict={}
        for obj in list_of_objects:
            self.append(obj)
    def __getitem__(self, item):
        return self.internal_dict[item]
    def __iter__(self):
        self._iterator = iter(self.internal_dict)
        return self
    def __next__(self):
        key = next(self._iterator)
        return self[key]
    def __repr__(self):
        return str(list(self.internal_dict.keys()))






class Parameter(str):
    """ Abstract representation of a parameter.

    This class inherits from string. As a result it is initialized as a string would: c = Parameter('c').
    Special attributes are added and can be specified at initialization using options.

    Attributes
    ----------
    name : str
        name of the parameter (typically its symbol). If not specified, the algebraic expression passed as string value is used.
    info : str
        user defined information
    value: numeric type
        numerical value of the parameter. To allow for possible extended numeric types (complex or matrices or ...) *no check* is performed
    complex_conjugate: str
        string representation of its complex conjugate. Most often this simply returns the string of the parameter itself as the default is to be real. Note that this attribute can also be a Parameter itself

    Notes
    -----

    The complex_conjugate option is really wonky at the moment. Use at your own risk and only if you know what you're doing.
    """
    def __new__(cls,  *args, name=None, info='',value = None, complex_conjugate=None, **kwargs):
        """Creator for the Parameter class, inheriting from list.

        Parameters
        ----------
        args : list
            arguments to give to the list creator. Typically just a string litteral
        name : str, optional
        info : str,optional
        value : numeric,optional
        complex_conjugate : str,optional
        kwargs : dict
            option to give to the list creator
        """
        new_coupling = str.__new__(cls, *args,**kwargs)
        if name is None:
            new_coupling.name = new_coupling.__str__()
        else:
            new_coupling.name = str(name)
        new_coupling.info = str(info)
        new_coupling.value = value
        if complex_conjugate is None:
            new_coupling.complex_conjugate = new_coupling.__str__()  # The default assumption is a real parameter
        else:
            assert isinstance(complex_conjugate,str) #Allow for couplings but force a string child
            new_coupling.complex_conjugate = complex_conjugate
        return new_coupling




class ParameterDict(AbstractObjectDict):
    """
    Container for Parameters. Inherits from AbstractObjectDict
    """
    _type = Parameter


class Particle:
    """Abstract representation of a particle type (i.e. 1 instance = 1 field)
    Attributes
    ----------
    name : str
    mass : Parameter
    spin : int
        Dimensionality of the spin state space, i.e. spin = 2*S+1

    Notes
    -----
    I commented out the functionnalities to have an attribute
    anti_particle: Particle
    which can also relate to itself if the particle is self-conjugate and be NotImplemented if the theory does not have anti particles (eg NR stuff)
    """

    def __init__(self, name, *, mass, spin=0, **kwargs): #anti_particle = NotImplemented
        """
        Parameters
        ----------
        name : str
        mass : Parameter
        spin : int
        kwargs : dict
        """
        self.name = str(name)
        self.mass = mass
        self.spin = spin
        # self.anti_particle = anti_particle
        # if self.anti_particle=None:
        #     self.anti_particle = self

        for key in kwargs:
            self.__setattr__(key,kwargs[key])



class ParticleDict(AbstractObjectDict):
    """
    Container for Particles. Inherits from AbstractObjectDict
    """
    _type = Particle


class Interaction(object):
    """Abstract representation of an interaction vertex
    TODO add more structure based on the new qgraf vertex object
    """
    def __init__(self,particles,feynman_rule):
        self.particles = ParticleDict(particles)
        self.feynman_rule = feynman_rule
        self.name = ",".join([particle.name for particle in particles])
    def __call__(self,vertex):
        return self.feynman_rule(vertex)

class InteractionDict(AbstractObjectDict):
    """Container for Interactions. Inherits from AbstractObjectDict
    An interactionDict is callable using a Vertex object which searches and calls the correct interaction.
    """
    _type = Interaction
    def __getitem__(self, item):
        """Get the content of the dictionary. Two ways of doing so: either with the name of the interaction or with a list of particle names. Due to how interaction names are generated, in this second case, all possible names can be obtained by looping over orderings of the particle names and joining them with commas.

        Parameters
        ----------
        item : str or list of str
            interaction name or list of particle names

        Returns
        -------
        self[item] : Interaction
        """
        if isinstance(item,str):
            return self.internal_dict[item]
        else:
            assert isinstance(item,list)
            orderings = list(permutations(item))
            for ordering in orderings:
                if sum(ordering) in self.internal_dict:
                    break
            return self.internal_dict[sum(ordering)]
    def __call__(self,vertex):
        """Use the vertex.types list of particle names as a key in the dictionary and call the corresponding interaction, i.e. Interaction.feynman_rule

        Parameters
        ----------
        vertex : vertex.Vertex
            a Vertex object defined in qgraf_parser

        Returns
        -------
        str
        """
        return self[vertex.types](vertex)




#####################################################################
#####################################################################
# Useful instances
#####################################################################
#####################################################################

zero = Parameter("zero")