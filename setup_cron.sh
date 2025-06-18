#!/bin/bash

# Bach Bot Daily Cron Script
# This script sets up a daily cron job to run the Bach bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEDULER_SCRIPT="$SCRIPT_DIR/scheduler.py"

# Function to add cron job
add_cron_job() {
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "bach_bot"; then
        echo "Bach Bot cron job already exists."
        echo "Current cron jobs:"
        crontab -l | grep bach_bot
        return
    fi
    
    # Add new cron job to run daily at 9:00 AM
    (crontab -l 2>/dev/null; echo "0 9 * * * /usr/bin/python3 $SCHEDULER_SCRIPT >> $SCRIPT_DIR/bach_bot.log 2>&1") | crontab -
    
    echo "Bach Bot cron job added successfully!"
    echo "The bot will run daily at 9:00 AM."
    echo "Logs will be saved to: $SCRIPT_DIR/bach_bot.log"
}

# Function to remove cron job
remove_cron_job() {
    crontab -l 2>/dev/null | grep -v "bach_bot" | crontab -
    echo "Bach Bot cron job removed."
}

# Function to show current cron jobs
show_cron_jobs() {
    echo "Current cron jobs for Bach Bot:"
    crontab -l 2>/dev/null | grep bach_bot || echo "No Bach Bot cron jobs found."
}

# Main script
case "$1" in
    "add")
        add_cron_job
        ;;
    "remove")
        remove_cron_job
        ;;
    "show")
        show_cron_jobs
        ;;
    *)
        echo "Usage: $0 {add|remove|show}"
        echo "  add    - Add daily cron job for Bach Bot"
        echo "  remove - Remove Bach Bot cron job"
        echo "  show   - Show current Bach Bot cron jobs"
        exit 1
        ;;
esac

