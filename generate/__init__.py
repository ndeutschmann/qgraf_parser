"""Steering qgraf from python
"""
import yaml
import os
import logging
logger=logging.getLogger(__name__)

config_file = "setup.yaml"
module_path = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(module_path,config_file)
with open(config_file_path) as config_raw:
    config = yaml.load(config_raw.read())


from .generator_interface import GeneratorCmd

def start_GeneratorCmd(config=config):
    """Start the Generator Command Line Interface"""
    GeneratorCmd(config=config).cmdloop()