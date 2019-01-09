'''This module defines the functions responsible for importing diagram files in appropriate formats
and generate abstract representation that can be processed using the functionalities implemented in models.

The main function is
TODO

The supported formats are:
* XML
'''

import logging
logger=logging.getLogger(__name__)

from xml.etree.ElementTree import XML,parse
from xml.etree.ElementInclude import default_loader
from qgraf_parser.diagram_elements import Diagram


def generate_XML_diagrams_node(file_path):
    """Generate an abstract representation of a XML <diagrams>

    Parameters
    ----------
    file_path : str
        string path to the XML QGRAF output

    Returns
    -------
    xml.etree.ElementTree.Element :
        the XML node corresponding to the mother <diagrams>...</diagrams> tag
    """
    return XML(default_loader(file_path, parse)).find("diagrams")

def create_diagrams_from_XML(file_path,model,mode='XML'):
    """Generate a list of Diagrams objects from XML file

    Parameters
    ----------
    file_path : str
        string path to the XML QGRAF output
    Returns
    -------
    list of qgraf_parser.diagram_elements.Diagram:
        list of diagram objects in the XML file
    """

    diagrams_node = generate_XML_diagrams_node(file_path)
    return [Diagram(diag,model,mode) for diag in diagrams_node.findall("diagram")]