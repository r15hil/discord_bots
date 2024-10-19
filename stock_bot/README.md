# Stock Price Discord Bot

This is a Discord bot that allows users to subscribe to stock price updates and receive notifications at configurable intervals. The bot uses the Twelve Data API to fetch real-time stock data and delivers updates directly through Discord messages. The API is free for 8 requests per minute at a maximum of 800 request per day (thats why I set the min interval at 3 mins to make sure I don't exceed it, and so I can do other non-this-bot requests to the API.)

## Features
- **Subscribe to Stock Updates**: Users can subscribe to receive price updates for specific stock symbols.
- **Unsubscribe**: Users can unsubscribe from any stock symbol they no longer wish to track.
- **Set Update Interval**: Users can configure the frequency at which they receive updates, with a minimum interval of 3 minutes (because I want to rate limit the API, you can change this if you want).
- **Real-Time Stock Data**: Fetches the latest stock data from Twelve Data API every 3 minutes and stores it in a local cache.

## Requirements
- Python 3.8 or higher (because that's what I've tested it on)
- Discord bot token
- Twelve Data API key

## Setup Instructions
1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```sh
   pip install -r stock_bot/requirements.txt
   ```

3. **Set Environment Variables**
   - `BOT_TOKEN`: Your Discord bot token (see main README on how to get this)
   - `TWELVE_DATA_API_KEY`: Your Twelve Data API key.

4. **Run the Bot**
   ```sh
   cd stock_bot.py
   python3 stock_bot.py
   ```

## Commands
Once you've added the bot to your server
- `!subscribe <stock_symbol>`: Subscribes the user to updates for the specified stock symbol (e.g., `!subscribe AAPL`).
- `!unsubscribe <stock_symbol>`: Unsubscribes the user from updates for the specified stock symbol (e.g., `!unsubscribe AAPL`).
- `!set_interval <interval>`: Sets the update interval in minutes for the user (e.g., `!set_interval 30`). The minimum allowed interval is 3 minutes.

## Files
- **`stock_bot.py`**: Main bot code that handles Discord commands and tasks.
- **`subscriptions.json`**: Stores user subscriptions to stock symbols.
- **`user_intervals.json`**: Stores user-defined update intervals.
- **`cache.json`**: Stores cached stock data.

## How It Works
- When the bot starts, it loads existing subscriptions, user intervals, and cache from JSON files if available.
- The `update_cache` task runs every on a configrable interval and queries the Twelve Data API for updated stock information. This data is stored in a local cache.
- The `check_stocks` task runs on a loop and checks user subscriptions to send updates based on their specified interval.
- Users can subscribe to multiple stock symbols, and the bot will deliver real-time stock updates directly to their Discord DMs.
