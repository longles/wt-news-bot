import discord
import asyncpraw
import os
import time

from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

load_dotenv(dotenv_path='secrets.env')

MY_ID = os.getenv('ID')
MY_SECRET = os.getenv('SECRET')
MY_AGENT = os.getenv('USER_AGENT')
MY_USER = os.getenv('USER')
MY_PASS = os.getenv('PASSWORD')

reddit = asyncpraw.Reddit(
        client_id=MY_ID,
        client_secret=MY_SECRET,
        user_agent=MY_AGENT,
        username=MY_USER,
        password=MY_PASS
        )


class RedditPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit_queries = dict()
        self.search_comments.start()

    @tasks.loop(seconds=1.0)
    async def search_comments(self):
        for username in list(self.reddit_queries):
            redditor = await reddit.redditor(str(username))
            async for comment in redditor.comments.new(limit=1):
                if self.reddit_queries[username]['comment'] is not None and comment != self.reddit_queries[username]['comment']:
                    for stalker in self.reddit_queries[username]['stalkers']:
                        user = await self.bot.fetch_user(stalker)
                        await user.send(f'{username} has sent a new message')
                        self.reddit_queries[username]['comment'] = comment
                else:
                        self.reddit_queries[username]['comment'] = comment

    @commands.command()
    async def stalk(self, ctx, redditor_username):
        if redditor_username in self.reddit_queries:
            if ctx.author.id in self.reddit_queries[redditor_username]['stalkers']:
                await ctx.send(f'{redditor_username} is already being stalked by you')
            else:
                 self.reddit_queries[redditor_username]['stalkers'].add(ctx.author.id)
                 ctx.send(f'{redditor_username} is now being stalked by you')
        else:
            self.reddit_queries[redditor_username] = {'stalkers' : {ctx.author.id}, 'comment' : None}
            await ctx.send(f'{redditor_username} is now being stalked by you')
        
    @commands.command()
    async def unstalk(self, ctx, redditor_username):
        if redditor_username in self.reddit_queries:
            if ctx.author.id in self.reddit_queries[redditor_username]['stalkers']:
               self.reddit_queries[redditor_username]['stalkers'].remove(ctx.author.id)
               await ctx.send(f'{redditor_username} has been unstalked')
            else:
                await ctx.send(f'{redditor_username} is not being stalked by you')
        else:
            await ctx.send(f'{redditor_username} is not currently being stalked')
 
    @commands.command()
    async def test(self, ctx):
        await ctx.send(self.reddit_queries)



def setup(bot):
    bot.add_cog(RedditPing(bot))
