"""Basic model with a Gluon, a Higgs and a Top quark"""
from .parameters import parameters
from .particles import particles
from .interactions import interactions
from .propagators import propagators
import logging
logger = logging.getLogger(__name__)