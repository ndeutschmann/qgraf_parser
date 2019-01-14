"""The command-line interface for the QGRAF importer

The main feature is the implementation of the ImporterCmd class
"""
from cmd import Cmd
import qgraf_parser.generator.qgraf_setup as qgraf_setup
import subprocess
import os

import logging
logger=logging.getLogger(__name__)

class ImporterCmd(Cmd):
    """The command-line interface for the QGRAF generator of qgraf_parser
    """
    prompt = 'QGRAF-importer>'
    intro = "Welcome to the importer! Type ? to list commands"

    def valid_config(self,config):
        """TODO Implement

        Parameters
        ----------
        config :

        Returns
        -------

        """
        logger.warning("No check for configuration validity in qgraf_parser.importer.importer_interface.ImporterCmd#__init__")
        return True

    def __init__(self,*args,config,**kwargs):
        logger.info("Creating a Generator Command Line")
        Cmd.__init__(self,*args,**kwargs)

        self.config = config
        try:
            assert self.valid_config()
        except AssertionError as e:
            logger.error("Incorrect configuration when instantiating a GeneratorCmd")
            logger.error(e)
            raise


    def do_load_model(self,model_name):
        """
        TODO DOC
        TODO Implement
        Parameters
        ----------
        model_name :

        Returns
        -------

        """
        raise NotImplementedError

    def do_import_diagrams(self,diagram_path):
        """
        TODO Implement
        Parameters
        ----------
        diagram_path :

        Returns
        -------

        """
        raise NotImplementedError

    def do_export_diagrams(self,output_path):
        """
        TODO Implement
        Parameters
        ----------
        output_path :

        Returns
        -------

        """
        raise NotImplementedError