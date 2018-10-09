from itertools import permutations
import logging

logger = logging.getLogger(__name__)

class AbstractObjectDict(object):
    """Dictionnary-like class with iteration over values

    This is a meta class which fails upon instantiation. Daughter classes should specify the class attribute _type as a class objet for the thing to be contained in a <type>Dict. It is necessary that the type in question have an attribute "name".

    New item should be added using the method append which creates a key using the item's name attribute.
    This class can be iterated over and the iteration returns the *values* in the dictionary, *not the keys*.

    One can relabel added items using self.relabel(old_key,new_key)

    Methods
    -------
    append(obj)
    relabel(old_key,new_key)
    keys

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
            message = "All elements in a " + str(type(self)) + " need to be of type " + _type
            logger.error(message)
            raise TypeError(message)
        if obj.name in self.internal_dict:
            message = "This object name exists already in the dictionnary {}: {}".format(self,obj)
            logger.error(message)
            raise KeyError(message)
        self.internal_dict[obj.name]=obj

    def __init__(self,list_of_objects):
        if self._type is None:
            message = "Use a specific daughter class of AbstractObjectDictionnary"
            logger.error(message)
            raise NotImplementedError(message)
        self.internal_dict={}
        for obj in list_of_objects:
            self.append(obj)

    def relabel(self,old_key,new_key):
        """Relabel a key of the dictionary"""
        self.internal_dict[new_key] = self.internal_dict[old_key]
        del self.internal_dict[old_key]

    def keys(self):
        """Access the keys of the internal dictionary"""
        return self.internal_dict.keys()

    def __getitem__(self, item):
        return self.internal_dict[item]
    def __iter__(self):
        self._iterator = iter(self.internal_dict)
        return self
    def __next__(self):
        key = next(self._iterator)
        return self[key]
    def __repr__(self):
        return repr(list(self.internal_dict.values()))
    def __str__(self):
        return str(list(self.internal_dict.values()))






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
            assert isinstance(complex_conjugate,str) #Allow for couplings but force a string
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
    def __str__(self):
        return "Particle: {p.name}".format(p=self)
    def __repr__(self):
        return self.name


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
        """Creator for the Interaction class

        Parameters
        ----------
        particles : list of Particle
        feynman_rule : function
        """
        self.particles = particles
        self.feynman_rule = feynman_rule
        self.name = ",".join([particle.name for particle in particles])
    def generate_feynman_rule(self,fields,*,line=None):
        """Create a string corresponding to the feynman rule for the qgraf_parser Vertex vertex

        Parameters
        ----------
        fields: list of qgraf_parser.diagram_elements.DiagramField
            list of fields
        line: str,optional
            the fermion line

        Returns
        -------
        str
            the expression of the feynman rule for this interaction with a specific choice of fields.
        """
        # Generate a dictionary field_name : [list of matching ids]
        field_index_mapper = {}
        for field in fields:
            if field.name in field_index_mapper:
                field_index_mapper[field.name].append(field.id)
            else:
                field_index_mapper[field.name]=[field.id]
        try:
            feynman_rule = self.feynman_rule(field_index_mapper,line=line)
        except (ValueError,KeyError) as error:
            logger.error("Error when generating feynman rule for Interaction:")
            logger.error(str(self))
            logger.error("With the following field mapping:")
            logger.error(str(field_index_mapper))
            logger.error("And the fermion line {}".format(line))
            logger.error(error)
            raise

        return feynman_rule

    def nice_string(self):
        return "Interaction: ({})".format(self.name)
    def short_string(self):
        return "({})".format(self.name)
    def __str__(self):
        return self.nice_string()
    def __repr__(self):
        return self.short_string()


class InteractionDict(AbstractObjectDict):
    """Container for Interactions. Inherits from AbstractObjectDict
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
            try:
                assert isinstance(item,list)
            except TypeError as t:
                message = "InteractionDict elements can be accessed using strings or lists as keys. Here a {} was used".format(type(item))
                logger.error("")
            orderings = list(permutations(item))
            for ordering in orderings:
                if ",".join(ordering) in self.internal_dict:
                    break
            return self.internal_dict[",".join(ordering)]




#####################################################################
#####################################################################
# Useful instances
#####################################################################
#####################################################################

zero = Parameter("zero")