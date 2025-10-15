# -*- coding: utf-8 -*-
"""
EduGraph - Curriculum Learning Graph Visualization (root package)
Exposes the high-level API used by scripts.
"""

from .graph_utils import GraphGenerator, generate_graph, get_graph_data

__all__ = ["GraphGenerator", "generate_graph", "get_graph_data"]
