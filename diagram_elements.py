"""Abstract representations of the elements of Feynman diagrams

The elements are the following
- DiagramField objects are the individual fields that attach to interaction vertices or propagators. They are in one to
one correspondance with the notion of fields in QGRAF
- DiagramVertex objects are vertices. They contain a list of fields that are attached to them (internal or external).
The code is designed such that DiagramVertex are generated first and used to generate the list of fields in the diagram
- DiagramPropagator objects represent propagators. Their field objects are picked from the list generated when parsing the
vertices
- Diagram objects represent entire diagrams and as such contain a list of Fields, Vertices and Propagators. Note that
the list of fields is obtained from the Vertices, such that each field should have a unique object representing it.
At the moment there is however no actual protections or checks to ensure that this is the case.

Vertex and Propagators are the elements that have a feynman rule attached to them, they are therefore generated with a
model, which is then searched to attach the corresponding Interaction/Propagator object
(qgraf_parser.models.common_tools.abstract_objects.Interaction or [...].Propagator)
"""
from .models.common_tools.algebra_tools import times
import logging
logger=logging.getLogger(__name__)

class DiagramField(object):
    """Specific field insertion in a Feynman diagram"""
    def __init__(self, name, field_id, momentum, model):
        """Constructor for a DiagramField object.

        Parameters
        ----------
        name : str
        field_id : int
        model : module
        """
        self.name = name
        self.id = str(abs(int(field_id)))
        self.momentum = momentum
        if int(field_id)<0:
            self.id = "ext"+self.id
        self.particle = model.particles[name]

    @staticmethod
    def parse_xml_external_leg(external_leg_node):
        """TODO DOC
        Parameters
        ----------
        external_leg_node :

        Returns
        -------

        """
        name=external_leg_node.find("field").text
        field_id=external_leg_node.find("id").text
        momentum=external_leg_node.find("momentum").text
        return (name, field_id, momentum)

    @classmethod
    def parse(cls,external_leg_node,mode='XML'):
        """TODO DOC

        Parameters
        ----------
        external_leg_node :
        mode :

        Returns
        -------

        """
        if mode=='XML':
            return cls.parse_xml_external_leg(external_leg_node)
        else:
            error = IOError("{} is not a valid input mode for DiagramField".format(mode))
            logger.error(error)
            raise error

    @classmethod
    def create_leg_from_node(cls,external_leg_node,model,mode='XML'):
        """Alternate constructor: from a <leg> node

        TODO DOC
        Parameters
        ----------
        external_leg_node :
        mode :

        Returns
        -------

        """
        cls(*cls.parse(external_leg_node,mode),model)


    def matches_id(self,field_id):
        """Check if a given field ID matches this field

        Parameters
        ----------
        field_id : int or str

        Returns
        -------
        bool
        """
        if isinstance(field_id,int):
            id = str(abs(field_id))
            if field_id<0:
                id = "ext" + id
        elif not isinstance(field_id,str):
            error=TypeError("Field id must be of type int or str")
            logger.error(error)
            raise error
        return id

    def nice_string(self):
        """Generate a long string for a field object"""
        field_string = "Diagram field for particle type {p.name} with ID {p.id}".format(p=self)
        return field_string
    def short_string(self):
        """Generate a compact notation for a field object"""
        field_string = "{p.name}({p.id})".format(p=self)
        return field_string
    def __str__(self):
        return self.nice_string()
    def __repr__(self):
        return self.short_string()

class DiagramVertex(object):
    """Specific vertex in a Feynman diagram

    TODO DOC
    Attributes
    ----------

    Methods
    -------
    """

    @staticmethod
    def parse_xml_vertex_node(vertex_node):
        """ Load the relevant data of a XML vertex node.

        This method is accessible through the class attribute `parsers` by calling cls.parsers['XML']

        Parameters
        ----------
        vertex_node : xml.etree.ElementTree.Element

        Returns
        -------
        list of tuple of str:
            triplets of (particle_type,field_id,momentum)
        """
        try:
            momenta = vertex_node.find("momenta").text.split(",")
            types=vertex_node.find("type").text.split(",")
            fields=vertex_node.find("fields").text.split(",")
        except AttributeError as error:
            logger.error("While using the XML vertex node parser:")
            logger.error("could not find the relevant vertex information in node:")
            logger.error(vertex_node)
            logger.error(error)
            raise
        try:
            assert len(momenta) == len(fields) and len(momenta) == len(types)
        except AssertionError as error:
            logger.error("While using the XML vertex node parser:")
            logger.error("the list of momenta,field IDs and types do not match in length")
            logger.error("in the vertex node:")
            logger.error(vertex_node)
            raise
        return zip(types,fields,momenta)

    # The class attribute `parsers` is a dictionnary of methods that can cast an object created by reading a file input
    # describing a vertex and outputs a list of triplets [type,field_id,momentum]

    @classmethod
    def parse(cls,vertex_node,mode):
        """
        TODO DOC
        Parameters
        ----------
        mode :

        Returns
        -------

        """
        if mode=='XML':
            return cls.parse_xml_vertex_node(vertex_node)
        else:
            error = IOError("{} is not a valid input mode for DiagramVertex".format(mode))
            logger.error(error)
            raise error

    def __init__(self,vertex_node,model,mode="XML"):
        """Constructor for a DiagramVertex object.

        Parameters
        ----------
        vertex_node : xml.etree.ElementTree.Element
            the node of the diagram output by QGRAF representing a specific vertex in a diagram
        model : module
            the module defining the model properties
        mode : str
            specification of how to read the vertex_node. The default refers to a node in a XML filed using
            xml.etree.[].XML
        TODO HANDLE EXCEPTIONS
        """

        vertex_fields = self.parse(vertex_node,mode)
        self.fields = {}
        for field in vertex_fields:
            diagfield = DiagramField(*field,model)
            self.fields.update({diagfield.id:diagfield})
        self.interaction = model.interactions[[field.name for field in self.fields.values()]]

    def generate_expression(self):
        """ Call the interaction feynman rule generation routines with

        Parameters
        ----------

        Returns
        -------
        str
            the expression of the feynman rule for this vertex
        """
        try:
            return self.interaction.generate_feynman_rule(self.fields.values())
        except (ValueError,KeyError) as error:
            logger.error("Error when generating the feynman rule for the following DiagramVertex in line {}".format(line))
            logger.error(self)
            logger.error(error)
            raise

    def access_field_by_id(self,field_id):
        """ Lookup an id in the vertex fields and return whether it is contained.

        If the id is an integer, process it to match our string conventions.

        Parameters
        ----------
        field_id : int or str
            a field index
        Returns
        -------
        DiagramField or None:
            is this ID that of a field in this vertex?
        """
        if isinstance(field_id,int):
            id = str(abs(field_id))
            if field_id<0:
                id = "ext" + id
        elif not isinstance(field_id,str):
            logger.error("Tried to access a field in a DiagramVertex with a key of type {}".format(type(field_id)))
            logger.error("Keys should be of type int or str")
            logger.error("In the DiagramVertex:")
            logger.error(self)
            error= TypeError("DiagramVertex fields must be accessed using keys of type int or str")
            logger.error(error)
            raise error
        try:
            found_field = self.fields[field_id]
        except KeyError:
            found_field = None
        return found_field

    def __contains__(self,field_id):
        return self.access_field_by_id(field_id) is not None

    def __getitem__(self, item):
        element = self.access_field_by_id(item)
        if element is None:
            error = KeyError("No such field id in DiagramVertex {}: {}".format(self,item))
            logger.error(error)
            raise error
        return element

    def __setitem__(self, key, value):
        error = NotImplementedError("DiagramVertex fields are immutable")
        logger.error(error)
        raise error

    def nice_string(self):
        return "DiagramVertex: {}".format(tuple(self.fields.values()))
    def short_string(self):
        return str(tuple(self.fields.values()))
    def __repr__(self):
        return self.short_string()
    def __str__(self):
        return self.nice_string()


class DiagramPropagator(object):
    """Specific propagator in a Feynman diagram
    TODO DOC
    """
    @staticmethod
    def parse_xml_propagator_node(propagator_node):
        """TODO DOC
        """
        # I need to put in more details about propagator oriention. Here from and to refer to the flow of momentum
        # and to the arrows for fermion propagators. The indices must therefore go in the opposite direction (to_index,from_index)
        from_field = propagator_node.find("dual-field").text
        to_field = propagator_node.find("field").text
        from_index = propagator_node.find("from").text
        to_index = propagator_node.find("to").text
        momentum = propagator_node.find("momentum").text
        return (from_field,from_index,to_field,to_index,momentum)

    @classmethod
    def parse(cls,propagator_node,mode):
        """
        TODO DOC
        Parameters
        ----------
        mode :

        Returns
        -------

        """
        if mode=='XML':
            return cls.parse_xml_propagator_node(propagator_node)
        else:
            error = IOError("{} is not a valid input mode for DiagramPropagator".format(mode))
            logger.error(error)
            raise error

    def __init__(self,propagator_node,fields,model,mode="XML"):
        """Constructor for a DiagramPropagator object.

        Parameters
        ----------
        propagator_node : xml.etree.ElementTree.Element
            the node of the diagram output by QGRAF representing a specific vertex in a diagram
        fields : dict of {str:DiagramFields}
            The vertices in the diagram - some of which could be connected to the
        model : module
            the module defining the model properties
        mode : str
            specification of how to read the vertex_node. The default refers to a node in a XML filed using
            xml.etree.[].XML
        """
        (from_field, from_index, to_field, to_index,momentum) = self.parse(propagator_node,mode)
        self.from_field = fields[from_index]
        self.to_field = fields[to_index]
        self.momentum = momentum
        self.propagator = model.propagators[[from_field,to_field]]

        ### SANITY CHECKS
        try:
            assert self.from_field.name == from_field
        except AssertionError as e:
            logger.error("Diagram propagator from_field read from XML does not match the DiagramField with the same index")
            logger.error(e)
            raise
        try:
            assert self.to_field.name == to_field
        except AssertionError as e:
            logger.error("Diagram propagator to_field read from XML does not match the DiagramField with the same index")
            logger.error(e)
            raise
        ####################

    def generate_expression(self):
        """ Call the interaction feynman rule generation routines with

        Parameters
        ----------

        Returns
        -------
        str
            the expression of the feynman rule for this vertex
        """
        try:
            return self.propagator.generate_feynman_rule([self.from_field,self.to_field],self.momentum)
        except (ValueError,KeyError) as error:
            logger.error("Error when generating the feynman rule for the following DiagramPropagator")
            logger.error(self)
            logger.error(error)
            raise

class Diagram(object):
    """Specific diagram in a QGRAF output

    TODO DOC
    """

    @staticmethod
    def parse_xml_diagram_node(diagram_node):
        """

        Parameters
        ----------
        diagram_node :

        Returns
        -------
        TODO HANDLE EXCEPTIONS
        TODO DOC
        """
        id = diagram_node.find("id").text
        vertices = diagram_node.find("vertices").findall("vertex")
        propagators = diagram_node.find("propagators").findall("propagator")
        legs = diagram_node.find("legs").findall("leg")
        return (id,legs,vertices,propagators)

    @classmethod
    def parse(cls,diagram_node,mode):
        """
        TODO DOC
        Parameters
        ----------
        mode :

        Returns
        -------

        """
        if mode=='XML':
            return cls.parse_xml_diagram_node(diagram_node)
        else:
            error = IOError("{} is not a valid input mode for Diagram".format(mode))
            logger.error(error)
            raise error

    def __init__(self,diagram_node,model,mode="XML"):
        """Constructor for a Diagram object.

        Parameters
        ----------
        diagram_node : xml.etree.ElementTree.Element
            the node of the diagram output by QGRAF representing a specific diagram
        model : module
            the module defining the model properties
        mode : str
            specification of how to read the diagram_node. The default refers to a node in a XML filed using
            xml.etree.[].XML
        TODO HANDLE EXCEPTIONS
        """
        id,legs,vertices,propagators = self.parse(diagram_node,mode)
        self.id=id
        self.external_fields = [DiagramField.create_leg_from_node(leg,model,mode) for leg in legs]
        self.vertices = [DiagramVertex(vertex,model,mode) for vertex in vertices]
        self.fields = {}
        for v_fields in [v.fields for v in self.vertices]:
            self.fields.update(v_fields)
        self.propagators = [DiagramPropagator(propagator, self.fields, model, mode) for propagator in propagators]
        self.expression = NotImplemented

    def generate_expression(self):
        vertices = [v.generate_expression() for v in self.vertices]
        propagators = [p.generate_expression() for p in self.propagators]
        return times(*(vertices+propagators))