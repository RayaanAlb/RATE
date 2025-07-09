#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

def main():
    # Define South African timezone (SAST = GMT+2)
    sast_tz = timezone(timedelta(hours=2))
    
    # Get current SAST time
    sast_time = datetime.now(sast_tz).strftime("%Y-%m-%d %H:%M:%S SAST")
    
    print(f"🚀 QR Generator Launcher ({sast_time})")
    print("=" * 50)
    
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
    
    print(f"📁 Changing to directory: {getdevuid_dir}")
    print("🎨 Launching QR Generator GUI with SAST timezone...")
    
    # Change to the getDEVUID directory and run the GUI
    try:
        os.chdir(getdevuid_dir)
        subprocess.run([sys.executable, 'qr_generator_gui.py'])
    except Exception as e:
        print(f"❌ Error launching QR Generator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 