# -*- coding: utf-8 -*-
"""
Test script to verify the EduGraph API endpoints.
Make sure the application is running first: docker-compose up -d
"""

import requests
import json
import sys


def test_endpoint(url, name, description):
    """Test a single API endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {url}")
    print(f"Description: {description}")
    print('='*60)
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS")
            
            # Pretty print a sample of the data
            if isinstance(data, dict):
                if 'status' in data:
                    print(f"   Status: {data['status']}")
                if 'data' in data:
                    if isinstance(data['data'], dict):
                        for key, value in data['data'].items():
                            if isinstance(value, list):
                                print(f"   {key}: {len(value)} items")
                            elif isinstance(value, dict):
                                print(f"   {key}: {json.dumps(value, indent=6)}")
                            else:
                                print(f"   {key}: {value}")
            
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Could not connect to server")
        print("   Make sure the application is running: docker-compose up -d")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def main():
    """Run all API tests."""
    print("🧪 EduGraph API Test Suite")
    print("="*60)
    print("Testing API endpoints at http://localhost:8000")
    
    base_url = "http://localhost:8000/api"
    
    tests = [
        (
            f"{base_url}/graph/data/",
            "Complete Graph Data",
            "Returns all nodes, links, and metadata"
        ),
        (
            f"{base_url}/graph/nodes/",
            "Graph Nodes",
            "Returns all graph nodes"
        ),
        (
            f"{base_url}/graph/nodes/?type=kazanım",
            "Filtered Nodes (kazanım)",
            "Returns nodes filtered by type"
        ),
        (
            f"{base_url}/graph/links/",
            "Graph Links",
            "Returns all graph connections"
        ),
        (
            f"{base_url}/graph/stats/",
            "Graph Statistics",
            "Returns statistical information"
        ),
        (
            f"{base_url}/graph/view/",
            "Interactive Visualization",
            "Returns HTML visualization page"
        ),
    ]
    
    results = []
    for url, name, description in tests:
        result = test_endpoint(url, name, description)
        results.append((name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
