#!/usr/bin/env python3
"""
QR Code Generator Launcher
Run this script after executing getDEVUID
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import qrcode
        import PIL
        import tkinter
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        return False

def main():
    print("QR Code Generator Launcher")
    print("=" * 30)
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("Required dependencies not found.")
        install_deps = input("Would you like to install them now? (y/n): ").lower().strip()
        if install_deps == 'y':
            if not install_dependencies():
                return
        else:
            print("Please install dependencies manually and run again.")
            return
    
    # Launch the GUI application
    print("Launching QR Code Generator GUI...")
    try:
        from qr_generator_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Please ensure all files are in the same directory and try again.")

if __name__ == "__main__":
    main() 