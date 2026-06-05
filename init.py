#!/usr/bin/env python
"""
Project initialization script.
Sets up environment, validates configuration, and prepares for deployment.
"""

import os
import sys
import json
from pathlib import Path

def init_project():
    """Initialize project for first-time setup"""
    print("\n" + "="*60)
    print("AI Application Compiler - Project Initialization")
    print("="*60 + "\n")

    # Step 1: Create .env from .env.example if it doesn't exist
    print("[1/5] Setting up environment configuration...")
    env_file = '.env'
    env_example = '.env.example'

    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            # Copy example to .env
            with open(env_example, 'r') as f:
                example_content = f.read()
            with open(env_file, 'w') as f:
                f.write(example_content)
            print(f"  Created {env_file} from {env_example}")
            print(f"  IMPORTANT: Edit {env_file} and set OPENROUTER_API_KEY\n")
        else:
            print(f"  WARNING: {env_example} not found\n")
    else:
        print(f"  {env_file} already exists\n")

    # Step 2: Create required directories
    print("[2/5] Creating required directories...")
    directories = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'build',
        'logs'
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print(f"  Created {len(directories)} directories\n")

    # Step 3: Check for configuration file
    print("[3/5] Checking application structure...")
    required_files = {
        'src/config.py': 'Configuration module',
        'main.py': 'Application entry point',
        'wsgi.py': 'WSGI entry point',
        'vercel.json': 'Vercel configuration'
    }

    missing = []
    for filepath, description in required_files.items():
        if os.path.exists(filepath):
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ {description} - MISSING")
            missing.append(filepath)

    if missing:
        print(f"\n  WARNING: {len(missing)} files missing")
    print()

    # Step 4: Display next steps
    print("[4/5] Next steps:")
    print("  1. Set OPENROUTER_API_KEY in .env file")
    print("  2. Run: python validate.py")
    print("  3. Run: python main.py")
    print("  4. Visit: http://localhost:5000\n")

    # Step 5: Configuration hints
    print("[5/5] Configuration information:")
    print("  Environment: development (set ENVIRONMENT=production for prod)")
    print("  Port: 5000 (set PORT env var to change)")
    print("  Log Level: INFO (set LOG_LEVEL env var to change)")
    print("  Docs: See README.md for detailed setup instructions\n")

    print("="*60)
    print("Initialization complete!")
    print("="*60 + "\n")

    return True


if __name__ == '__main__':
    try:
        success = init_project()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}\n")
        sys.exit(1)
