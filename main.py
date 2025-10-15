# -*- coding: utf-8 -*-
"""
Modern main entry point for EduGraph.
Demonstrates how to use the modular architecture.
"""

from src import GraphGenerator, get_graph_data
import json

def main():
    """Main function demonstrating the new modular architecture."""
    
    # Configuration
    data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
    output_file = "kazanim_graph.html"
    
    print("🚀 EduGraph - Curriculum Learning Graph Generator")
    print("=" * 50)
    
    # Method 1: Simple generation (backward compatible)
    print("📊 Generating graph using simple method...")
    generator = GraphGenerator()
    html_content, stats = generator.generate_from_file(data_file, output_file)
    
    print(f"✅ Generated: {output_file}")
    print(f"   📈 Nodes: {stats['nodes_count']}")
    print(f"   🔗 Links: {stats['links_count']}")
    print(f"   📋 Records processed: {stats['records_processed']}")
    
    # Method 2: Get just the data (for API usage)
    print("\n🔧 Getting graph data for API usage...")
    nodes, links = get_graph_data(data_file)
    
    print(f"✅ Data extracted:")
    print(f"   📈 Nodes: {len(nodes)}")
    print(f"   🔗 Links: {len(links)}")
    
    # Method 3: Step by step (for custom processing)
    print("\n⚙️  Step-by-step processing...")
    generator = GraphGenerator()
    
    # Load data
    records = generator.load_data(data_file)
    print(f"📥 Loaded {len(records)} records")
    
    # Process into graph
    nodes, links = generator.create_graph_data(records)
    print(f"🔄 Processed into {len(nodes)} nodes and {len(links)} links")
    
    # Generate custom HTML (could customize template here)
    custom_html = generator.generate_html(nodes, links)
    print(f"🎨 Generated HTML ({len(custom_html)} characters)")
    
    print("\n🎯 Example: Working with the data programmatically")
    # Example: Show node type distribution
    node_types = {}
    for node in nodes:
      node_type = node.get('type', 'unknown')
      node_types[node_type] = node_types.get(node_type, 0) + 1
    
    print("📊 Node distribution:")
    for node_type, count in sorted(node_types.items()):
      print(f"   {node_type}: {count}")
    
    # Example: Show links between different types
    link_types = {}
    for link in links:
      source_node = next((n for n in nodes if n['id'] == link['source']), None)
      target_node = next((n for n in nodes if n['id'] == link['target']), None)
      
      if source_node and target_node:
        link_key = f"{source_node['type']} → {target_node['type']}"
        link_types[link_key] = link_types.get(link_key, 0) + 1
    
    print("\n🔗 Link distribution:")
    for link_type, count in sorted(link_types.items()):
      if count > 0:  # Only show existing link types
        print(f"   {link_type}: {count}")
    
    print(f"\n✨ All done! Open {output_file} in your browser to view the graph.")

if __name__ == "__main__":
    main()
