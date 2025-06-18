#!/usr/bin/env python3
"""
Flask web interface for Bach Bot management.
Provides a simple web interface to configure and manage the Bach Bot.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import json
import os
import subprocess
import sys
from datetime import datetime
from bach_bot import BachBot

app = Flask(__name__)
app.secret_key = 'bach_bot_secret_key_change_this'
CORS(app)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    """Main dashboard."""
    return render_template('index.html')


@app.route('/config')
def config():
    """Configuration page."""
    config_file = os.path.join(SCRIPT_DIR, 'config.json')
    config_data = {}
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    
    return render_template('config.html', config=config_data)


@app.route('/save_config', methods=['POST'])
def save_config():
    """Save configuration."""
    config_file = os.path.join(SCRIPT_DIR, 'config.json')
    
    config_data = {
        "mastodon": {
            "instance_url": request.form.get('instance_url', ''),
            "client_key": request.form.get('client_key', ''),
            "client_secret": request.form.get('client_secret', ''),
            "access_token": request.form.get('access_token', '')
        },
        "youtube": {
            "search_base_url": "https://www.youtube.com/results?search_query="
        }
    }
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    flash('Configuration saved successfully!', 'success')
    return redirect(url_for('config'))


@app.route('/test_connection')
def test_connection():
    """Test Mastodon connection."""
    try:
        bot = BachBot()
        if bot.test_connection():
            return jsonify({'status': 'success', 'message': 'Connection successful!'})
        else:
            return jsonify({'status': 'error', 'message': 'Connection failed. Check your credentials.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})


@app.route('/post_now')
def post_now():
    """Post a Bach BWV now."""
    try:
        bot = BachBot()
        if bot.post_daily_bach():
            return jsonify({'status': 'success', 'message': 'Posted successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to post. Check your configuration.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})


@app.route('/preview')
def preview():
    """Preview what would be posted."""
    try:
        bot = BachBot()
        bwv_number = bot.get_random_bwv()
        bwv_info = bot.get_bwv_info(bwv_number)
        youtube_url = bot.search_youtube_for_bwv(bwv_number)
        post_text = bot.create_post_text(bwv_info, youtube_url)
        
        return jsonify({
            'status': 'success',
            'bwv_number': bwv_number,
            'bwv_info': bwv_info,
            'youtube_url': youtube_url,
            'post_text': post_text
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})


@app.route('/logs')
def logs():
    """View bot logs."""
    log_file = os.path.join(SCRIPT_DIR, 'bach_bot.log')
    logs = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.readlines()[-50:]  # Last 50 lines
    
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(SCRIPT_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

