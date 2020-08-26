import discord
from discord.ext import commands, tasks
import datetime
import discord, datetime, time, aiohttp, asyncio, random
from discord.ext import commands
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
import gspread

bot = commands.Bot(command_prefix='!')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

easy = client.open('Math Club Leaderboard').get_worksheet(0)
medium = client.open('Math Club Leaderboard').get_worksheet(1)
hard = client.open('Math Club Leaderboard').get_worksheet(2)
diffic = {
    "Hard" : hard,
    "Medium" : medium,
    "Easy" : easy
}

def update_leaderboard(): # basically just rearranges people according to their point values
  for sheet in diffic:
    points = diffic[sheet].col_values(3)
    del points[0]
    points = [x for x in points if x] # added
    print("debug1")
    print(points)
    indices = np.argsort(points)
    points.sort(reverse=True)
    print(points)
    indices = list(reversed(list(indices)))
    points.insert(0, "Points")
    for index, i in enumerate(points):
      diffic[sheet].update_cell(index+1, 3, i) # swapped
    names = diffic[sheet].col_values(2)
    del names[0]
    names = [x for x in names if x] # added
    if(len(indices) == 0):
      pass
    else:
      print("debug2")
      print(names)
      print(indices)
      names = [names[i] for i in indices]
    print(names)
    names.insert(0, "Names")
    for index, i in enumerate(names):
      diffic[sheet].update_cell(index+1, 2, i) # swapped

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

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

@bot.command()
@commands.has_role('Admin')
async def potd(ctx, problem, format, difficulty):
    date = str(datetime.datetime.now().date())
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
    embedv = discord.Embed(title="Problem of The Day", description=date, color=0xffff00)
    try:
      if(is_url_image(problem) == True):
        embedv.set_image(url=problem)
      else:
        if(problem.startswith("$")):
          message = await ctx.send(problem)
          await message.delete()
        else:
          embedv.add_field(name="Problem", value=problem, inline=False)
    except:
      if(problem.startswith("$")):
        message = await ctx.send(problem)
        await message.delete()
      else:
        embedv.add_field(name="Problem", value=problem, inline=False)
    embedv.add_field(name="Answer Format", value=format, inline=False)
    embedv.add_field(name="Points", value="1st - 50 Points \n 2nd - 30 Points \n 3rd - 20 Points \n 4th - 10 Points \n 5h - 1 Point", inline=False)
    embedv.add_field(name="Difficulty", value=difficulty, inline=False)
    await ctx.send(embed=embedv)
    await ctx.message.delete()

@bot.command()
@commands.has_role('Admin')
async def potdhelp(ctx):
  await ctx.send("`!potd [problem text/image url] [answer format] [difficulty]`")

@bot.command()
@commands.has_role('Admin')
async def leaderboard_update(ctx, name, points, difficulty):
  if(name not in diffic[difficulty].col_values(2)): 
    diffic[difficulty].update_cell(25, 2, name) 
    diffic[difficulty].update_cell(25, 3,  points) 
  else:
    index = diffic[difficulty].col_values(2).index(name)
    past_points = diffic[difficulty].cell(index+1, 3).value
    diffic[difficulty].update_cell(index+1, 3, int(past_points) + int(points)) # not swapped
  update_leaderboard()  

@bot.command()
async def info(ctx):
  await ctx.send("Hi! Welcome to Math Club! Our goal is to prepare you to be better at math and help you understand confusing and new topics. We're also going to offer the opportunity for you to take the American Mathematics Competition (AMC) test. The AMC test is full of fun and interesting problems that can lead to some insight on math tricks and shortcuts. A math problem should be up on `#cool-problems` at noon two days of the week. Solve it to get points and score high on the leaderboard. First place will get a prize at the end of the year! \n \n Please tell us your name, grade, and current math class so we can get to know you!")

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




    


bot.run('token')
