import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

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
bot.run(os.getenv('DISCORD_TOKEN'))