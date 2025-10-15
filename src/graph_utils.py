# -*- coding: utf-8 -*-
"""
Main graph utility module.
Provides a simple interface for generating curriculum graphs.
"""

from typing import List, Dict, Any, Tuple
from .utils.data_loader import load_curriculum_data, validate_record
from .utils.graph_processor import create_graph_data
from .utils.template_manager import TemplateManager


class GraphGenerator:
    """Main class for generating curriculum graphs."""

    def __init__(self, template_dir: str = "templates"):
        self.template_manager = TemplateManager(template_dir)

    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        records = load_curriculum_data(file_path)
        return [r for r in records if validate_record(r)]

    def create_graph_data(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
        return create_graph_data(records)

    def render(self, nodes: List[Dict[str, Any]], links: List[Dict[str, Any]]) -> str:
        return self.template_manager.render_graph_html(nodes, links, template_name="graph.html")

    # keep backwards-compatible alias used in README
    def generate_html(self, nodes: List[Dict[str, Any]], links: List[Dict[str, Any]]) -> str:
        return self.render(nodes, links)

    def save(self, html_content: str, output_file: str) -> None:
        self.template_manager.save_html(html_content, output_file)

    def generate_from_file(self, data_file: str, output_file: str = "kazanim_graph.html") -> Tuple[str, Dict[str, int]]:
        records = self.load_data(data_file)
        nodes, links = self.create_graph_data(records)
        html = self.render(nodes, links)
        self.save(html, output_file)
        stats = {
            "nodes_count": len(nodes),
            "links_count": len(links),
            "records_processed": len(records),
        }
        return html, stats


# Convenience functions for backward compatibility

def generate_graph(data_file: str, output_file: str = "kazanim_graph.html") -> Dict[str, int]:
    html, stats = GraphGenerator().generate_from_file(data_file, output_file)
    return stats


def get_graph_data(data_file: str) -> Tuple[List[Dict], List[Dict]]:
    records = GraphGenerator().load_data(data_file)
    return create_graph_data(records)
