# -*- coding: utf-8 -*-
"""
API Views for EduGraph curriculum graph visualization.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from pathlib import Path
import json

from src import GraphGenerator, get_graph_data


class GraphDataAPIView(APIView):
    """
    API endpoint that returns complete graph data (nodes and links).
    
    GET /api/graph/data/
    
    Returns:
        {
            "status": "success",
            "data": {
                "nodes": [...],
                "links": [...],
                "metadata": {
                    "total_nodes": int,
                    "total_links": int,
                    "node_types": {...}
                }
            }
        }
    """
    
    def get(self, request):
        try:
            # Load data from the curriculum file
            data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
            nodes, links = get_graph_data(data_file)
            
            # Calculate metadata
            node_types = {}
            for node in nodes:
                node_type = node.get('type', 'unknown')
                node_types[node_type] = node_types.get(node_type, 0) + 1
            
            # Prepare response
            response_data = {
                "status": "success",
                "data": {
                    "nodes": nodes,
                    "links": links,
                    "metadata": {
                        "total_nodes": len(nodes),
                        "total_links": len(links),
                        "node_types": node_types
                    }
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except FileNotFoundError:
            return Response(
                {
                    "status": "error",
                    "message": "Curriculum data file not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GraphNodesAPIView(APIView):
    """
    API endpoint that returns only graph nodes.
    
    GET /api/graph/nodes/
    
    Query parameters:
        - type: Filter nodes by type (e.g., ?type=kazanım)
    
    Returns:
        {
            "status": "success",
            "data": {
                "nodes": [...],
                "count": int
            }
        }
    """
    
    def get(self, request):
        try:
            data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
            nodes, _ = get_graph_data(data_file)
            
            # Filter by type if specified
            node_type = request.query_params.get('type')
            if node_type:
                nodes = [n for n in nodes if n.get('type') == node_type]
            
            return Response(
                {
                    "status": "success",
                    "data": {
                        "nodes": nodes,
                        "count": len(nodes)
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GraphLinksAPIView(APIView):
    """
    API endpoint that returns only graph links.
    
    GET /api/graph/links/
    
    Returns:
        {
            "status": "success",
            "data": {
                "links": [...],
                "count": int
            }
        }
    """
    
    def get(self, request):
        try:
            data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
            _, links = get_graph_data(data_file)
            
            return Response(
                {
                    "status": "success",
                    "data": {
                        "links": links,
                        "count": len(links)
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GraphStatsAPIView(APIView):
    """
    API endpoint that returns graph statistics.
    
    GET /api/graph/stats/
    
    Returns:
        {
            "status": "success",
            "data": {
                "total_nodes": int,
                "total_links": int,
                "node_types": {...},
                "link_types": {...},
                "average_connections": float
            }
        }
    """
    
    def get(self, request):
        try:
            data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
            nodes, links = get_graph_data(data_file)
            
            # Calculate node type distribution
            node_types = {}
            for node in nodes:
                node_type = node.get('type', 'unknown')
                node_types[node_type] = node_types.get(node_type, 0) + 1
            
            # Calculate link type distribution
            link_types = {}
            node_map = {n['id']: n for n in nodes}
            
            for link in links:
                source_node = node_map.get(link['source'])
                target_node = node_map.get(link['target'])
                
                if source_node and target_node:
                    link_key = f"{source_node['type']} → {target_node['type']}"
                    link_types[link_key] = link_types.get(link_key, 0) + 1
            
            # Calculate average connections per node
            avg_connections = (len(links) * 2) / len(nodes) if nodes else 0
            
            return Response(
                {
                    "status": "success",
                    "data": {
                        "total_nodes": len(nodes),
                        "total_links": len(links),
                        "node_types": node_types,
                        "link_types": link_types,
                        "average_connections": round(avg_connections, 2)
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GraphVisualizationView(View):
    """
    View that returns the HTML visualization page.
    
    GET /api/graph/view/
    
    Returns: HTML page with the interactive graph visualization
    """
    
    def get(self, request):
        try:
            # Load and process graph data
            data_file = "shared/curriculum/matematik/matematik_kazanimlari_124_154.json"
            nodes, links = get_graph_data(data_file)
            
            # Prepare data for template
            context = {
                'nodes_json': json.dumps(nodes, ensure_ascii=False),
                'links_json': json.dumps(links, ensure_ascii=False),
            }
            
            # Render using Django template system
            return render(request, 'graph_view.html', context)
            
        except Exception as e:
            return HttpResponse(
                f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>",
                content_type='text/html',
                status=500
            )
