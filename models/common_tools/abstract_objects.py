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




class ParameterList(list):
    """
    Container for couplings.
    For now just checks that all entries are Parameters

    TODO describe checks
    TODO describe __getattr__
    """
    def __new__(cls, *args, **kwargs):
        """

        Parameters
        ----------
        args :
        kwargs :

        Returns
        -------

        """
        new_parameter_list = list.__new__(cls,*args, **kwargs)
        for param in new_parameter_list:
            try:
                assert isinstance(param,Parameter)
            except AssertionError:
                raise AssertionError("Cannot create a ParameterList: all entries should be of Parameter type")
        # Check that there are no name duplicates
        try:
            assert len(new_parameter_list) == len(set([param.name for param in new_parameter_list]))
        except AssertionError:
            raise AssertionError("Cannot create a ParameterList: there are two entries with the same name attribute")
        return new_parameter_list
    def append(self, param):
        try:
            assert isinstance(param,Parameter)
        except AssertionError:
            raise AssertionError("Cannot append to this ParameterList: all entries should be of Parameter type")
        # Check that we're not adding a parameter with an existing name
        try:
            assert param.name not in [p.name for p in self]
        except AssertionError:
            raise AssertionError("Cannot append Parameter to this ParameterList: this name already exists")
        super().append(param)
    def __getattr__(self, item):
        """
        Use parameter names as attributes
        """
        for param in self:
            if item == param.name:
                return param
            raise AttributeError("No parameter with name % found"%item)


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



class ParticleList(list):
    """
    Container for couplings.
    For now just checks that all entries are Particles
    TODO BAD implement a mother class for mixed list-dict behavior
    TODO describe checks
    TODO describe __getattr__
    """
    def __new__(cls, *args, **kwargs):
        new_particle_list = list.__new__(cls,*args, **kwargs)
        for part in new_particle_list:
            try:
                assert isinstance(part,Particle)
            except AssertionError:
                raise AssertionError("Cannot create a ParticleList: all entries should be of Particle type")
        # Check that there are no name duplicates
        try:
            assert len(new_particle_list) == len(set([part.name for part in new_particle_list]))
        except AssertionError:
            raise AssertionError("Cannot create a ParticleList: there are two entries with the same name attribute")
        return new_particle_list
    def append(self, part):
        try:
            assert isinstance(part,Particle)
        except AssertionError:
            raise AssertionError("Cannot append to this ParticleList: all entries should be of Particle type")
        # Check that we're not adding a particle with an existing name
        try:
            assert part.name not in [p.name for p in self]
        except AssertionError:
            raise AssertionError("Cannot append Particle to this ParticleList: this name already exists")
        super().append(part)
    def __getattr__(self, item):
        """
        Use particle names as attributes
        """
        for part in self:
            if item == part.name:
                return part
            raise AttributeError("No particle with name % found"%item)




#####################################################################
#####################################################################
# Useful instances
#####################################################################
#####################################################################

zero = Parameter("zero")