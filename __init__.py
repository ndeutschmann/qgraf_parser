"""QGRAF PARSER"""

from .logger import init_logger
from logging import DEBUG

# Setup a logger that ensures all submodules can have nicely configured loggers
logger=init_logger(__name__,stderr_output=True,stderr_level=DEBUG)