#!/usr/bin/env python3
"""
QR Generator Dependencies Checker
Checks if all required dependencies are installed and offers to install missing ones.
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def get_requirements_path():
    """Get the path to requirements.txt file."""
    # Check if we're in root directory
    if os.path.exists("getDEVUID/requirements.txt"):
        return "getDEVUID/requirements.txt"
    # Check if we're in getDEVUID directory
    elif os.path.exists("requirements.txt"):
        return "requirements.txt"
    else:
        print("❌ Error: requirements.txt not found!")
        print("   Please run this script from the project root directory or getDEVUID directory.")
        return None

def parse_requirements(requirements_path):
    """Parse requirements.txt and extract package names and versions."""
    requirements = []
    
    try:
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle different requirement formats
                    if '>=' in line:
                        package = line.split('>=')[0]
                        version = line.split('>=')[1]
                    elif '==' in line:
                        package = line.split('==')[0]
                        version = line.split('==')[1]
                    elif '>' in line:
                        package = line.split('>')[0]
                        version = line.split('>')[1]
                    else:
                        package = line
                        version = None
                    
                    # Handle special cases like qrcode[pil]
                    if '[' in package:
                        package = package.split('[')[0]
                    
                    requirements.append({
                        'name': package,
                        'version': version,
                        'original': line
                    })
    
    except FileNotFoundError:
        print(f"❌ Error: Could not find {requirements_path}")
        return None
    
    return requirements

def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        # Some packages have different import names
        import_aliases = {
            'pillow': 'PIL',
            'pil': 'PIL',
            'openpyxl': 'openpyxl'
        }
        
        if package_name.lower() in import_aliases:
            try:
                importlib.import_module(import_aliases[package_name.lower()])
                return True
            except ImportError:
                pass
        
        return False

def get_installed_version(package_name):
    """Get the installed version of a package."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', package_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split('Version:')[1].strip()
    except:
        pass
    return None

def install_packages(missing_packages):
    """Install missing packages."""
    if not missing_packages:
        return True
    
    print(f"\n🔧 Installing {len(missing_packages)} missing packages...")
    
    try:
        cmd = [sys.executable, '-m', 'pip', 'install'] + [pkg['original'] for pkg in missing_packages]
        print(f"   Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            print("✅ All packages installed successfully!")
            return True
        else:
            print("❌ Installation failed!")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed with error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during installation: {e}")
        return False

def main():
    """Main function to check dependencies."""
    print("🔍 QR Generator Dependencies Checker")
    print("=" * 40)
    
    # Get requirements file path
    requirements_path = get_requirements_path()
    if not requirements_path:
        sys.exit(1)
    
    print(f"📋 Reading requirements from: {requirements_path}")
    
    # Parse requirements
    requirements = parse_requirements(requirements_path)
    if not requirements:
        sys.exit(1)
    
    print(f"📦 Found {len(requirements)} required packages")
    print()
    
    # Check each package
    missing_packages = []
    installed_packages = []
    
    for req in requirements:
        package_name = req['name']
        required_version = req['version']
        
        if check_package_installed(package_name):
            installed_version = get_installed_version(package_name)
            installed_packages.append({
                'name': package_name,
                'version': installed_version,
                'required': required_version
            })
            
            version_info = f" (v{installed_version})" if installed_version else ""
            print(f"✅ {package_name}{version_info}")
        else:
            missing_packages.append(req)
            print(f"❌ {package_name} - NOT INSTALLED")
    
    print()
    print("=" * 40)
    
    # Summary
    if missing_packages:
        print(f"📊 Summary: {len(installed_packages)} installed, {len(missing_packages)} missing")
        print()
        print("Missing packages:")
        for pkg in missing_packages:
            print(f"  - {pkg['name']} ({pkg['original']})")
        
        print()
        response = input("🤔 Would you like to install missing packages? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if install_packages(missing_packages):
                print()
                print("🎉 All dependencies are now installed!")
                print("   You can now run the QR Generator:")
                print("   python3 qr.py")
            else:
                print()
                print("❌ Installation failed. Please install manually:")
                print(f"   pip3 install -r {requirements_path}")
                sys.exit(1)
        else:
            print()
            print("⚠️  Missing dependencies detected!")
            print("   Please install them manually:")
            print(f"   pip3 install -r {requirements_path}")
            sys.exit(1)
    else:
        print("🎉 All dependencies are installed!")
        print()
        print("✅ System is ready to run QR Generator")
        print("   Launch with: python3 qr.py")
        
        # Optional: Show installed versions
        print()
        print("📦 Installed packages:")
        for pkg in installed_packages:
            version_info = f" (v{pkg['version']})" if pkg['version'] else ""
            required_info = f" [required: >={pkg['required']}]" if pkg['required'] else ""
            print(f"   {pkg['name']}{version_info}{required_info}")

if __name__ == "__main__":
    main() 