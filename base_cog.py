import traceback
import discord
import re
from discord.ext import commands
from misc.logger import logger
from config.config import BB2_API_KEY

from misc.long_message import LongMessage

def sanitize(obj):
  """Make the msg safe to display"""
  msg = str(obj).replace(BB2_API_KEY,"***")
  return msg

class BotCog(commands.Cog):
  async def cog_command_error(self, ctx, error):
      msg = sanitize(error)
      await ctx.send(msg)
      text = type(error).__name__ +": "+msg
      logger.error(text)
      logger.error(traceback.format_exc())
      await ctx.send_help(ctx.command)
      await self.cog_after_invoke(ctx)

  @staticmethod
  async def send_embed(data, ctx):
    embed = discord.Embed(title=data['embed_title'], description=data['embed_desc'], color=0xEE8700)
    embed.set_thumbnail(url=data['thumbnail_url'])
    for field in data['embed_fields']:
        embed.add_field(name=field['name'], value=transform_message(field['value'], ctx), inline=field['inline'])
    await ctx.send(embed=embed)

  @staticmethod
  async def send_message(channel, message_list, block=False):
    """Sends messages to channel"""
    msg = LongMessage(channel, block=block)
    for message in message_list:
        msg.add(message)
    await msg.send()