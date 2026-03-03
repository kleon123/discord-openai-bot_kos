import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Get the Discord token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Check if tokens are set
if not DISCORD_TOKEN:
    print("ERROR: DISCORD_TOKEN not found in environment variables!")
    exit(1)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Ignore messages without content or from bots
    if not message.content or message.author.bot:
        return
    
    # Echo the message back
    reply = message.content

    # Send response (split if too long for Discord's 2000 char limit)
    if len(reply) > 2000:
        for i in range(0, len(reply), 2000):
            await message.reply(reply[i:i+2000])
    else:
        await message.reply(reply)

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
