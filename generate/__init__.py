"""Steering qgraf from python
"""
import logging
import yaml
import os

logger=logging.getLogger(__name__)

config_file = "setup.yaml"
module_path = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(module_path,config_file)
with open(config_file_path) as config_raw:
    config = yaml.load(config_raw.read())
