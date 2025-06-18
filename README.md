# Bach Bot - Mastodon Daily Posting Bot

## Overview

Bach Bot is a Python-based Mastodon bot that automatically posts a random J.S. Bach BWV (Bach-Werke-Verzeichnis) work with a YouTube search link daily. The bot covers all BWV numbers from 1 to 1080, ensuring a diverse selection of Bach's compositions including cantatas, organ works, keyboard pieces, orchestral works, and more.

## Features

- **Random BWV Selection**: Picks a random BWV number (1-1080) daily
- **YouTube Integration**: Generates YouTube search links for each BWV work
- **Mastodon Integration**: Posts directly to any Mastodon instance
- **Web Interface**: User-friendly web dashboard for configuration and management
- **Automated Scheduling**: Cron-based daily posting
- **Known Works Database**: Includes titles for popular BWV works
- **Comprehensive Testing**: Built-in test suite for validation
- **Easy Setup**: Automated configuration scripts

## Project Structure

```
bach_bot/
├── bach_bot.py          # Main bot application
├── config.json          # Configuration file (Mastodon credentials)
├── setup.py             # Automated Mastodon setup script
├── test_bot.py          # Test suite for bot functionality
├── scheduler.py         # Daily scheduling script
├── setup_cron.sh        # Cron job setup script
├── web_interface.py     # Flask web dashboard
├── templates/           # HTML templates for web interface
│   ├── index.html       # Main dashboard
│   ├── config.html      # Configuration page
│   └── logs.html        # Logs viewer
└── README.md           # This documentation
```

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A Mastodon account on any instance

### Step 1: Install Dependencies

```bash
pip install Mastodon.py flask flask-cors
```

### Step 2: Configure Mastodon Credentials

You have two options for setting up Mastodon credentials:

#### Option A: Automated Setup (Recommended)
```bash
python3 setup.py
```
This script will guide you through:
1. Registering the application with your Mastodon instance
2. Getting authorization from your account
3. Automatically saving credentials to config.json

#### Option B: Manual Setup
1. Go to your Mastodon instance (e.g., mastodon.social)
2. Navigate to Preferences → Development → New Application
3. Create an application with read and write permissions
4. Copy the Client Key, Client Secret, and Access Token
5. Edit `config.json` with your credentials

### Step 3: Test the Bot

```bash
# Run the test suite
python3 test_bot.py

# Test a single post (without actually posting)
python3 bach_bot.py
```

### Step 4: Set Up Daily Scheduling

```bash
# Add daily cron job (runs at 9:00 AM)
./setup_cron.sh add

# View current cron jobs
./setup_cron.sh show

# Remove cron job
./setup_cron.sh remove
```

### Step 5: Launch Web Interface (Optional)

```bash
python3 web_interface.py
```
Then visit http://localhost:5000 for the web dashboard.

## Usage

### Command Line Usage

```bash
# Post a random Bach BWV now
python3 bach_bot.py

# Run tests
python3 test_bot.py

# Set up Mastodon credentials
python3 setup.py
```

### Web Interface Usage

1. Start the web interface: `python3 web_interface.py`
2. Open http://localhost:5000 in your browser
3. Use the dashboard to:
   - Configure Mastodon credentials
   - Test connection
   - Preview posts
   - Post immediately
   - View logs

### Scheduling Options

The bot supports multiple scheduling methods:

1. **Cron (Linux/macOS)**:
   ```bash
   ./setup_cron.sh add
   ```

2. **Manual Cron Entry**:
   ```bash
   # Edit crontab
   crontab -e
   
   # Add this line for daily 9 AM posting
   0 9 * * * /usr/bin/python3 /path/to/bach_bot/scheduler.py
   ```

3. **Systemd Timer (Linux)**:
   Create systemd service and timer files for more advanced scheduling.

## Configuration

### config.json Structure

```json
{
  "mastodon": {
    "instance_url": "https://mastodon.social",
    "client_key": "your_client_key_here",
    "client_secret": "your_client_secret_here",
    "access_token": "your_access_token_here"
  },
  "youtube": {
    "search_base_url": "https://www.youtube.com/results?search_query="
  }
}
```

### Customization Options

You can customize the bot by modifying `bach_bot.py`:

- **Posting Time**: Change the cron schedule in `setup_cron.sh`
- **Post Format**: Modify the `create_post_text()` method
- **BWV Range**: Adjust the range in `get_random_bwv()` method
- **Known Titles**: Add more BWV titles to the `known_titles` dictionary
- **Hashtags**: Customize hashtags in the post template

## BWV Coverage

The bot covers all BWV numbers from 1 to 1080, including:

- **BWV 1-224**: Sacred Cantatas
- **BWV 225-249**: Motets, Masses, and Oratorios
- **BWV 250-524**: Chorales and Sacred Songs
- **BWV 525-771**: Organ Works
- **BWV 772-994**: Keyboard Works
- **BWV 995-1040**: Lute and Chamber Music
- **BWV 1041-1080**: Orchestral Works and The Art of Fugue

### Featured Works

The bot includes specific titles for popular BWV works such as:
- BWV 140: "Wachet auf, ruft uns die Stimme"
- BWV 147: "Herz und Mund und Tat und Leben"
- BWV 244: "St. Matthew Passion"
- BWV 565: "Toccata and Fugue in D minor"
- BWV 988: "Goldberg Variations"
- BWV 1080: "The Art of Fugue"

## Troubleshooting

### Common Issues

1. **"Unauthorized" Error**:
   - Check your Mastodon credentials in config.json
   - Ensure your access token has write permissions
   - Verify your instance URL is correct

2. **"Module not found" Error**:
   - Install required dependencies: `pip install Mastodon.py flask flask-cors`

3. **Cron Job Not Running**:
   - Check cron service is running: `systemctl status cron`
   - Verify cron job exists: `crontab -l`
   - Check logs: `tail -f bach_bot.log`

4. **Web Interface Not Accessible**:
   - Ensure Flask is running on 0.0.0.0:5000
   - Check firewall settings
   - Verify all dependencies are installed

### Debugging

Enable debug mode by setting the environment variable:
```bash
export FLASK_DEBUG=1
python3 web_interface.py
```

Check logs:
```bash
tail -f bach_bot.log
```

## Security Considerations

- Keep your `config.json` file secure and never commit it to version control
- Use environment variables for credentials in production
- Regularly rotate your Mastodon access tokens
- Run the bot with minimal required permissions

## Contributing

To contribute to Bach Bot:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section above
- Review the test output for diagnostic information
- Ensure all dependencies are properly installed
- Verify Mastodon credentials are correctly configured

## Acknowledgments

- Johann Sebastian Bach for his incredible musical legacy
- The Mastodon community for providing an open social platform
- The Python community for excellent libraries and tools

