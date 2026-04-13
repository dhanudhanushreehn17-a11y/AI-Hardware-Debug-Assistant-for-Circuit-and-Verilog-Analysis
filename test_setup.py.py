"""
Test script to verify the AI Hardware Debug Assistant setup
Run this script before starting the main application
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("  ✓ Streamlit")
    except ImportError:
        print("  ✗ Streamlit - Run: pip install streamlit")
        return False
    
    try:
        import requests
        print("  ✓ Requests")
    except ImportError:
        print("  ✗ Requests - Run: pip install requests")
        return False
    
    try:
        import PIL
        print("  ✓ Pillow")
    except ImportError:
        print("  ✗ Pillow - Run: pip install Pillow")
        return False
    
    return True


def test_opencode_connection():
    """Test connection to OpenCode server"""
    print("\nTesting OpenCode connection...")
    
    import requests
    
    try:
        response = requests.get("http://localhost:8080/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"  ✓ OpenCode connected")
            print(f"    Available models: {len(models)}")
            for model in models[:5]:  # Show first 5 models
                print(f"    - {model.get('name', 'Unknown')}")
            if len(models) > 5:
                print(f"    ... and {len(models) - 5} more")
            return True
        else:
            print(f"  ✗ OpenCode returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ✗ Cannot connect to OpenCode")
        print("    Make sure OpenCode is running: opencode serve")
        return False
    except requests.exceptions.Timeout:
        print("  ✗ OpenCode connection timed out")
        return False


def test_opencode_models():
    """Check if required models are available"""
    print("\nChecking required models...")
    
    import requests
    
    required_models = ["llava", "codellama"]
    
    try:
        response = requests.get("http://localhost:8080/api/tags", timeout=5)
        data = response.json()
        available_models = [m.get("name", "") for m in data.get("models", [])]
        
        all_found = True
        for model in required_models:
            found = any(model in m for m in available_models)
            if found:
                print(f"  ✓ {model} model available")
            else:
                print(f"  ✗ {model} model not found")
                print(f"    Run: opencode pull {model}")
                all_found = False
        
        return all_found
    except:
        print("  (Could not check models)")
        return True


def main():
    print("=" * 50)
    print("AI Hardware Debug Assistant - Setup Test")
    print("=" * 50)
    
    print("\n--- Package Tests ---")
    packages_ok = test_imports()
    
    print("\n--- OpenCode Tests ---")
    opencode_ok = test_opencode_connection()
    
    if opencode_ok:
        models_ok = test_opencode_models()
    else:
        models_ok = False
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    if packages_ok and opencode_ok and models_ok:
        print("✓ All tests passed!")
        print("  You can now run: streamlit run app.py")
        return 0
    else:
        print("✗ Some tests failed")
        print("  Please fix the issues above before running the app")
        return 1


if __name__ == "__main__":
    sys.exit(main())
