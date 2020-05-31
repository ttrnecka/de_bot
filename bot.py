"""Bot"""
import os
import discord
import re
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler

ROOT = os.path.dirname(__file__)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.propagate = False
handler = RotatingFileHandler(
    os.path.join(ROOT, 'logs','discord.log'), maxBytes=1000000,
    backupCount=5, encoding='utf-8', mode='a'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!', case_insensitive=True)


@bot.check
async def check_if_can_respond(ctx):
  logger.info("%s: %s", ctx.author, ctx.message.content)
  #ignore DM
  if isinstance(ctx.channel, discord.abc.PrivateChannel):
    raise discord.ext.commands.CommandError("PM commands are not allowed. Please use the Imperium discord server.")
  return True

@bot.event
async def on_ready():
    """loads custom emojis upon ready"""
    logger.info('Logged in as')
    logger.info(bot.user.name)
    logger.info(bot.user.id)
    logger.info('------')

    act = discord.Game(f"Playing DE")
    await bot.change_presence(status=discord.Status.online, activity=act)

@bot.event
async def on_message(message):
    if message.author == bot.user:
      return
    if re.match(r"starting roster", message.content, re.IGNORECASE):
      msg ="""DE starting rosters:

            1. 4 Blitzers, 1 Runner, 6 Linos, 2 RRs
            Pros:
            - rookie friendlier (more blocks, no frenzy trapping)
            - fast 3rd RR through Leader on Runner
            - safer (recommended for Eternal leagues rosters)

            Cons:
            - no witch till about game 3/4
            - runner hogs lot of SPP and you do not want to keep him forever

            2. 3 Blitzers, 1 Witch, 2 RRs
            Pros:
              - witch from the start (surfing threat/dodge)
              - less wasted SPP

            Cons:
              - witch from the start (additional liability/AV7)
              - riskier (recommended for ladders where you can restart team if the first games go awry)
              - need more money for 3rd RR/APO"
              """

      await message.channel.send(msg)

with open(os.path.join(ROOT, 'config/TOKEN'), 'r') as token_file:
    TOKEN = token_file.read()
    
bot.run(TOKEN, bot=True, reconnect=True)

