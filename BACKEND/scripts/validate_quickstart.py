"""
Quickstart validation script
This script validates that the implementation matches the quickstart guide
"""
import asyncio
import subprocess
import sys
import os
from pathlib import Path

async def validate_setup():
    """Validate the setup instructions from quickstart.md"""
    print("Validating setup...")
    
    # Check if Python 3.11+ is available
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print(f"❌ Python 3.11+ required, found {python_version.major}.{python_version.minor}")
        return False
    else:
        print(f"✅ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is valid")
    
    # Check if required dependencies are available
    dependencies = ["fastapi", "uvicorn", "cohere", "qdrant-client", "asyncpg", "pydantic", "python-dotenv", "pytest"]
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))  # Convert package names with dashes to underscores
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {missing_deps}")
        return False
    else:
        print("✅ All dependencies are available")
    
    # Check if .env file exists and has required variables
    env_file_path = Path("backend/.env")
    if not env_file_path.exists():
        print("⚠️  .env file does not exist (this may be expected in some deployments)")
    else:
        with open(env_file_path, 'r') as f:
            env_content = f.read()
        
        required_vars = ["COHERE_API_KEY", "QDRANT_API_KEY", "QDRANT_CLUSTER_ENDPOINT", "NEON_DB_URL"]
        missing_vars = []
        
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing environment variables in .env: {missing_vars}")
        else:
            print("✅ All required environment variables are present in .env")
    
    print("✅ Setup validation passed")
    return True

async def validate_basic_functionality():
    """Validate basic functionality as described in quickstart.md"""
    print("\nValidating basic functionality...")
    
    # Test if the main application can be imported without errors
    try:
        # Change to the backend directory to import the main app
        original_cwd = os.getcwd()
        os.chdir("backend")
        
        # Temporarily add the backend/src to the path to import modules
        sys.path.insert(0, os.path.join(os.getcwd(), "src"))
        
        from src.api.main import app
        print("✅ Main application can be imported without errors")
        
        # Restore the original working directory and path
        os.chdir(original_cwd)
        sys.path.pop(0)
        
    except ImportError as e:
        print(f"❌ Failed to import main application: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during import validation: {e}")
        return False
    
    # Check if required directories exist
    required_dirs = [
        "backend/src/models",
        "backend/src/services", 
        "backend/src/api",
        "backend/src/utils",
        "backend/src/db",
        "backend/tests/unit",
        "backend/tests/integration",
        "backend/tests/contract"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing required directories: {missing_dirs}")
        return False
    else:
        print("✅ All required directories exist")
    
    print("✅ Basic functionality validation passed")
    return True

async def validate_api_endpoints():
    """Validate that the API endpoints match the quickstart examples"""
    print("\nValidating API endpoints...")
    
    # Import and check the main app routes
    try:
        original_cwd = os.getcwd()
        os.chdir("backend")
        sys.path.insert(0, os.path.join(os.getcwd(), "src"))
        
        from src.api.main import app
        from src.api import book_routes, query_routes, history_routes
        
        # Check if the expected routes exist
        expected_routes = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/status", "GET"),
            ("/api/v1/books", "POST"),
            ("/api/v1/books/{book_id}", "GET"),
            ("/api/v1/books", "GET"),
            ("/api/v1/query", "POST"),
            ("/api/v1/query/validate", "POST"),
            ("/api/v1/history", "GET"),
            ("/api/v1/history/{query_id}/feedback", "POST")
        ]
        
        found_routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                for method in route.methods:
                    found_routes.append((route.path, method))
        
        missing_routes = []
        for expected_route, expected_method in expected_routes:
            if (expected_route, expected_method) not in found_routes:
                missing_routes.append((expected_route, expected_method))
        
        if missing_routes:
            print(f"❌ Missing expected routes: {missing_routes}")
            return False
        else:
            print("✅ All expected API routes are available")
        
        os.chdir(original_cwd)
        sys.path.pop(0)
        
    except Exception as e:
        print(f"❌ Error validating API endpoints: {e}")
        return False
    
    print("✅ API endpoints validation passed")
    return True

async def main():
    """Main validation function"""
    print("Running quickstart validation...")
    print("="*50)
    
    all_passed = True
    
    # Run all validation steps
    all_passed &= await validate_setup()
    all_passed &= await validate_basic_functionality()
    all_passed &= await validate_api_endpoints()
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All validations passed! The implementation matches the quickstart guide.")
        return 0
    else:
        print("❌ Some validations failed. Please check the implementation against the quickstart guide.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)