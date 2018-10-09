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
        self.id = str(abs(field_id))
        self.momentum = momentum
        if field_id<0:
            self.id = "ext"+self.id
        self.particle = model.particles[name]

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
    TODO
    Attributes
    ----------

    Methods
    -------
    """

    @staticmethod
    def parse_xml_vertex_node(vertex_node):
        """ Load the relevant data of a XML vertex node. This method is accessible through the class attribute `parsers` by calling cls.parsers['XML']

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
    parsers = {"XML": parse_xml_vertex_node}

    def __init__(self,vertex_node,model,mode="XML"):
        """Constructor for a DiagramVertex object.

        Parameters
        ----------
        vertex_node :
            the node of the diagram output by QGRAF representing a specific vertex in a diagram
        model : module
            the module defining the model properties
        mode : str
            specification of how to read the vertex_node. The default refers to a node in a XML filed using
            xml.etree.[].XML
        """

        vertex_fields = self.parsers[mode](vertex_node)
        self.fields = []
        for field in vertex_fields:
            self.fields.append(DiagramField(*field))
        self.interaction = model.interactions[[field.name for field in self.fields]]

    def generate_expression(self,*,line=None):
        """ Call the interaction feynman rule generation routines with

        Parameters
        ----------
        line : str,optional
            fermion line number

        Returns
        -------
        str
            the expression of the feynman rule for this vertex
        """
        try:
            self.interaction.generate_feynman_rule(self.fields,line=line)
        except (ValueError,KeyError) as error:
            logger.error("Error when generating the feynman rule for the following DiagramVertex in line {}".format(line))
            logger.error(self)
            logger.error(error)
            raise
    def nice_string(self):
        return "DiagramVertex: {}".format(tuple(self.fields))
    def short_string(self):
        return str(tuple(self.fields))
    def __repr__(self):
        return self.short_string()
    def __str__(self):
        return self.nice_string()