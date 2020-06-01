"""Bot"""
import os
import discord
import re
from discord.ext import commands
from logging.handlers import RotatingFileHandler
from misc.logger import logger

bot = commands.Bot(command_prefix='!', case_insensitive=True)
ROOT = os.path.dirname(__file__)

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

    act = discord.Game(f"Playing BB2")
    await bot.change_presence(status=discord.Status.online, activity=act)

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
      return
    if re.search(r"starting roster", message.content, re.IGNORECASE):
      msg ="""
      DE starting rosters:
      **1. 4 Blitzers, 1 Runner, 6 Linos, 2 RRs**
      Pros:
      - rookie friendlier (more blocks, no frenzy trapping)
      - fast 3rd RR through Leader on Runner
      - safer (recommended for Eternal leagues rosters)

      Cons:
      - no witch till about game 3/4
      - runner hogs lot of SPP and you do not want to keep him forever

      **2. 3 Blitzers, 1 Witch, 2 RRs**
      Pros:
        - witch from the start (surfing threat/dodge)
        - less wasted SPP

      Cons:
        - witch from the start (additional liability/AV7)
        - riskier (recommended for ladders where you can restart team if the first games go awry)
        - need more money for 3rd RR/APO"

      **3. 4 Blitzers, 7 Linos, 2 RRs**
      Pros:
      - All your players are AV8
      - More money left for Apo after first match
      - Very safe, no players who you don't want SPP on
      
      Cons:
      - No witch till about game 3/4
      - Less MV7 on the team, you're noticeably slower to move over the pitch
      """

      await message.channel.send(msg)


cogs_dir = os.path.join(ROOT, 'cogs')
# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            logger.info(f'Loading cog {extension}')
            bot.load_extension("cogs." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            logger.error(f'Failed to load extension {extension}.')

with open(os.path.join(ROOT, 'config/TOKEN'), 'r') as token_file:
    TOKEN = token_file.read()
    
bot.run(TOKEN, bot=True, reconnect=True)

