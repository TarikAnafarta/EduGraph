# -*- coding: utf-8 -*-
"""
Backend facade that re-exports the implementation from the top-level src package.
This keeps a clean separation while preserving backend imports.
"""
from typing import List, Dict, Any, Tuple

# Import from top-level src
from ...src.graph_utils import GraphGenerator as _GraphGenerator
from ...src.graph_utils import generate_graph as _generate_graph
from ...src.graph_utils import get_graph_data as _get_graph_data


# Re-export types and functions
GraphGenerator = _GraphGenerator

def generate_graph(data_file: str, output_file: str = "kazanim_graph.html") -> Dict[str, int]:
    return _generate_graph(data_file, output_file)


def get_graph_data(data_file: str) -> Tuple[List[Dict], List[Dict]]:
    return _get_graph_data(data_file)
