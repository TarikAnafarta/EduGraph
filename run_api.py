# -*- coding: utf-8 -*-
"""
Quick start script to run the EduGraph API server.
"""

import subprocess
import sys
import os


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import django
        import rest_framework
        print("✓ Dependencies installed")
        return True
    except ImportError as e:
        print("✗ Missing dependencies!")
        print(f"  Error: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False


def run_migrations():
    """Run Django migrations."""
    print("\n📦 Running migrations...")
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Migrations completed")
        return True
    else:
        print("✗ Migration failed!")
        print(result.stderr)
        return False


def start_server(port=8000):
    """Start the Django development server."""
    print(f"\n🚀 Starting API server on port {port}...")
    print(f"\nAPI endpoints available at:")
    print(f"  📊 Graph Data:    http://localhost:{port}/api/graph/data/")
    print(f"  📈 Nodes Only:    http://localhost:{port}/api/graph/nodes/")
    print(f"  🔗 Links Only:    http://localhost:{port}/api/graph/links/")
    print(f"  📉 Statistics:    http://localhost:{port}/api/graph/stats/")
    print(f"  🎨 Visualization: http://localhost:{port}/api/graph/view/")
    print(f"\n  🔧 Admin Panel:   http://localhost:{port}/admin/")
    print(f"\nPress Ctrl+C to stop the server.\n")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", f"{port}"])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")


def main():
    """Main function."""
    print("🎓 EduGraph API Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        sys.exit(1)
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
