import discord
import requests
import hashlib
import sqlite3
import urllib.parse

from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext import tasks

db = sqlite3.connect('wt_news.db')


class WarThunder:
    def __init__(self, title, desc, url, img_url, date):
        self.title = title
        self.desc = desc
        self.url = url
        self.img_url = img_url
        self.date = date


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.news.start()

    @tasks.loop(minutes=1)
    async def news(self):
        cursor = db.cursor()
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == 'wt-news':
                    news_channel = self.bot.get_channel(channel.id)
                    news = scrape('https://warthunder.com/en/news')
                    patchnotes = scrape('https://warthunder.com/en/game/changelog/')

                    for data in reversed(news):  # newest to oldest (bottom to top)
                        wt1 = data_find(data)
                        hash_val = hashlib.md5(f'{wt1.url}'.encode('utf-8')).hexdigest()
                        cursor.execute(f'SELECT hash FROM warthunder WHERE hash="{str(hash_val)}"')
                        result = cursor.fetchone()
                        if not result:   # checking if such a hash value exists in db
                            cursor.execute(f'INSERT INTO warthunder VALUES("{str(hash_val)}")')
                            db.commit()
                            embed = discord.Embed(title=wt1.title, url=wt1.url, description=wt1.desc)
                            embed.set_thumbnail(url=wt1.img_url)
                            embed.set_footer(text=wt1.date)
                            await news_channel.send(embed=embed)

                    for data in reversed(patchnotes):
                        wt2 = data_find(data)
                        hash_val = hashlib.md5(f'{wt2.url}'.encode('utf-8')).hexdigest()
                        cursor.execute(f'SELECT hash FROM warthunder WHERE hash="{str(hash_val)}"')
                        result = cursor.fetchone()
                        if not result:
                            cursor.execute(f'INSERT INTO warthunder VALUES("{str(hash_val)}")')
                            db.commit()
                            embed = discord.Embed(title=wt2.title, url=wt2.url, description=wt2.desc)
                            embed.set_thumbnail(url=wt2.img_url)
                            embed.set_footer(text=wt2.date)
                            await news_channel.send(embed=embed)

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', {'class': 'showcase__item widget'})
    return results

def data_find(data):
    title = data.find('div', {'class': 'widget__title'})
    desc = data.find('div', {'class': 'widget__comment'})
    url = data.find('a', {'class': 'widget__link'})
    img_url = data.find('img', {'class': 'widget__poster-media js-lazy-load'})
    date = data.find('li', {'class': 'widget-meta__item widget-meta__item--right'})
    return WarThunder(title.text.strip(),
                      desc.text.strip(),
                      'https://warthunder.com' + urllib.parse.quote(url.attrs['href']),
                      'https:' + urllib.parse.quote(img_url.attrs['data-src']),
                      date.text.strip()
                      )


def setup(bot):
    bot.add_cog(News(bot))
