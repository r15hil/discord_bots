import json
import os
from typing import Optional

import discord
import requests
from discord.ext import commands, tasks

DISCORD_BOT_TOKEN = os.getenv("BOT_TOKEN")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

MIN_UPDATE = 3
DEFAULT_INTERVAL = 60

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
subscriptions = {}
user_intervals = {}
cache = {}

if os.path.exists("subscriptions.json"):
    with open("subscriptions.json", "r") as f:  # [unspecified-encoding]
        subscriptions = json.load(f)

if os.path.exists("user_intervals.json"):
    with open("user_intervals.json", "r") as f:  # [unspecified-encoding]
        user_intervals = json.load(f)

if os.path.exists("cache.json"):
    with open("cache.json", "r") as f:  # [unspecified-encoding]
        cache = json.load(f)


@bot.event
async def on_ready() -> None:
    """
    Event called when the bot is ready.
    Starts the stock checking loop.
    """
    print(f"{bot.user.name} has connected.")
    update_cache.start()
    check_stocks.start()


@bot.command(name="subscribe")
async def subscribe(ctx: commands.Context, stock_symbol: str) -> None:
    """
    Subscribes the user to updates for a given stock symbol.

    Args:
        ctx (commands.Context): The context of the command.
        stock_symbol (str): The stock symbol to subscribe to.
    """
    user_id = str(ctx.author.id)
    stock_symbol = stock_symbol.upper()

    if user_id not in subscriptions:
        subscriptions[user_id] = []

    if stock_symbol in subscriptions[user_id]:
        await ctx.send(f"You are already subscribed to {stock_symbol} updates.")
        return

    subscriptions[user_id].append(stock_symbol)
    await ctx.send(f"Subscribed to {stock_symbol} updates.")
    save_subscriptions()


@bot.command(name="unsubscribe")
async def unsubscribe(ctx: commands.Context, stock_symbol: str) -> None:
    """
    Unsubscribes the user from updates for a given stock symbol.

    Args:
        ctx (commands.Context): The context of the command.
        stock_symbol (str): The stock symbol to unsubscribe from.
    """
    user_id = str(ctx.author.id)
    stock_symbol = stock_symbol.upper()

    if user_id in subscriptions and stock_symbol in subscriptions[user_id]:
        subscriptions[user_id].remove(stock_symbol)
        await ctx.send(f"Unsubscribed from {stock_symbol} updates.")
        if not subscriptions[user_id]:
            del subscriptions[user_id]
            if user_id in user_intervals:
                del user_intervals[user_id]
    else:
        await ctx.send(f"You are not subscribed to {stock_symbol}.")

    save_subscriptions()
    save_user_intervals()


@bot.command(name="set_interval")
async def set_interval(ctx: commands.Context, interval: int) -> None:
    """
    Sets the update interval for the user.

    Args:
        ctx (commands.Context): The context of the command.
        interval (int): The interval in minutes for updates.
    """
    if interval < MIN_UPDATE:
        await ctx.send(f"The minimum interval for updates is {MIN_UPDATE} minutes.")
        return

    user_id = str(ctx.author.id)
    user_intervals[user_id] = interval
    await ctx.send(f"Update interval set to {interval} minutes.")
    save_user_intervals()


@tasks.loop(minutes=MIN_UPDATE)
async def update_cache() -> None:
    """
    Updates the local cache with stock data every MIN_UPDATE minutes.
    """
    symbols = set()
    for user_symbols in subscriptions.values():
        for symbol in user_symbols:
            symbols.add(symbol)

    if symbols:
        data = get_stock_data(list(symbols))
        if data:
            for symbol in symbols:
                if symbol in data:
                    cache[symbol] = {
                        "price": data[symbol].get("close"),
                        "market_open": data[symbol].get("is_market_open"),
                        "name": data[symbol].get("name"),
                        "datetime": f"{data[symbol].get('datetime')} {data[symbol].get('timestamp')}",
                        "change": data[symbol].get("change"),
                        "percent_change": data[symbol].get("percent_change"),
                    }
    save_cache()


@tasks.loop(minutes=1)
async def check_stocks() -> None:
    """
    Sends stock price updates to subscribed users based on their configured intervals.
    """
    for user_id, symbols in subscriptions.items():
        interval = user_intervals.get(user_id, DEFAULT_INTERVAL)
        if check_stocks.current_loop % interval == 0:
            for symbol in symbols:
                if symbol in cache:
                    stock_info = cache[symbol]
                    user_obj = await bot.fetch_user(int(user_id))
                    await user_obj.send(
                        f"{symbol} ({stock_info['name']}) is currently at {stock_info['price']} (Market {'Open' if stock_info['market_open'] else 'Closed'})\n"
                        f"Change: {stock_info['change']} ({stock_info['percent_change']}%)\nLast updated: {stock_info['datetime']}"
                    )


def get_stock_data(symbols: list) -> Optional[dict]:
    """
    Retrieves stock data for a list of symbols using the Twelve Data API.

    Args:
        symbols (list): A list of stock symbols.

    Returns:
        Optional[dict]: A dictionary containing the stock data, or None if the request fails.
    """
    symbol_str = ",".join(symbols)
    url = f"https://api.twelvedata.com/quote?symbol={symbol_str}&apikey={TWELVE_DATA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None


def save_subscriptions() -> None:
    """
    Saves the current subscriptions to a JSON file.
    """
    with open("subscriptions.json", "w") as f:  # [unspecified-encoding]
        json.dump(subscriptions, f)


def save_user_intervals() -> None:
    """
    Saves the current user intervals to a JSON file.
    """
    with open("user_intervals.json", "w") as f:  # [unspecified-encoding]
        json.dump(user_intervals, f)


def save_cache() -> None:
    """
    Saves the current cache to a JSON file.
    """
    with open("cache.json", "w") as f:  # [unspecified-encoding]
        json.dump(cache, f)


bot.run(DISCORD_BOT_TOKEN)
