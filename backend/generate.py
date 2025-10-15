# -*- coding: utf-8 -*-
"""
Simple graph generator - replaces the old graph.py
"""

from src import generate_graph

# Generate the graph
stats = generate_graph(
    "shared/curriculum/matematik/matematik_kazanimlari_124_154.json",
    "kazanim_graph.html"
)

print(f"✓ Generated: kazanim_graph.html | Nodes: {stats['nodes_count']} | Links: {stats['links_count']}")
