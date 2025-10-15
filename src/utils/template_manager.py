# -*- coding: utf-8 -*-
"""
Template management utilities for rendering HTML with graph data.
"""
from pathlib import Path
from typing import List, Dict, Any
import json


class TemplateManager:
    """Manages HTML template rendering with graph data."""

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)

    def render_graph_html(self, nodes: List[Dict[str, Any]], links: List[Dict[str, Any]],
                          template_name: str = "graph.html") -> str:
        """Render the graph HTML template with nodes and links data."""
        template_path = self.template_dir / template_name
        html = template_path.read_text(encoding="utf-8")

        nodes_json = json.dumps(nodes, ensure_ascii=False)
        links_json = json.dumps(links, ensure_ascii=False)

        # Support both raw and commented placeholders
        replacements = {
            "{{NODES}}": nodes_json,
            "{{LINKS}}": links_json,
        }
        for k, v in replacements.items():
            if k in html:
                html = html.replace(k, v)

        return html

    def save_html(self, html_content: str, output_path: str) -> None:
        out = Path(output_path)
        out.write_text(html_content, encoding="utf-8")
