import discord
import requests
from discord.ext import commands
from base_cog import BotCog
from misc.bb2 import agent

class Common(BotCog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def team(self, ctx, *, team_name):
        """Returns team info"""
        team = agent.team(team_name)
        if not team:
          await ctx.send(f"Error: Team {team_name} does not exist")
          return
        team_id = team['team']['id']
        url = f"https://rebbl.net/api/v2/team/{team_id}"
        r = requests.get(url = url)
        data = r.json()
        if not data.get('team', None):
          await ctx.send(f"Error: Team {team_name} is not REBBL team")
          return
        embed = discord.Embed(\
            title=data['team']['name'], \
            url=url,\
            description=data['team']['leitmotiv'] )
        embed.set_thumbnail(url=f"https://cdn2.rebbl.net/images/logo/256x256/logo_{data['team']['logo'].lower()}.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Common(bot))