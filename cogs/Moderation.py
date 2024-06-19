import discord
from discord.ext import commands, bridge
import time
    


class Moderation(commands.Cog):

 def __init__(self, client):
     self.client = client
	
 @commands.Cog.listener()
 async def on_ready(self):
     print('Cogs Loaded')

 @bridge.bridge_command()
 async def ping(self, ctx:bridge.BridgeContext):
     
     await ctx.send(f'{ctx.author.mention} Pong {round(max(time.time() - ctx.message.created_at.timestamp(), self.client.latency)*1000)}ms')
 
 @bridge.bridge_command(aliases = ['serv'])
 async def servers(self, ctx):
    servers = list(self.client.guilds)
    await ctx.send(f"Connected on {str(len(servers))} servers:")
    if ctx.channel.id != 764925802214195221:
        await ctx.send('\n'.join( (f"{guild.name} - ({str(len(guild.members))} members)") for guild in servers))
    else:
        await ctx.send('\n'.join( (f"{guild.name} - ({str(len(guild.members))} members) (owner:{guild.owner})") for guild in servers))
 

 

 
 #@commands.command()
 #async def clear(self, ctx, amount=5):
 #    await ctx.channel.purge(limit=amount + 1)

def setup(client):
    client.add_cog(Moderation(client))
