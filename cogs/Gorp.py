import discord
import random
from discord.ext import commands, bridge

    
global blocked
blocked = []
global server
server = 0
global servuser
servuser = {}
global servtotal
servtotal = 0

class Gorp(commands.Cog):

 def __init__(self, client):
     self.client = client

 #@commands.command()
 #async def spam(self, ctx, *, text):
 #    split = list(text)
 #    if len(split) <= 10:
 #        for i in split:
 #            await ctx.send(i)
 #    else:
 #        response = ["I get it's called spam but come on", "You really want me to spam that?? Na", "You are a physcopath if you think imma spam that", "Too much letter, no", "[insert response the says the message is over the character limit in a funny way]", f"{text} -- {ctx.author.nick} A.K.A. Someone who thought this was an acceptable spam amount"]
 #        await ctx.send(f'{random.choice(response)}')
 #@commands.command()
 #async def spamcaleb(self, ctx):
 #    await ctx.send()
 
 @commands.command()
 async def block(self, ctx, user):
     if ctx.author.id == 666999744572293170:
         blocked.append(int(user))
         await ctx.send('User Blocked :)')
         print(blocked)
     else:
         await ctx.send('You are NOT Cheesy Brik')

 @commands.command()
 async def unblock(self, ctx, user):
     if ctx.author.id == 666999744572293170:
         blocked.remove(int(user))
         await ctx.send('User Unblocked :)')
         print(blocked)
     else:
         await ctx.send('You are NOT Cheesy Brik')


 @commands.command()
 async def submit(self, ctx, command, *, txt = '\n---No Message---\n'):
     block = False
     for i in blocked:
         if ctx.author.id == i:
             block = True
     if block == False:

         found = 0
         accepted = ['rat', 'rats', 'frog', 'frogs', 'gif', 'creature', 'trait', 'item']
         for i in accepted:
             if command.lower().replace(' ','') == i:
                 found = 1
                 await ctx.send(f"Your submission for {command} will be reviewed :)")
                 me = self.client.get_user(666999744572293170)
                 try:
                     await me.send(f'User: {ctx.message.author.name} / {ctx.message.author.id}\nCommand:{i}\nSubmission:{str(ctx.message.attachments[0].url)}{txt}')
                 except:
                     await me.send(f'User:{ctx.message.author.name} / {ctx.message.author.id}\nCommand:{i}\nSubmission:{txt}')
         if found == 0:
             await ctx.send(f"Sorry we're only accepting submissions for {accepted}")
     else:
         await ctx.send("You're blocked from submitting :(")

 @commands.command()
 async def send(self, ctx, user, *, txt):
     if ctx.author.id == 666999744572293170:
         await self.client.get_user(int(user)).send(f'"*{txt}*"')
         await ctx.send('Sent :+1:')
     else:
         await ctx.send('You are NOT Cheesy Brik')
 
 @commands.command()
 async def say(self, ctx, channel, *, txt):
     if ctx.author.id == 666999744572293170:
         await self.client.get_channel(int(channel)).send(txt)
     else:
         await ctx.send('You are NOT Cheesy Brik')
 
 @bridge.bridge_command(aliases = ['invite', 'server'])
 async def about(self, ctx):
     await ctx.send(" Brik bot is just my(Cheesy Brik) genreal purpose bot for anything I want to do bot wise. There is a lot it can do so it's very scattered, but I think it would be worth adding to your server.\nTo invite Brik Bot to your server go to the their profile and click add to server\n The offcial Brik Bot server invite link is https://discord.gg/VnZym5v6dp")                   
        
def setup(client):
    client.add_cog(Gorp(client))
