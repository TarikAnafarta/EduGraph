# -*- coding: utf-8 -*-
"""
Quick script to open the graph visualization in your default browser.
Make sure the API server is running first (python run_api.py).
"""

import webbrowser
import time
import sys

try:
    import requests
except ImportError:
    print("⚠️  'requests' package not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


def check_server():
    """Check if the API server is running."""
    try:
        response = requests.get("http://localhost:8000/api/graph/stats/", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    print("🌐 Opening EduGraph Visualization...")
    print("=" * 50)
    
    # Check if server is running
    if not check_server():
        print("⚠️  API server is not running!")
        print("\nPlease start the server first:")
        print("   python run_api.py")
        print("\nOr run this command in a separate terminal and try again.")
        return 1
    
    print("✅ Server is running")
    print("📊 Opening visualization in your default browser...")
    
    # Open the visualization
    url = "http://localhost:8000/api/graph/view/"
    webbrowser.open(url)
    
    print(f"\n✨ Opened: {url}")
    print("\nOther available endpoints:")
    print("   📊 Graph Data:    http://localhost:8000/api/graph/data/")
    print("   📈 Nodes:         http://localhost:8000/api/graph/nodes/")
    print("   🔗 Links:         http://localhost:8000/api/graph/links/")
    print("   📉 Statistics:    http://localhost:8000/api/graph/stats/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
