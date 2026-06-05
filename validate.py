#!/usr/bin/env python
"""
Startup validation script for the AI Application Compiler.
Runs environment and configuration checks before starting the server.
"""

import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config

logger = logging.getLogger(__name__)


def validate_environment():
    """Validate all environment variables and configuration"""
    print("\n" + "="*60)
    print("AI Application Compiler - Startup Validation")
    print("="*60 + "\n")

    # Check configuration
    print("[1/4] Validating configuration...")
    is_valid, errors = Config.validate()

    if not is_valid:
        print("ERROR: Configuration validation failed!\n")
        for error in errors:
            print(f"  - {error}")
        return False

    print("  OK: Configuration is valid\n")

    # Check required files
    print("[2/4] Checking required files...")
    required_files = [
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print("WARNING: Missing frontend files:")
        for file in missing:
            print(f"  - {file}")
        print()
    else:
        print("  OK: All required files present\n")

    # Check Python packages
    print("[3/4] Checking Python dependencies...")
    required_packages = [
        'flask',
        'flask_cors',
        'openai',
        'pydantic',
        'python_dotenv'
    ]

    try:
        for package in required_packages:
            __import__(package.replace('_', '-').replace('-', '_'))
        print("  OK: All dependencies installed\n")
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}\n")
        return False

    # Display configuration
    print("[4/4] Configuration summary:")
    config_dict = Config.to_dict()
    for key, value in config_dict.items():
        print(f"  {key}: {value}")
    print()

    print("="*60)
    print("All validation checks passed!")
    print("="*60 + "\n")

    return True


if __name__ == '__main__':
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )

    # Run validation
    success = validate_environment()

    if not success:
        sys.exit(1)
