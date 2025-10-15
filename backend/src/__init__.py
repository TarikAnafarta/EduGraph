# -*- coding: utf-8 -*-
"""
EduGraph backend package - re-exports top-level API for convenience.
"""

from .graph_utils import GraphGenerator, generate_graph, get_graph_data

__all__ = ["GraphGenerator", "generate_graph", "get_graph_data"]
