# -*- coding: utf-8 -*-
"""
URL configuration for the artifacts (graph) API.
"""

from django.urls import path
from . import views

app_name = 'artifacts'

urlpatterns = [
    # API endpoints
    path('graph/data/', views.GraphDataAPIView.as_view(), name='graph-data'),
    path('graph/nodes/', views.GraphNodesAPIView.as_view(), name='graph-nodes'),
    path('graph/links/', views.GraphLinksAPIView.as_view(), name='graph-links'),
    path('graph/stats/', views.GraphStatsAPIView.as_view(), name='graph-stats'),
    
    # HTML visualization endpoint
    path('graph/view/', views.GraphVisualizationView.as_view(), name='graph-view'),
]
