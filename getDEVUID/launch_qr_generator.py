#!/usr/bin/env python3
"""
QR Code Generator Launcher
Run this script after getDEVUID to launch the QR code generator GUI
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import qrcode
        import PIL
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages with: pip install -r requirements.txt")
        return False

def main():
    print("QR Code Generator Launcher")
    print("=" * 30)
    
    # Check if dependencies are installed
    if not check_dependencies():
        sys.exit(1)
    
    # Try GUI first, fallback to CLI
    try:
        import tkinter
        from qr_generator_gui import main as gui_main
        print("Launching QR Code Generator GUI...")
        gui_main()
    except ImportError:
        print("GUI not available (tkinter missing), launching CLI version...")
        from qr_generator_cli import main as cli_main
        cli_main()
    except Exception as e:
        print(f"Error launching application: {e}")
        print("Falling back to CLI version...")
        try:
            from qr_generator_cli import main as cli_main
            cli_main()
        except Exception as e2:
            print(f"Error launching CLI: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main() 