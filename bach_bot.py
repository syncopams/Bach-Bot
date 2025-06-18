#!/usr/bin/env python3
"""
Bach BWV Mastodon Bot

A bot that posts a random J.S. Bach BWV (1-1080) YouTube link daily to Mastodon.
"""

import random
import json
import os
from datetime import datetime
from mastodon import Mastodon
import requests
from urllib.parse import quote


class BachBot:
    def __init__(self, config_file='config.json'):
        """Initialize the Bach bot with configuration."""
        self.config_file = config_file
        self.config = self.load_config()
        self.mastodon = None
        self.setup_mastodon()
        
    def load_config(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config template
            default_config = {
                "mastodon": {
                    "instance_url": "https://mastodon.social",
                    "client_key": "",
                    "client_secret": "",
                    "access_token": ""
                },
                "youtube": {
                    "search_base_url": "https://www.youtube.com/results?search_query="
                }
            }
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config file: {self.config_file}")
            print("Please fill in your Mastodon credentials.")
            return default_config
    
    def setup_mastodon(self):
        """Set up Mastodon API connection."""
        try:
            if not all([
                self.config['mastodon']['client_key'],
                self.config['mastodon']['client_secret'],
                self.config['mastodon']['access_token']
            ]):
                print("Mastodon credentials not configured. Please update config.json")
                return
                
            self.mastodon = Mastodon(
                client_id=self.config['mastodon']['client_key'],
                client_secret=self.config['mastodon']['client_secret'],
                access_token=self.config['mastodon']['access_token'],
                api_base_url=self.config['mastodon']['instance_url']
            )
            print("Mastodon API connection established.")
        except Exception as e:
            print(f"Error setting up Mastodon: {e}")
    
    def get_random_bwv(self):
        """Get a random BWV number between 1 and 1080."""
        return random.randint(1, 1080)
    
    def search_youtube_for_bwv(self, bwv_number):
        """Search YouTube for a specific BWV work."""
        search_query = f"Bach BWV {bwv_number}"
        search_url = self.config['youtube']['search_base_url'] + quote(search_query)
        
        # For a more sophisticated approach, we could use YouTube API
        # But for simplicity, we'll construct a search URL
        return search_url
    
    def get_bwv_info(self, bwv_number):
        """Get information about a BWV work."""
        # This is a simplified mapping - in a real implementation,
        # you might want a more comprehensive database
        bwv_info = {
            "number": bwv_number,
            "title": f"BWV {bwv_number}",
            "composer": "Johann Sebastian Bach"
        }
        
        # Add some known titles for popular BWVs
        known_titles = {
            1: "Wie schön leuchtet der Morgenstern (Cantata)",
            2: "Ach Gott, vom Himmel sieh darein (Cantata)",
            3: "Ach Gott, wie manches Herzeleid (Cantata)",
            4: "Christ lag in Todes Banden (Cantata)",
            5: "Wo soll ich fliehen hin (Cantata)",
            6: "Bleib bei uns, denn es will Abend werden (Cantata)",
            7: "Christ unser Herr zum Jordan kam (Cantata)",
            8: "Liebster Gott, wenn werd ich sterben? (Cantata)",
            9: "Es ist das Heil uns kommen her (Cantata)",
            10: "Meine Seel erhebt den Herren (Cantata)",
            140: "Wachet auf, ruft uns die Stimme (Cantata)",
            147: "Herz und Mund und Tat und Leben (Cantata)",
            244: "St. Matthew Passion",
            245: "St. John Passion",
            248: "Christmas Oratorio",
            565: "Toccata and Fugue in D minor",
            582: "Passacaglia and Fugue in C minor",
            846: "Well-Tempered Clavier Book I, Prelude and Fugue No. 1 in C major",
            847: "Well-Tempered Clavier Book I, Prelude and Fugue No. 2 in C minor",
            988: "Goldberg Variations",
            1080: "The Art of Fugue"
        }
        
        if bwv_number in known_titles:
            bwv_info["title"] = f"BWV {bwv_number}: {known_titles[bwv_number]}"
        
        return bwv_info
    
    def create_post_text(self, bwv_info, youtube_url):
        """Create the text for the Mastodon post."""
        post_text = f"🎼 Daily Bach: {bwv_info['title']}\n\n"
        post_text += f"Discover this masterpiece by Johann Sebastian Bach:\n"
        post_text += f"{youtube_url}\n\n"
        post_text += f"#Bach #ClassicalMusic #BWV{bwv_info['number']} #DailyBach #BaroqueMusic"
        
        return post_text
    
    def post_daily_bach(self):
        """Post a random Bach BWV to Mastodon."""
        if not self.mastodon:
            print("Mastodon not configured. Cannot post.")
            return False
        
        try:
            # Get random BWV
            bwv_number = self.get_random_bwv()
            bwv_info = self.get_bwv_info(bwv_number)
            
            # Get YouTube search URL
            youtube_url = self.search_youtube_for_bwv(bwv_number)
            
            # Create post text
            post_text = self.create_post_text(bwv_info, youtube_url)
            
            # Post to Mastodon
            status = self.mastodon.status_post(post_text)
            
            print(f"Successfully posted BWV {bwv_number} to Mastodon!")
            print(f"Post URL: {status['url']}")
            print(f"Post text:\n{post_text}")
            
            return True
            
        except Exception as e:
            print(f"Error posting to Mastodon: {e}")
            return False
    
    def test_connection(self):
        """Test the Mastodon connection."""
        if not self.mastodon:
            print("Mastodon not configured.")
            return False
        
        try:
            account = self.mastodon.me()
            print(f"Connected to Mastodon as: @{account['username']}")
            return True
        except Exception as e:
            print(f"Error testing connection: {e}")
            return False


def main():
    """Main function to run the bot."""
    bot = BachBot()
    
    # Test connection first
    if bot.test_connection():
        # Post daily Bach
        bot.post_daily_bach()
    else:
        print("Please configure your Mastodon credentials in config.json")


if __name__ == "__main__":
    main()

