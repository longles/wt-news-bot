import discord
import os
import dotenv

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions

load_dotenv(dotenv_path='BOT_TOKEN.env')
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('bot is ready')
    
@bot.command()
@has_permissions(administrator=True)
async def refresh(ctx):
    for cog in os.listdir('./cogs'):
        if cog.endswith(".py"):
            bot.unload_extension(f'cogs.{cog[:-3]}')
            bot.load_extension(f'cogs.{cog[:-3]}')   
    await ctx.send('cogs have been refreshed')

if __name__ == '__main__': 
    for filename in os.listdir("./cogs"): 
        if filename.endswith(".py"):        
            bot.load_extension(f"cogs.{filename[:-3]}") 

bot.run(TOKEN)