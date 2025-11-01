# -*- coding: utf-8 -*-
"""
Tests for the graph API views.
"""

from django.test import TestCase, Client
from django.urls import reverse
import json


class GraphAPITestCase(TestCase):
    """Test cases for the graph API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_graph_data_endpoint(self):
        """Test the complete graph data endpoint."""
        url = reverse('artifacts:graph-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIn('nodes', data['data'])
        self.assertIn('links', data['data'])
        self.assertIn('metadata', data['data'])
        
        # Check metadata structure
        metadata = data['data']['metadata']
        self.assertIn('total_nodes', metadata)
        self.assertIn('total_links', metadata)
        self.assertIn('node_types', metadata)
        
        # Verify counts match
        self.assertEqual(metadata['total_nodes'], len(data['data']['nodes']))
        self.assertEqual(metadata['total_links'], len(data['data']['links']))
    
    def test_graph_nodes_endpoint(self):
        """Test the nodes-only endpoint."""
        url = reverse('artifacts:graph-nodes')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['status'], 'success')
        self.assertIn('nodes', data['data'])
        self.assertIn('count', data['data'])
        self.assertEqual(data['data']['count'], len(data['data']['nodes']))
    
    def test_graph_nodes_filtered_by_type(self):
        """Test filtering nodes by type."""
        url = reverse('artifacts:graph-nodes')
        response = self.client.get(url, {'type': 'kazanım'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify all returned nodes are of the requested type
        for node in data['data']['nodes']:
            self.assertEqual(node['type'], 'kazanım')
    
    def test_graph_links_endpoint(self):
        """Test the links-only endpoint."""
        url = reverse('artifacts:graph-links')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['status'], 'success')
        self.assertIn('links', data['data'])
        self.assertIn('count', data['data'])
        self.assertEqual(data['data']['count'], len(data['data']['links']))
        
        # Verify link structure
        if data['data']['links']:
            link = data['data']['links'][0]
            self.assertIn('source', link)
            self.assertIn('target', link)
    
    def test_graph_stats_endpoint(self):
        """Test the statistics endpoint."""
        url = reverse('artifacts:graph-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['status'], 'success')
        stats = data['data']
        
        self.assertIn('total_nodes', stats)
        self.assertIn('total_links', stats)
        self.assertIn('node_types', stats)
        self.assertIn('link_types', stats)
        self.assertIn('average_connections', stats)
        
        # Verify statistics are numeric
        self.assertIsInstance(stats['total_nodes'], int)
        self.assertIsInstance(stats['total_links'], int)
        self.assertIsInstance(stats['average_connections'], (int, float))
    
    def test_graph_visualization_endpoint(self):
        """Test the HTML visualization endpoint."""
        url = reverse('artifacts:graph-view')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html')
        
        # Verify HTML content contains expected elements
        html_content = response.content.decode('utf-8')
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('</html>', html_content)
