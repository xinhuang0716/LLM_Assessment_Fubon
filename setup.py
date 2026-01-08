#!/usr/bin/env python3
"""
Setup script for the Integrated LLM Assessment Framework
Helps install dependencies for all modules
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"Directory: {cwd or 'current'}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def main():
    root_dir = Path(__file__).parent
    
    print("\n" + "="*60)
    print("🚀 LLM Assessment Framework - Dependency Installation")
    print("="*60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"\n✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    # Install explainability dependencies
    print("\n\n📦 Installing Explainability module dependencies...")
    exp_dir = root_dir / "explainability"
    if (exp_dir / "requirements.txt").exists():
        success = run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=str(exp_dir)
        )
        if success:
            print("✅ Explainability dependencies installed")
        else:
            print("⚠️  Failed to install Explainability dependencies")
    else:
        print("⚠️  requirements.txt not found in explainability/")
    
    # Install reliability/ceval dependencies
    print("\n\n📦 Installing Reliability (C-Eval) module dependencies...")
    ceval_dir = root_dir / "reliability" / "ceval"
    if (ceval_dir / "requirements.txt").exists():
        success = run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=str(ceval_dir)
        )
        if success:
            print("✅ C-Eval dependencies installed")
        else:
            print("⚠️  Failed to install C-Eval dependencies")
    else:
        print("⚠️  requirements.txt not found in reliability/ceval/")
    
    # Install reliability/consistency dependencies
    print("\n\n📦 Installing Reliability (Consistency) module dependencies...")
    consistency_dir = root_dir / "reliability" / "consistency"
    if (consistency_dir / "requirements.txt").exists():
        success = run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=str(consistency_dir)
        )
        if success:
            print("✅ Consistency dependencies installed")
        else:
            print("⚠️  Failed to install Consistency dependencies")
    else:
        print("⚠️  requirements.txt not found in reliability/consistency/")
    
    # Install safety dependencies (using uv)
    print("\n\n📦 Installing Safety module dependencies...")
    safety_dir = root_dir / "safety"
    
    # Check if uv is installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        uv_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        uv_installed = False
    
    if uv_installed:
        if (safety_dir / "pyproject.toml").exists():
            success = run_command(
                ["uv", "sync"],
                cwd=str(safety_dir)
            )
            if success:
                print("✅ Safety dependencies installed")
            else:
                print("⚠️  Failed to install Safety dependencies")
        else:
            print("⚠️  pyproject.toml not found in safety/")
    else:
        print("⚠️  'uv' is not installed. Please install it first:")
        print("     curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("     or visit: https://github.com/astral-sh/uv")
    
    # Summary
    print("\n\n" + "="*60)
    print("📋 Installation Summary")
    print("="*60)
    print("\n✅ Setup complete!")
    print("\n📝 Next steps:")
    print("   1. Edit config.json with your API keys and settings")
    print("   2. Run: python main.py")
    print("   3. Check results/ directory for outputs")
    print("\n📚 For more information, see INTEGRATION_README.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
