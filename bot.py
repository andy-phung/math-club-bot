import discord
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks
import datetime
from urllib.request import urlopen
import discord, datetime, time, aiohttp, asyncio, random
from discord.ext import commands
from random import randint
from random import choice
from urllib.parse import quote_plus
from collections import deque

bot = commands.Bot(command_prefix='!')
client = MongoClient() # for retrieving problems and answers

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="!commands"))

@bot.command()
async def problem(ctx, year, competition, prob):
    try:
      prob = int(prob)
      prob = str(prob)
      year = int(year)
      year = str(year)
      date = str(datetime.datetime.now().date())
      date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
      print("https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_AMC_" + str(competition) + "_Problems/Problem_" + str(prob))
      embedv = discord.Embed(title= str(year) + " AMC " + str(competition) + ", Problem " + str(prob), description=date, color=0xffff00)
      embedv.add_field(name="Problem", value="hi", inline=False)
      embedv.add_field(name="Answer Format", value="DM your answer to this bot in the format [insert format here]!", inline=False)
      embedv.add_field(name="Points", value="1st - 5 Points \n 2nd - 3 Points \n 3rd - 2 Points \n 4th - 1 Point", inline=False)
      await ctx.send(embed=embedv)
    except:
      pass
    
@bot.command()
async def info(ctx):
  await ctx.send("Hi! Welcome to Math Club! Our goal is to prepare you to be better at math and help you understand confusing and new topics. We also plan to try the AMC tests. The AMC test is full of fun and interesting problems that can lead to some insight on math tricks and shortcuts. A math problem should be up on `#cool-problems` at noon daily. Solve it to get points and score high on the leaderboard. First place will get a prize at the end of the year!")

@bot.command()
async def commands(ctx):
  await ctx.send("To request an AMC problem, use `!problem [year] [competition] [problem]`, where [competition] can be 10A, 10B, 12A, or 12B. \n For an introduction to this club, use `!info`.")

@bot.command()
async def ping(ctx):
  await ctx.send('Pong :ping_pong: {0}'.format(bot.latency))

msg_dump_channel = 744394077306355712
@bot.event
async def on_message(message: discord.Message):
    channel = bot.get_channel(msg_dump_channel)
    if message.guild is None and not message.author.bot:
        # if the channel is public at all, make sure to sanitize this first
        await channel.send(message.content)
    await bot.process_commands(message)


# WIP command that posts stuff from r/learnmath
acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()
memeSubreddits = ["learnmath"]

async def getSub(self, ctx, sub):
  """Get stuff from requested sub"""
  async with aiohttp.ClientSession() as session:
      async with session.get(f"https://www.reddit.com/r{sub}/hot.json?limit=100") as response:
          request = await response.json()

  attempts = 1
  while attempts < 5:
      if 'error' in request:
          print("failed request {}".format(attempts))
          await asyncio.sleep(2)
          async with aiohttp.ClientSession() as session:
              async with session.get(f"https://www.reddit.com/r/{sub}/hot.json?limit=100") as response:
                  request = await response.json()
          attempts += 1
      else:
          index = 0

          for index, val in enumerate(request['data']['children']):
              if 'url' in val['data']:
                  url = val['data']['url']
                  urlLower = url.lower()
                  accepted = False
                  for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
                      if v in urlLower:
                          accepted = True
                  if accepted:
                      if url not in memeHistory:
                          memeHistory.append(url)  #add the url to the history, so it won't be posted again
                          if len(memeHistory) > 63: #limit size
                              memeHistory.popleft() #remove the oldest

                          break #done with this loop, can send image
          await ctx.send(memeHistory[len(memeHistory) - 1]) #send the last image
          return
  await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

@bot.command()
async def learnmath(ctx):
  """Memes from various subreddits (excluding r/me_irl. some don't understand those memes)"""
  async with aiohttp.ClientSession() as session:
      async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
          request = await response.json()

  attempts = 1
  while attempts < 5:
      if 'error' in request:
          print("failed request {}".format(attempts))
          await asyncio.sleep(2)
          async with aiohttp.ClientSession() as session:
              async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=100".format(random.choice(memeSubreddits))) as response:
                  request = await response.json()
          attempts += 1
      else:
          index = 0

          for index, val in enumerate(request['data']['children']):
              if 'url' in val['data']:
                  url = val['data']['url']
                  urlLower = url.lower()
                  accepted = False
                  for j, v, in enumerate(acceptableImageFormats): 
                      if v in urlLower:
                          accepted = True
                  if accepted:
                      if url not in memeHistory:
                          memeHistory.append(url)  
                          if len(memeHistory) > 63: 
                              memeHistory.popleft() 

                          break 
          await ctx.send(memeHistory[len(memeHistory) - 1])
          return
  await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))


    


bot.run('token')
