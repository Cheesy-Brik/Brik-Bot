import discord
import random
from discord.ext import commands, bridge, pages
import os
import time
import io
import bz2
from fuzzywuzzy import process
from discord.ui import button, View, Button
from discord.interactions import Interaction
import inspect
import copy
import sys
from typing import get_type_hints
from discord import Embed

botid = eval(open(r"cogs\id.txt", "r", encoding="utf8").read())

def load_save(file: str, fallback={}):
    try:
        return eval(
            open(
                r"cogs/" + file + r".txt", "r", encoding="utf-8", errors="ignore"
            ).read()
        )
    except FileNotFoundError:
        return fallback

def dump_save(file_name: str, value):
    if botid != 764921656199872523 and file_name != "sussy":
        return
    try:
        with open(f"cogs/{file_name}.txt", "r", encoding="utf8") as file:
            content = file.read()
    except FileNotFoundError:
        content = None

    if content != str(value):
        with open(f"cogs/{file_name}.txt", "w", encoding="utf8") as file:
            file.write(str(value))

def patch_dict(template, user_dict):
    for key, value in template.items():
        if key not in user_dict:
            user_dict[key] = value
        else:
            if type(value) is not type(user_dict[key]):
                try:
                    user_dict[key] = type(value)(user_dict[key])
                except ValueError:
                    user_dict[key] = value
            elif isinstance(value, dict):
                patch_dict(value, user_dict[key])
    return user_dict

def correct_spelling(misspelled, possibilities):
    closest_match = process.extractOne(misspelled, possibilities)
    return closest_match[0]

_cmd_registry = {}

def traverse_by_path(vfs, filepath):
    path = filepath.split(">")
    current_dir = vfs
    try:
        while path:
            if path[0] == "main":
                current_dir = vfs[path.pop(0)]
                continue
            if "rlocked" in current_dir["data"][path[0]]["args"]:
                return current_dir
            current_dir = current_dir["data"][path.pop(0)]
        return current_dir
    except KeyError:
        return None

mine_temp = {
    "users" : {},
}
user_temp = {
    "inv" : {},
    "current_depth": 0,
    "equipped" : {
        "pick" : 0,
        "accessory" : None,
    },
    "backpack size" : 50,
}

picks = {
    0 : {
        "name" : "Starter Pickaxe",
        "speed" : lambda user: 1,
    }
}

depths = {
    5 : {"dirt" : 10, "gravel" : 5},
    10 : {"gravel" : 8, "dirt" : 5, "stone" : 10, "copper" : 5,"iron" :2},
    20 : {"dirt" : 2, "stone" : 10, "copper" : 10,"iron" : 5},
    25 : {"stone" : 10, "copper" : 5, "iron" : 10},
    30 : {"stone" : 10, "copper" : 10, "iron" : 5},
    33 : {"stone" : 10, "iron" : 5},
    34 : {"sex crystal" : 1, "stone" : 20},
    35 : {"stone" : 10, "iron" : 10},
}

mine_data = load_save("mine_data", )

def blend_dict(dict1:dict,dict2:dict, transition:float) -> dict:
        result = {key:value*transition for key,value in dict2.items()}
        for key,value in {key:value*(1-transition) for key,value in dict1.items()}.items():
            if key not in result:result[key] = value
            else:result[key] += value
        return result

def weighted_choice(dict):
    return random.choices(list(dict.keys()), weights = tuple(dict.values()), k = 1)

class MINE:
    def __init__(self, ctx=None, user=None):
        self.ctx = ctx
        self.user = user

    async def __page(
        self, items, items_per_page=10, page_title="test", page_footer="test"
    ):
        class ViewWithButton(View):
            def __init__(self, ctx):
                super().__init__(timeout=120)
                self.num = 1
                self.disabled = False
                self.ctx = ctx

                async def check(interaction):
                    return interaction.user.id == self.ctx.author.id

                self.interaction_check = check

            @button(style=discord.ButtonStyle.blurple, emoji="◀️")
            async def back(
                self,
                button: Button,
                interaction: Interaction,
            ):
                if self.num > 1:
                    # button.disabled = False
                    self.num -= 1
                else:
                    self.num = len(pageinv)
                    # button.disabled = True
                embed = discord.Embed(
                    title=f"Help(Page {self.num})", description=pageinv[self.num - 1]
                )
                embed.set_footer(text="Get more some info with !invite")
                await msg.edit(embed=embed, view=self)
                await interaction.response.defer()

            @button(style=discord.ButtonStyle.blurple, emoji="⏹")
            async def kill(
                self,
                button: Button,
                interaction: Interaction,
            ):
                self.stop()
                await msg.edit(embed=embed, view=None)
                await interaction.response.defer()

            @button(style=discord.ButtonStyle.blurple, emoji="▶️")
            async def next(
                self,
                button: Button,
                interaction: Interaction,
            ):
                if self.num < len(pageinv):
                    # button.disabled = False
                    self.num += 1
                else:
                    self.num = 1
                    # button.disabled = True
                embed = discord.Embed(
                    title=f"{page_title} (Page {self.num})",
                    description=pageinv[self.num - 1],
                )
                embed.set_footer(text=page_footer)
                await msg.edit(embed=embed, view=self)
                await interaction.response.defer()

        reg1 = 0
        inv = []
        pageinv = []

        for i in items:
            inv.append(i)
            reg1 += 1
            if reg1 == items_per_page:
                pageinv.append("\n".join(inv))
                inv = []
                reg1 = 0

        if reg1 != items_per_page and inv:
            pageinv.append("\n".join(inv))

        embed = discord.Embed(title=page_title + " (Page 1)", description=pageinv[0])
        embed.set_footer(text=page_footer)
        msg = await self.ctx.respond(embed=embed, view=ViewWithButton(self.ctx))

        return msg

    async def __grab_item(self, depth):
        index1 = None
        index2 = None
        for key, value in depths.items():
            if key > depth:
                index2 = key
                break
            if index1 == None or depth-key<index1:
                index1 = key
        if index2 == None:
            index2 = index1
        if index1 == None:
            index1 = index2
        blending_value = 0
        try:
            blending_value = (depth - index1)/(index2 - index1)
        except:
            pass
        item = self.weighted_choice(self.blend_dict(depths[index1], depths[index2], blending_value))
        if callable(item):
            return item()
        return item[0]

    async def __main__(self):
        message = ""
        self.user['current_depth'] += picks[self.user["equipped"]["pick"]]["speed"](self.user)
        message += f"You mined to {self.user['current_depth']}m!"
        await self.ctx.respond(message)
    
    async def help(self, command: str = ""):
        "Shows this command"
        commands = [
            getattr(self, attr)
            for attr in dir(self)
            if callable(getattr(self, attr))
            and hasattr(getattr(self, attr), "__code__")
            and "__" not in getattr(self, attr).__name__
        ]
        if command == "":
            await self.__page(
                [
                    f"* **{i.__name__.title()}**\n    {i.__doc__} "
                    for i in commands
                    if i.props["view"](self)
                ],
                10,
                "Help",
                "Do !mine help | <command> to get more info!",
            )
        else:
            command = getattr(
                self, correct_spelling(command.lower(), [i.__name__ for i in commands])
            )
            command_desc = command.__doc__
            command_desc += "\n\nFormat: ```\n!mine " + command.__name__
            type_names = {int: "Number", str: "Text"}
            for name, param in inspect.signature(command).parameters.items():
                command_desc += (
                    f" | <{name.title().replace('_', ' ')} : {type_names.get(param.annotation) or param.annotation.__name__}"
                    + (" (Optional)" if param.default != inspect._empty else "")
                    + ">"
                )
            command_desc += "\n```"
            embed = discord.Embed(
                title=command.__name__.title(), description=command_desc
            )
            embed.set_footer(text='Each parameter must be seperated by "|"')
            await self.ctx.respond(embed=embed)

    async def dev(self, cmd: str = ""):
        args = cmd.split(";")[1:]
        cmd = cmd.split(" ")[0].split(";")[0]

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @bridge.bridge_command(aliases=["m"])
    async def mine(self, ctx: bridge.BridgeContext, *, sub_command: str = ""):
        global mine_data
        
        mine_data = patch_dict(mine_temp, mine_data)
        
        if ctx.author.id not in mine_data["users"]:
            mine_data["users"][ctx.author.id] = {}
        patch_dict(user_temp, mine_data["users"][ctx.author.id])

        user = mine_data["users"][ctx.author.id]
        ####

        game = MINE(ctx, user)

        commands = [
            getattr(game, attr)
            for attr in dir(game)
            if callable(getattr(game, attr))
            and hasattr(getattr(game, attr), "__code__")
            and "__" not in getattr(game, attr).__name__
        ]

        if sub_command == "":
            await game.__main__()
        else:
            sub_command = sub_command.split("|")
            command = getattr(
                game,
                correct_spelling(
                    sub_command[0].lower(), [i.__name__ for i in commands]
                ),
            )
            if not command.props["use"](game):
                await ctx.respond("You cannot use this command!")
                return

            args = []
            for i, param in zip(
                sub_command[1:], inspect.signature(command).parameters.values()
            ):
                if param.annotation is str:
                    args.append(i.strip())
                else:
                    args.append(eval(i.strip()))
            await command(*args)
        mine_data["users"][ctx.author.id] = game.user

        dump_save("mine_data", mine_data)

def setup(client):
    client.add_cog(Mine(client))
