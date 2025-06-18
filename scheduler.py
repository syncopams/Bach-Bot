#!/usr/bin/env python3
"""
Scheduler for Bach Bot - runs the bot daily using cron or systemd timer.
"""

import subprocess
import sys
import os
from datetime import datetime


def run_bot():
    """Run the Bach bot."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_script = os.path.join(script_dir, 'bach_bot.py')
    
    try:
        print(f"[{datetime.now()}] Running Bach Bot...")
        result = subprocess.run([sys.executable, bot_script], 
                              capture_output=True, text=True, cwd=script_dir)
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] Bach Bot completed successfully")
            print("Output:", result.stdout)
        else:
            print(f"[{datetime.now()}] Bach Bot failed with return code {result.returncode}")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"[{datetime.now()}] Error running Bach Bot: {e}")


if __name__ == "__main__":
    run_bot()

