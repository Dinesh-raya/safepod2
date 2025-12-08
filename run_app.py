"""
This script is the main entry point for the Streamlit application.
It ensures that the custom `uuid` module is added to the system path before running the app,
which is crucial for compatibility with Streamlit Cloud.
"""

import sys
import os

def main():
    # The root of the project, which is the 'safepod2' directory.
    # This allows the app to find the custom 'uuid.py' and other modules.
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Add the project root to the Python path. This is the critical step.
    sys.path.insert(0, project_root)
    
    # Always directly import and run the main app to avoid runtime conflicts
    try:
        from app.main import main as app_main
        app_main()
    except Exception as e:
        print(f"Error running app: {e}")
        raise

if __name__ == "__main__":
    main()