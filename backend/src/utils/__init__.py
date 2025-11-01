# -*- coding: utf-8 -*-
"""
Utilities package for the graph visualization system.
(Top-level mirror of backend.src.utils for direct src usage.)
"""

from .colors import score_to_color, TYPE_COLORS, TYPE_BASE_RADIUS, clamp01
from .text import esc, trim_label
from .data_loader import load_curriculum_data, validate_record
from .graph_processor import GraphProcessor, create_graph_data
from .template_manager import TemplateManager

__all__ = [
    'score_to_color', 'TYPE_COLORS', 'TYPE_BASE_RADIUS', 'clamp01',
    'esc', 'trim_label',
    'load_curriculum_data', 'validate_record',
    'GraphProcessor', 'create_graph_data',
    'TemplateManager'
]
