# -*- coding: utf-8 -*-
"""
Debug script to check if the API is properly configured.
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {path}")
        return False

def check_directory(path, description):
    """Check if a directory exists."""
    if Path(path).is_dir():
        files = list(Path(path).rglob('*'))
        print(f"✅ {description}: {path} ({len(files)} files)")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {path}")
        return False

def main():
    print("🔍 EduGraph API Configuration Check")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    
    print("\n📁 Directory Structure:")
    check_directory(base_dir / "static", "Static files directory")
    check_directory(base_dir / "static" / "css", "CSS directory")
    check_directory(base_dir / "static" / "js", "JavaScript directory")
    check_directory(base_dir / "templates", "Root templates directory")
    check_directory(base_dir / "backend" / "artifacts" / "templates", "Artifacts templates directory")
    
    print("\n📄 Required Files:")
    check_file(base_dir / "static" / "css" / "graph.css", "Graph CSS")
    check_file(base_dir / "static" / "js" / "graph.js", "Graph JavaScript")
    check_file(base_dir / "backend" / "artifacts" / "templates" / "graph_view.html", "Django template")
    check_file(base_dir / "templates" / "graph.html", "Standalone template")
    
    print("\n📦 Data Files:")
    check_file(base_dir / "shared" / "curriculum" / "matematik" / "matematik_kazanimlari_124_154.json", "Curriculum data")
    
    print("\n🔧 Configuration Files:")
    check_file(base_dir / "backend" / "settings.py", "Django settings")
    check_file(base_dir / "backend" / "urls.py", "Main URLs")
    check_file(base_dir / "backend" / "artifacts" / "urls.py", "Artifacts URLs")
    check_file(base_dir / "backend" / "artifacts" / "views.py", "Artifacts views")
    
    print("\n⚙️  Testing Django Configuration:")
    try:
        # Add the project directory to Python path
        sys.path.insert(0, str(base_dir))
        
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"✅ Django initialized")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   STATIC_URL: {settings.STATIC_URL}")
        print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Check if template directories are configured
        for template_config in settings.TEMPLATES:
            print(f"   Template DIRS: {template_config.get('DIRS')}")
            print(f"   Template APP_DIRS: {template_config.get('APP_DIRS')}")
        
        # Check if apps are installed
        print(f"\n📱 Installed Apps:")
        for app in settings.INSTALLED_APPS:
            if 'artifacts' in app or 'rest_framework' in app or 'cors' in app:
                print(f"   ✅ {app}")
        
    except Exception as e:
        print(f"❌ Django configuration error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    print("✨ Configuration check complete!")
    print("\nTo start the server:")
    print("   python run_api.py")
    print("\nThen visit:")
    print("   http://localhost:8000/api/graph/view/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
