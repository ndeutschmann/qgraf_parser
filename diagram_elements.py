import logging
from copy import deepcopy

class Diagram_Field(object):
    """Specific field insertion in a Feynman diagram"""
    def __init__(self,name,field_ID,momentum,model):
        """Constructor for a Diagram_Field object.

        Parameters
        ----------
        name : str
        field_ID : int
        model : module
        """
        self.name = name
        self.id = str(abs(field_ID))
        self.momentum = momentum
        if field_ID<0:
            self.id = "ext"+self.id
        self.particle = model.particles[name]

    def __str__(self):
        return self.id

class Diagram_Vertex(object):
    """Specific vertex in a Feynman diagram

    Attributes
    ----------

    Methods
    -------
    """

    @staticmethod
    def parse_xml_vertex_node(vertex_node):
        """ Load the relevant data of a XML vertex node

        Parameters
        ----------
        vertex_node : xml.etree.ElementTree.Element

        Returns
        -------
        list of tuple of str:
            triplets of (particle_type,field_id,momentum)
        """
        try:
            momenta = element.find("momenta").text.split(",")
            types=element.find("type").text.split(",")
            fields=element.find("fields").text.split(",")
        except AttributeError as error:
            logging.error("Error while parsing a XML vertex")
            logging.error(error)
            raise
        try:
            assert len(momenta) == len(fields) and len(momenta) = len(types)
        except AssertionError as error:
            logging.error("Something went wrong when parsing a vertex: not the same number for each attribute list")
            logging.error(error)
            raise
        return zip(types,fields,momenta)

    parsers = {"XML": parse_xml_vertex_node}

    def __init__(self,vertex_node,model,mode="XML"):
        """Constructor for a Diagram_Vertex object.

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
            self.fields.append(Diagram_Field(*field))
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
        return self.interaction.generate_feynman_rule(self.fields,line=line)