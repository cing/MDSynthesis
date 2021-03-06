# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# mdsynthesis

"""
MDSynthesis --- a persistence engine for molecular dynamics data
================================================================

MDSynthesis is designed to address the logistical aspects of molecular dynamics
trajectory analysis. Whereas MDAnalysis gives the computational tools to
dissect trajectories, MDSynthesis provides a framework for automatically
organizing the results. This allows you (the scientist) to focus on your
science, letting the computer handle the lower-level logistical details.

.. SeeAlso:: :class:`mdsynthesis.containers.Sim` 
             :class:`mdsynthesis.containers.Group`


"""

__version__ = "0.4.0-dev"  # NOTE: keep in sync with RELEASE in setup.py

__all__ = ['Sim', 'Group', 'Coordinator']

# Bring some often used objects into the current namespace
#from coordinator import Coordinator
from containers import Sim, Group
from coordinator import Coordinator
import core
from core.bundle import Bundle
from manipulators import *
