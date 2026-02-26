import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Get the Discord token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if tokens are set
if not DISCORD_TOKEN:
    print("ERROR: DISCORD_TOKEN not found in environment variables!")
    exit(1)

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found in environment variables!")
    exit(1)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

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
    
    # Show typing indicator
    async with message.channel.typing():
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": message.content}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Get the response text
            reply = response['choices'][0]['message']['content']
            
            # Send response (split if too long for Discord's 2000 char limit)
            if len(reply) > 2000:
                for i in range(0, len(reply), 2000):
                    await message.reply(reply[i:i+2000])
            else:
                await message.reply(reply)
                
        except Exception as e:
            await message.reply(f"Error: {str(e)}")

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
