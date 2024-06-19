import discord
import os
from discord.ext import commands, bridge
from discord.ext.commands.bot import Bot
from discord.ui import button, View, Button
from discord.interactions import Interaction
import sys

intents = discord.Intents(
    messages=True,
    guilds=True,
    reactions=True,
    members=True,
    presences=True,
    message_content=True,
)
client = bridge.Bot(
    command_prefix=["^","!"],
    case_insensitive=True,
    intents=intents,
)
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Streaming(
            name="!help and !server",
            url="https://www.twitch.tv/Brik-Bot-2000-Official-Server---discord.gg/VnZym5v6dp",
        )
    )
    print("Boot up complete")

@client.event
async def on_command_error(ctx:bridge.BridgeContext, error:commands.CommandError):
    #type:ignore
    import traceback
    if type(error) in [commands.errors.CommandNotFound, discord.errors.Forbidden]:
        return
    try:
        if type(error) != commands.errors.MissingRequiredArgument:
            await client.get_user(666999744572293170).send("ERROR: " + ctx.message.jump_url + "\nTRACE: " + ''.join(traceback.format_exception(type(error), error, error.__traceback__)))
    except:
        await client.get_user(666999744572293170).send("ERROR: " + ctx.message.jump_url + "\nTRACE: " + "Printed in console...")
        print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
    if isinstance(error, commands.CommandError):
        await ctx.reply("Command Error: ```\n" + str(error).replace(':', ':\n') + "```")
    elif isinstance(error, Exception):
        await ctx.reply("Unexpected Error: ```\n" + str(error).replace(':', ':\n') + "```")
    else:
        print(f"Unexpected error: {error}")
    
@client.listen("on_message")
async def same(text):
    if text.author == client.user:
        return
    if len(text.content) == 1:
        await text.reply("same")

@client.listen("on_message")
async def welcome(text):
    if text.author == client.user:
        return
    if text.channel.id == 819407737053511713:
        await text.channel.send(
            f"Welcome {text.author.mention}!\n Check out <#1060380303153188884> to choose your roles!"
        )


@client.command(aliases=["Yeah", "Great", "Brik"])
async def Good(ctx, bot):
    if bot.lower() == "bot":
        await ctx.send("H")

@client.command()
async def restart_bot(ctx):
    if ctx.author.id != 666999744572293170:
        return
    try:
        await ctx.reply("Restarting...")
    except:
        pass
    os._exit(3)

@client.command()
async def kill_bot(ctx):
    if ctx.author.id != 666999744572293170:
        return
    try:
        await ctx.reply("Exiting...")
    except:
        pass
    os._exit(4)

@client.command()
async def help(ctx, *, txt="all"):
    "Shows this"

    class ViewWithButton(View):
        def __init__(self):
            super().__init__(timeout=120)
            self.num = 1
            self.disabled = False

            async def check(interaction):
                return interaction.user.id == ctx.author.id

            self.interaction_check = check

        @button(style=discord.ButtonStyle.blurple, emoji="◀️")
        async def back(self, button: Button, interaction: Interaction):
            if self.num > 1:
                # button.disabled = False
                self.num -= 1
            else:
                pass
                # button.disabled = True
            embed = discord.Embed(
                title=f"Help(Page {self.num})", description=pageinv[self.num - 1]
            )
            embed.set_footer(text="Get more some info with !invite")
            await msg.edit(embed=embed, view=self)
            await interaction.response.defer()

        @button(style=discord.ButtonStyle.blurple, emoji="⏹")
        async def kill(self, button: Button, interaction: Interaction):
            self.stop()
            await msg.edit(embed=embed, view=None)
            await interaction.response.defer()

        @button(style=discord.ButtonStyle.blurple, emoji="▶️")
        async def next(self, button: Button, interaction: Interaction):
            if self.num < len(pageinv):
                # button.disabled = False
                self.num += 1
            else:
                pass
                # button.disabled = True
            embed = discord.Embed(
                title=f"Help(Page {self.num})", description=pageinv[self.num - 1]
            )
            embed.set_footer(text="Get more some info with !invite")
            await msg.edit(embed=embed, view=self)
            await interaction.response.defer()

    reg1 = 0
    inv = []
    pageinv = []
    num = 1

    if txt != "all":
        pass
    for i in sorted(list(client.commands), key=lambda item: item.name):
        inv.append(
            (
                f"-**{str(i.name)}**- "
                + (
                    ("(" + ", ".join(aliase for aliase in i.aliases) + ")")
                    if i.aliases
                    else ""
                )
            )
            + "\n"
            + (i.help if i.help else "")
        )
        reg1 += 1
        if reg1 == 10:
            pageinv.append("\n".join(inv))
            inv = []
            reg1 = 0

    if reg1 != 10:
        pageinv.append("\n".join(inv))

    embed = discord.Embed(title="Help(Page 1)", description=pageinv[0])
    embed.set_footer(text="Get more some info with !invite")
    msg = await ctx.reply(embed=embed, view=ViewWithButton())

botid = 0

if len(sys.argv) > 1:
    print(sys.argv)
    botid = 764921656199872523
else:
    print("___RUNNING BETA___")
    botid = 931369681560944650

Write = open("cogs/id.txt", "w", encoding="utf8")
Write.write(str(botid))
Write.close()

for filename in os.listdir(
        r"C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs"
    ):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

if botid == 764921656199872523:
    client.run(<MAIN BOT ID>)
else:
    client.run(<BETA BOT ID>)