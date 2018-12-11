'''This module defines the functions responsible for importing diagram files in appropriate formats
and generate abstract representation that can be processed using the functionalities implemented in models.

The main function is
TODO

The supported formats are:
* XML
'''

from xml.etree.ElementTree import XML,parse
from xml.etree.ElementInclude import default_loader

def generate_XML_diagrams_node(file_path):
    """
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

