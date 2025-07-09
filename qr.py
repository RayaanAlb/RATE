#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the getDEVUID directory
    getdevuid_dir = os.path.join(script_dir, 'getDEVUID')
    
    # Path to the QR generator GUI script
    gui_script = os.path.join(getdevuid_dir, 'qr_generator_gui.py')
    
    # Check if the GUI script exists
    if not os.path.exists(gui_script):
        print(f"❌ Error: QR Generator GUI not found at {gui_script}")
        sys.exit(1)
    
    # Change to the getDEVUID directory and run the GUI
    try:
        os.chdir(getdevuid_dir)
        subprocess.run([sys.executable, 'qr_generator_gui.py'])
    except Exception as e:
        print(f"❌ Error launching QR Generator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 