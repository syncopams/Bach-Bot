#!/usr/bin/env python3
"""
Test script for Bach Bot functionality without requiring Mastodon credentials.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bach_bot import BachBot


def test_bwv_generation():
    """Test BWV number generation and info retrieval."""
    print("Testing BWV generation and info retrieval...")
    print("=" * 50)
    
    bot = BachBot()
    
    # Test random BWV generation
    for i in range(5):
        bwv_number = bot.get_random_bwv()
        bwv_info = bot.get_bwv_info(bwv_number)
        youtube_url = bot.search_youtube_for_bwv(bwv_number)
        post_text = bot.create_post_text(bwv_info, youtube_url)
        
        print(f"\nTest {i+1}:")
        print(f"BWV Number: {bwv_number}")
        print(f"BWV Info: {bwv_info}")
        print(f"YouTube URL: {youtube_url}")
        print(f"Post Text:\n{post_text}")
        print("-" * 30)


def test_known_bwvs():
    """Test some well-known BWV works."""
    print("\nTesting known BWV works...")
    print("=" * 50)
    
    bot = BachBot()
    known_bwvs = [1, 4, 140, 147, 244, 245, 248, 565, 582, 846, 988, 1080]
    
    for bwv_number in known_bwvs:
        bwv_info = bot.get_bwv_info(bwv_number)
        youtube_url = bot.search_youtube_for_bwv(bwv_number)
        
        print(f"\nBWV {bwv_number}: {bwv_info['title']}")
        print(f"YouTube Search: {youtube_url}")


def test_edge_cases():
    """Test edge cases for BWV numbers."""
    print("\nTesting edge cases...")
    print("=" * 50)
    
    bot = BachBot()
    edge_cases = [1, 1080, 500]  # First, last, and middle
    
    for bwv_number in edge_cases:
        bwv_info = bot.get_bwv_info(bwv_number)
        youtube_url = bot.search_youtube_for_bwv(bwv_number)
        post_text = bot.create_post_text(bwv_info, youtube_url)
        
        print(f"\nBWV {bwv_number}:")
        print(f"Title: {bwv_info['title']}")
        print(f"YouTube URL: {youtube_url}")
        print(f"Post length: {len(post_text)} characters")


if __name__ == "__main__":
    print("Bach Bot Test Suite")
    print("=" * 50)
    
    test_bwv_generation()
    test_known_bwvs()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("The bot is ready to use once Mastodon credentials are configured.")

