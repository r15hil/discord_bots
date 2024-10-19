import json
import os
from typing import Optional

import discord
import requests
from discord.ext import commands

TOKEN = os.environ.get("HOROSCOPE_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialise user data
if os.path.exists("user_data.json"):
    with open("user_data.json", "r") as f:  # [unspecified-encoding]
        user_data = json.load(f)
else:
    user_data = {}

ZODIAC_SIGNS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]


@bot.command()
async def setsign(ctx, sign: str) -> None:
    """Command to set user's zodiac sign and save off in data file."""
    sign = sign.lower()
    if sign in ZODIAC_SIGNS:
        user_data[str(ctx.author.id)] = sign
        with open("user_data.json", "w") as f:  # [unspecified-encoding]
            json.dump(user_data, f)
        await ctx.send(f"Your zodiac sign has been set to **{sign.capitalize()}**.")
    else:
        await ctx.send(
            "Invalid zodiac sign. Please choose from: " + ", ".join(ZODIAC_SIGNS)
        )


def get_horoscope(sign: str) -> Optional[str]:
    """Fetch horoscope from API"""
    url = f"https://ohmanda.com/api/horoscope/{sign}/"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data["horoscope"]
    return None


@bot.command()
async def horoscope(ctx) -> None:
    """Command to get and send the horoscope of the user"""
    user_id = str(ctx.author.id)
    if user_id in user_data:
        sign = user_data[user_id]
        horoscope_info = get_horoscope(sign)
        if horoscope_info:
            await ctx.send(
                f"Here's your horoscope for today (**{sign.capitalize()}**):\n\n{horoscope_info}"
            )
        else:
            await ctx.send("Sorry, I couldn't fetch your horoscope at this time.")
    else:
        await ctx.send(
            "You haven't set your zodiac sign yet. Use `!setsign your_zodiac_sign` to set it."
        )


# Run the bot
bot.run(TOKEN)
