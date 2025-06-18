#!/usr/bin/env python3
"""
Setup script for Bach Bot Mastodon credentials.
This script helps you register your application with Mastodon and get the necessary credentials.
"""

from mastodon import Mastodon
import json
import os


def setup_mastodon_app():
    """Set up Mastodon application and get credentials."""
    print("Bach Bot Mastodon Setup")
    print("=" * 30)
    
    # Get instance URL
    instance_url = input("Enter your Mastodon instance URL (e.g., https://mastodon.social): ").strip()
    if not instance_url.startswith('http'):
        instance_url = 'https://' + instance_url
    
    print(f"\nRegistering application with {instance_url}...")
    
    try:
        # Register application
        client_id, client_secret = Mastodon.create_app(
            'Bach Bot',
            scopes=['read', 'write'],
            api_base_url=instance_url
        )
        
        print("Application registered successfully!")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret}")
        
        # Get access token
        mastodon = Mastodon(
            client_id=client_id,
            client_secret=client_secret,
            api_base_url=instance_url
        )
        
        print("\nTo get your access token, you need to authorize the application.")
        print("This will open a browser window where you can log in and authorize the bot.")
        
        # Get authorization URL
        auth_url = mastodon.auth_request_url(scopes=['read', 'write'])
        print(f"\nPlease visit this URL to authorize the application:")
        print(auth_url)
        
        # Get authorization code
        auth_code = input("\nEnter the authorization code from the website: ").strip()
        
        # Get access token
        access_token = mastodon.log_in(code=auth_code)
        
        print("Access token obtained successfully!")
        
        # Save configuration
        config = {
            "mastodon": {
                "instance_url": instance_url,
                "client_key": client_id,
                "client_secret": client_secret,
                "access_token": access_token
            },
            "youtube": {
                "search_base_url": "https://www.youtube.com/results?search_query="
            }
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\nConfiguration saved to config.json")
        print("You can now run the bot with: python3 bach_bot.py")
        
        return True
        
    except Exception as e:
        print(f"Error setting up Mastodon: {e}")
        return False


if __name__ == "__main__":
    setup_mastodon_app()

