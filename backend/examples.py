# -*- coding: utf-8 -*-
"""
Example: Using EduGraph as a utility for web applications.
Shows how to integrate with Flask, FastAPI, or other web frameworks.
"""

from src import GraphGenerator, get_graph_data
import json

def example_api_endpoint():
    """Example of how you might use this in a web API."""
    
    print("🌐 Example: API Endpoint Usage")
    print("=" * 40)
    
    # Get graph data for API response
    nodes, links = get_graph_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
    
    # Create API response format
    api_response = {
        "status": "success",
        "data": {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_nodes": len(nodes),
                "total_links": len(links),
                "node_types": {}
            }
        }
    }
    
    # Add node type counts to metadata
    for node in nodes:
        node_type = node.get('type', 'unknown')
        api_response["data"]["metadata"]["node_types"][node_type] = \
            api_response["data"]["metadata"]["node_types"].get(node_type, 0) + 1
    
    print(f"📊 API Response Structure:")
    print(f"   Nodes: {api_response['data']['metadata']['total_nodes']}")
    print(f"   Links: {api_response['data']['metadata']['total_links']}")
    print(f"   Node Types: {api_response['data']['metadata']['node_types']}")
    
    return api_response

def example_custom_template():
    """Render using the default template directory (templates/)."""
    gen = GraphGenerator()  # uses templates/
    records_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
    records = gen.load_data(records_file)
    nodes, links = gen.create_graph_data(records)
    html = gen.render(nodes, links)
    gen.save(html, "kazanim_graph.html")
    print("Saved HTML using default template.")

def example_data_analysis():
    """Do a quick analysis of dataset sizes."""
    gen = GraphGenerator()
    records = gen.load_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
    print("Records:", len(records))

def example_export_formats():
    """Show how to export nodes/links as JSON for other frontends."""
    nodes, links = get_graph_data("shared/curriculum/matematik/matematik_kazanimlari_124_154.json")
    import json
    print(json.dumps({"nodes": nodes, "links": links})[:200] + "…")

def main():
    """Run all examples."""
    
    print("🔧 EduGraph Utility Examples")
    print("=" * 50)
    
    # Run examples
    api_data = example_api_endpoint()
    react_data = example_custom_template()
    example_data_analysis()
    example_export_formats()
    
    print("\n✨ All examples completed!")
    print("\n💡 These examples show how to use EduGraph as a utility library")
    print("   in different contexts like web APIs, React apps, data analysis, etc.")

if __name__ == "__main__":
    main()
