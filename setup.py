#!/usr/bin/env python3
"""
Automated bootstrap, Git configuration, dependency setup, and Google Drive integration for Agentic Wiki Builder.
"""

import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, check=True, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=check, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if check:
            sys.exit(1)

def setup_google_drive(root, venv_python):
    gdrive_dir = root / ".agents" / "mcp" / "gdrive"
    service_account_path = gdrive_dir / "service_account.json"
    credentials_path = gdrive_dir / "credentials.json"
    token_path = gdrive_dir / "token.json"

    print("=" * 60)
    print("      Google Drive MCP Server Credentials Setup")
    print("=" * 60)
    print()
    print("This guide will help you set up credentials for the read-only")
    print("Google Drive MCP server.")
    print()
    print("Please choose your preferred authentication method:")
    print("  [1] Google Service Account (Recommended for automated/non-interactive workflows)")
    print("  [2] Google OAuth 2.0 Client (Recommended for accessing your personal/workspace drive)")
    print("  [3] Skip/Done (Already configured or set up later)")
    print()
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    if choice == "3":
        print("Skipping Google Drive credentials setup.")
        return
    elif choice not in ("1", "2"):
        print("Invalid choice. Skipping.")
        return
        
    print()
    if choice == "1":
        print("--- Google Service Account Setup ---")
        print(f"Please place your downloaded Service Account JSON key file at:")
        print(f"  {service_account_path}")
        print()
        print("Steps to obtain this key:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Enable the Google Drive API for your project")
        print("3. Go to IAM & Admin > Service Accounts > Create Service Account")
        print("4. Select the created Service Account, go to Keys > Add Key > Create new key (JSON)")
        print("5. Share the Google Drive folders/files you want to read with the service account's email address.")
        print()
        
        if service_account_path.exists():
            print("✓ Success! service_account.json detected in .agents/mcp/gdrive/")
        else:
            print("Status: Pending. Please add the file and run setup.py again when ready.")
            
    else:
        print("--- Google OAuth 2.0 Setup ---")
        if token_path.exists():
            print("✓ OAuth token.json already exists! No action needed.")
            return
            
        if not credentials_path.exists():
            print(f"Please download your OAuth client credentials JSON and place it at:")
            print(f"  {credentials_path}")
            print()
            print("Steps to obtain this credentials file:")
            print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
            print("2. Enable the Google Drive API for your project")
            print("3. Go to APIs & Services > OAuth consent screen (configure Internal or External)")
            print("4. Go to Credentials > Create Credentials > OAuth client ID (Select Application type: Desktop app)")
            print("5. Download the client secret JSON file, rename it to credentials.json, and save it to the path above.")
            print()
            print("Please run setup.py again after placing credentials.json.")
            return
            
        print("✓ credentials.json detected! Starting the interactive authorization flow...")
        print("This will open a browser window for you to login and authorize read-only access.")
        input("Press Enter to start the flow...")
        print()
        
        try:
            cmd_python = str(venv_python) if venv_python.exists() else "python3"
            run_command([cmd_python, str(gdrive_dir / "server.py"), "--auth"])
            print()
            print("✓ OAuth Setup Completed successfully!")
        except Exception as e:
            print(f"Error executing auth flow: {e}")

def main():
    print("=" * 60)
    print("  Agentic Wiki Builder — Complete Setup & Bootstrap")
    print("=" * 60)
    print()

    # 1. Git LFS Initialization
    if not shutil.which("git-lfs"):
        print("⚠️  WARNING: 'git-lfs' command not found.")
        print("   Please install Git LFS (https://git-lfs.com/) for tracking large raw sources.")
        print()
    else:
        print("✓ Git LFS found. Registering settings...")
        run_command(["git", "lfs", "install"])
        print()

    # 2. Submodule Initialization
    print("✓ Initializing and updating git submodules...")
    run_command(["git", "-c", "protocol.file.allow=always", "submodule", "update", "--init", "--recursive"], check=False)
    print()

    # 3. Configure Git Submodule recurse & automatic push behaviors
    print("✓ Configuring local Git settings for seamless team collaboration...")
    
    # Enable recursive pulling: git pull automatically fetches submodule updates
    run_command(["git", "config", "submodule.recurse", "true"])
    
    # Enable on-demand recursive pushing: git push from parent automatically pushes dirty submodules
    run_command(["git", "config", "push.recurseSubmodules", "on-demand"])
    print()

    # 4. Virtual Environment Creation
    root = Path(__file__).resolve().parent
    venv_dir = root / ".venv"
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    if not venv_dir.exists():
        print("✓ Creating Python virtual environment (.venv)...")
        run_command([sys.executable, "-m", "venv", str(venv_dir)])
    else:
        print("✓ Python virtual environment (.venv) already exists.")
    print()

    # 5. Installing Dependencies
    print("✓ Installing and updating dependencies from requirements.txt...")
    if venv_pip.exists():
        run_command([str(venv_pip), "install", "--upgrade", "pip"])
        run_command([str(venv_pip), "install", "-r", "requirements.txt"])
    else:
        print("⚠️  Could not find pip in virtual environment. Attempting fallback setup...")
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print()

    # 6. Environment Configuration (.env)
    env_file = root / ".env"
    example_env_file = root / ".example.env"
    if not env_file.exists():
        if example_env_file.exists():
            print("✓ Creating .env file from .example.env...")
            shutil.copy(example_env_file, env_file)
            print("👉 Created .env file. Please update it with your API credentials if necessary.")
        else:
            print("⚠️  Could not find .example.env to generate .env.")
    else:
        print("✓ .env file already exists.")
    print()

    # 7. Google Drive Credentials Setup
    try:
        setup_google_drive(root, venv_python)
    except Exception as e:
        print(f"⚠️  Google Drive credentials setup encountered an issue: {e}")
    print()

    print("=" * 60)
    print("✓ Setup Complete!")
    print("- Submodules will now automatically pull updates during a standard 'git pull'.")
    print("- Commits in submodules will automatically push when you run 'git push' from the parent repository.")
    print("- Virtual environment is configured and dependencies are installed.")
    print("- Environment (.env) has been prepared.")
    print("=" * 60)

if __name__ == "__main__":
    main()
