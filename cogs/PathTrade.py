import discord
import random
from discord import AutocompleteContext
from discord.ext import commands, bridge, pages
from discord.commands import option as option_decorator
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


def group_by_n(input_list, n):
    return [tuple(input_list[i:i + n]) for i in range(0, len(input_list), n)]

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


botid = eval(open(r"cogs\id.txt", "r", encoding="utf8").read())

paths = load_save("path", [])

bans = load_save("path_bans", [])

s_times = load_save("stimes", 0)

s_users = load_save("sussy")

with open(f"cogs/query (1).txt", "r", encoding="utf8") as file:
    elements_by_id = [i.lower() for i in file.read().split("\n")]
elements_by_id = {i: index for index, i in enumerate(elements_by_id)}


s_items = {
    "gun": {
        "name": "Gun",
        "desc": "Allows you to `reload` the gun costing 5sp, with the chance of it firing off and giving you back 10sp while sexing",
        "uses": ["reload"],
        "meta": {"reloaded": False, "reload cost": 5},
    },
    "cookie": {
        "name": "Warm Cookie",
        "desc": "Every sex will give +1 sp because it's a good sex snack\n(Does stack)",
        "uses": [],
        "meta": {},
    },
    "bladder": {
        "name": "Failing Bladder",
        "desc": "Filters out and rerolls an item drop once if you already have that item \n(Does stack)",
        "uses": [],
        "meta": {},
    },
    "carrot": {
        "name": "Carrot",
        "desc": "When `consume`d will give you better eyesight and a higher chance of finding items for the next 5 minutes\nCan only be consumed once every 30 minutes \n(Does not stack)",
        "uses": ["consume"],
        "meta": {"last consumed": 0, "consume gap": 1200},
    },
    "cross": {
        "name": "Golden Cross",
        "desc": "Prevents greed and item drops from happening",
        "uses": [],
        "meta": {},
    },
    "filter": {
        "name": "Coffee Filter",
        "desc": "Makes items you already have less likely to appear \n(Does Stack)",
        "uses": [],
        "meta": {},
    },
    "shotgun": {
        "name": "Shotgun",
        "desc": "Allows you to `reload` the shotgun costing 50sp, with the chance of it firing off and giving you back 120sp while sexing",
        "uses": ["reload"],
        "meta": {"reloaded": False, "reload cost": 50},
    },
    "sheep": {
        "name": "Sheep Plushie",
        "desc": "Encourages you to follow the herd and gives you +3 sp every time you get an item you already have\n(Does Stack)",
        "uses": [],
        "meta": {},
    },
    "dice": {
        "name": "Cursed Dice",
        "desc": "Will randomly roll between -6sp and +6sp, will not make total sex points gained go below 0\n(Does Stack)",
        "uses": [],
        "meta": {},
    },
    "liquor": {
        "name": "Bottle of Liquor",
        "desc": "When `consume`d will give you better sexing skills for 2 minutes, giving a 5% sp boost\nCan only be consumed once every 20 minutes \n(Does stack)",
        "uses": ["consume"],
        "meta": {"last consumed": 0, "consume gap": 1800},
    },
    "seed": {
        "name": "Seed",
        "desc": "When `plant`ed will grow after 20-30 minutes giving 55sp",
        "uses": ["plant"],
        "meta": {
            "planted": False,
            "sprout time": 0,
            "min sprout time": 20 * 60,
            "max sprout time": 30 * 60,
        },
    },
}

cast_meta_data = {
    "reloaded": lambda i: f"{'Yes' if i else 'No'}",
    "last_consumed": lambda i: f"<t:{int(i)}:R>",
    "planted": lambda i: f"{'Yes' if i else 'No'}",
}

s_template = {
    "inv": [],
    "equipped": [],
    "sp": 0,
    "modifiers": [],
    "rebirths": 0,
}


class SEX:
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

    def __drop_item(self, reroll=False):
        global s_times
        user = self.user
        item_ids = [i["id"] for i in user["inv"]]
        equipped_item_ids = [user["inv"][i]["id"] for i in user["equipped"]]

        possible_items = []

        if user["sp"] < 10:
            return

        if (
            random.randint(0, min(len(user["inv"]), 4)) != 0
            and not any(
                [
                    (time.time() - user["inv"][i]["last consumed"] < 60 * 5)
                    for i in user["equipped"]
                    if user["inv"][i]["id"] == "carrot"
                ]
            )
            and not reroll
        ):
            return

        if "cross" in equipped_item_ids:
            return

        if s_times > 25:
            if (
                random.randint(
                    0, 12 - (5 * int("5" in str(s_times) or "gun" not in item_ids))
                )
                == 0
            ):
                possible_items.append("gun")

        for i in str(s_times):
            if i == "7":
                if random.randint(0, 3) == 0:
                    possible_items.append("cookie")
                    break
            else:
                if random.randint(0, 15) == 0:
                    possible_items.append("cookie")
                    break

        if s_times > 100 and len(user["inv"]) > 5:
            if random.randint(
                0, 12 - int("6" in str(s_times)) - int("9" in str(s_times))
            ):
                if random.randint(0, item_ids.count("bladder")) == 0:
                    possible_items.append("bladder")

        if (
            "bladder" in item_ids
            and random.randint(0, 12) == 0
            and item_ids.count(i) > 3
        ):
            possible_items.append("filter")

        if item_ids.count("gun") > 2 and "gun" in equipped_item_ids:
            if "shotgun" not in item_ids:
                possible_items.append("shotgun")
            elif random.randint(0, 18 - 7 * int("16" in str(s_items))) == 0:
                possible_items.append("shotgun")

        if "1" in str(s_times):
            for i in set(item_ids):
                if item_ids.count(i) > 2:
                    if random.randint(0, 6) == 0:
                        possible_items.append("carrot")
                        break
        else:
            for i in set(item_ids):
                if item_ids.count(i) > 2:
                    if random.randint(0, 16) == 0:
                        possible_items.append("carrot")
                        break

        if len(user["inv"]) > 10 and "cross" not in item_ids:
            possible_items.append("cross")

        if [item_ids.count(i) for i in set(item_ids)] and max(
            [item_ids.count(i) for i in set(item_ids)]
        ) > 5:
            if (
                random.randint(0, 10 - 5 * int("2" in str(s_times)))
                and random.randint(0, item_ids.count("sheep") // 2) == 0
            ):
                possible_items.append("sheep")

        if "cross" in item_ids and random.randint(0, 6 + item_ids.count("dice")) == 0:
            possible_items.append("dice")

        if (
            "gun" in item_ids
            and random.randint(0, 10 + item_ids.count("liquor") * 4) == 0
        ):
            possible_items.append("liquor")

        ####

        item_pool = []

        # print(possible_items)

        for i in possible_items:
            if (
                i in item_ids
                and random.randint(0, 2 + equipped_item_ids.count("filter") * 2) == 0
            ):
                item_pool.append(i)

        return random.choice(item_pool) if item_pool else None

    def __format_sp(self, amount):
        return f"{'+' if amount > 0 else ''}{amount}sp"

    def __remove_item(self, item_index):
        item = self.user["inv"].pop(item_index)
        new_equipped = copy.copy(self.user["equipped"])
        for index, i in enumerate(self.user["equipped"]):
            if i == item_index:
                new_equipped.pop(index)
            elif i > item_index:
                new_equipped[index] -= 1

    def __convert_str_to_range(self, string: str):
        start, stop = string.strip().replace(" ", "").split("-")
        range(int(start), int(stop))

    def __give_item(self, item_id: str):
        item_id = item_id.lower().strip()
        self.user["inv"].append(copy.deepcopy(s_items[item_id]["meta"]))
        self.user["inv"][-1].update({"id": item_id})
        self.user["inv"][-1].update({"unique id": random.randint(0, 2**8)})

    async def __sex__(self):
        global s_times
        total_sp = 0

        msg = ""

        if True:
            msg += "You did the sexed!"
            total_sp += 1

        ####
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "shotgun":
                if (
                    self.user["inv"][i]["reloaded"] == True
                    and random.randint(0, 14) == 0
                ):
                    self.user["inv"][i]["reloaded"] = False
                    msg += (
                        f"\nYour {s_items['gun']['name']} in equip slot {self.user['equipped'].index(i)+1} went off! "
                        + self.__format_sp(120)
                    )
                    total_sp += 120
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "gun":
                if (
                    self.user["inv"][i]["reloaded"] == True
                    and random.randint(0, 6) == 0
                ):
                    self.user["inv"][i]["reloaded"] = False
                    msg += (
                        f"\nYour {s_items['gun']['name']} in equip slot {self.user['equipped'].index(i)+1} went off! "
                        + self.__format_sp(10)
                    )
                    total_sp += 10
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "cookie":
                msg += (
                    f"\nYour {s_items['cookie']['name']} in equip slot {self.user['equipped'].index(i)+1} tasted good! "
                    + self.__format_sp(1)
                )
                total_sp += 1
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "dice":
                num = random.randint(-6, 6)
                msg += (
                    f"\nYour {s_items['dice']['name']} in equip slot {self.user['equipped'].index(i)+1} rolled a {num}! "
                    + self.__format_sp(num)
                )
                total_sp = max(total_sp + num, 0)
        ####

        item = self.__drop_item()
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "bladder":
                if item in [j["id"] for j in self.user["inv"]]:
                    new_item = self.__drop_item(True)
                    if new_item:
                        msg += f"\nYour {s_items['bladder']['name']} in equip slot {self.user['equipped'].index(i)+1} rerolled an item!"
                        item = new_item
                else:
                    break

        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "sheep":
                if item in [i["id"] for i in self.user["inv"]]:
                    msg += (
                        f"\nYour {s_items['sheep']['name']} in equip slot {self.user['equipped'].index(i)+1} was happy you got something you've seen before! "
                        + self.__format_sp(3)
                    )
                    total_sp += 3

        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "seed":
                print(self.user["inv"][i]["sprout time"] - time.time())
                if (
                    self.user["inv"][i]["sprout time"] - time.time() < 0
                    and self.user["inv"][i]["sprout time"] != 0
                ):
                    msg += (
                        f"\nYour {s_items['seed']['name']} in equip slot {self.user['equipped'].index(i)+1} sprouted!"
                        + self.__format_sp(50)
                    )
                    total_sp += 50

        if item:
            name = s_items[item]["name"]
            if name[0] in "aeiou":
                msg += f"\nYou got an {name}!"
            else:
                msg += f"\nYou got a {name}!"

            if not self.user["inv"]:
                msg += " (Use !sex inv to see your items)"

            self.__give_item(s_items[item]["id"])

        ####
        for i in self.user["equipped"]:
            if self.user["inv"][i]["id"] == "liquor":
                if time.time() - self.user["inv"][i]["consumed"] < 60 * 2:
                    total_sp *= 1.05
        ####
        msg += f"\n{'+' if total_sp >= 0 else ''}{total_sp} sex points"

        if self.user == s_template:
            msg += "\n\nWelcome to sex, use !sex help to get a list of commands. And do !sex help | help to get even more info"

        msg += f"\n\nSex counter: {s_times}"
        await self.ctx.respond(msg)
        s_times += total_sp
        self.user["sp"] += total_sp

    async def inv(self, inv_slot: int = 0):
        "Shows your inventory"
        if len(self.user["inv"]) == 0:
            await self.ctx.respond("You don't have any items!")
            return
        if not inv_slot:
            await self.__page(
                [
                    f"{index+1}. **{s_items[i['id']]['name']}**"
                    + (" - *Equipped*" if index in self.user["equipped"] else "")
                    for index, i in enumerate(self.user["inv"])
                ],
                15,
                "Inventory",
                "Do !sex inv | <item index> to get more info on that item",
            )
        else:
            try:
                inv_slot = abs(inv_slot) - 1
                item_desc = ""
                item = self.user["inv"][inv_slot]
                item_desc += (
                    f"**Equipped in equip slot {self.user['equipped'].index(inv_slot) + 1}**\n"
                    if inv_slot in self.user["equipped"]
                    else "*Not Equipped*\n"
                )
                item_desc += s_items[item["id"]]["desc"] + "\n\n"
                for key, value in item.items():
                    if key in cast_meta_data:
                        item_desc += (
                            f"**{key.title()}**: {cast_meta_data[key](value)}\n"
                        )
                item_desc += (
                    "\nAvailable actions: ```\n"
                    + "\n".join([i.title() for i in s_items[item["id"]]["uses"]])
                    + "\n```"
                )
                embed = discord.Embed(
                    title=s_items[item["id"]]["name"] + f" ({inv_slot+1})",
                    description=item_desc,
                )
                embed.set_footer(
                    text="An item's effect only takes place when equipped\nDo !sex equip | <item index> to equip this item in the first available slot"
                )
                await self.ctx.respond(embed=embed)
            except IndexError:
                await self.ctx.respond("Not a valid item index")

    async def equip(self, inv_slot: int, equip_slot: int = -1):
        "Equips an item of a specified inv slot"
        msg = ""
        if inv_slot == -1:
            inv_slot = len(self.user["inv"]) - 1
        else:
            inv_slot -= 1
        if equip_slot != -1:
            equip_slot -= 1
        if equip_slot > self.user["rebirths"] + 2:
            await self.ctx.respond("You don't have that many equip slots!")
            return
        if inv_slot > len(self.user["inv"]) - 1:
            await self.ctx.respond("You do not have an item in that inventory slot!")
            return
        if inv_slot in self.user["equipped"]:
            await self.ctx.respond(
                f"You already have that item equipped in equip slot {self.user['equipped'].index(inv_slot)+1}"
            )
            return
        if equip_slot != -1:
            if equip_slot > len(self.user["equipped"]) - 1:
                msg += "You don't have anything equipped in that equip slot, equipping to the nearest slot\n"
                equip_slot = -1
            else:
                msg += f"Replacing item of inv slot {self.user['equipped'][equip_slot] + 1} with the new equip slot\n"
        else:
            if len(self.user["equipped"]) == self.user["rebirths"] + 3:
                await self.ctx.respond(
                    f"You can currently only equip {self.user['rebirths']+3} items at once!"
                )
                return
        new = len(self.user["equipped"]) == 0
        if equip_slot == -1:
            self.user["equipped"].append(None)
            equip_slot = len(self.user["equipped"]) - 1
        self.user["equipped"][equip_slot] = inv_slot
        msg += f"Equipped item {s_items[self.user['inv'][inv_slot]['id']]['name']} in equip slot {equip_slot+1}"
        msg += (
            f"\n\nUse !sex use to use | <inv slot> | <action> equipped items"
            if new
            else ""
        )
        await self.ctx.respond(msg)

    async def equipped(self):
        "Shows what items you have equipped"
        await self.__page(
            [
                f"{index+1}. **{s_items[self.user['inv'][i]['id']]['name']}**\n    Inv slot {i+1} "
                if i != None
                else " *Nothing Equipped*"
                for index, i in enumerate(
                    self.user["equipped"]
                    + [None]
                    * (len(self.user["equipped"]) - (self.user["rebirths"] + 3))
                )
            ],
            10,
            "Equipped",
            "Do !sex unequip | <equip_slot> to unequip an item",
        )

    async def unequip(self, equip_slot: int):
        "Unequips an item of a specified equip slot"
        equip_slot -= 1
        if equip_slot > len(self.user["equipped"]) - 1 or equip_slot < -len(
            self.user["equipped"]
        ):
            await self.ctx.respond("Not a valid equip_slot")
            return
        item = self.user["inv"][self.user["equipped"][equip_slot]]
        match item["id"]:
            case "gun":
                if item["reloaded"]:
                    await self.ctx.respond(
                        "You cannot unequip a loaded gun (It's dangerous)"
                    )
                    return
            case "shotgun":
                if item["reloaded"]:
                    await self.ctx.respond(
                        "You cannot unequip a loaded shotgun (It's dangerous)"
                    )
                    return
            case "carrot":
                if item["consumed"]:
                    await self.ctx.respond(
                        "The carrot's already gone? (Consumables are unequipable after being consumed)"
                    )
                    return
            case "seed":
                if item["planted"]:
                    await self.ctx.respond(
                        "The seeds in the ground. Maybe wait till it's grown to unequip it."
                    )
                    return
        inv_slot = self.user["equipped"].pop(equip_slot)
        await self.ctx.respond(
            f"Unequipped item {s_items[self.user['inv'][inv_slot]['id']]['name']} in equip slot {equip_slot+1}"
        )

    async def unequip_all(self):
        "Unequips all items"
        length = len(self.user["equipped"])
        for i in range(length):
            await self.unequip(i + 1)
        await self.ctx.respond(
            f"Unequipped {length-len(self.user['equipped'])} item(s)"
        )

    async def use(self, equip_slot: int, action: str):
        "Allows you to use an item if an item has available actions"

        if equip_slot > 0:
            equip_slot -= 1
        try:
            self.user["equipped"][equip_slot]
        except IndexError:
            await self.ctx.respond("Not a valid equip index!")
            return

        inv_slot = self.user["equipped"][equip_slot]

        action = action.lower()

        if action not in s_items[self.user["inv"][inv_slot]["id"]]["uses"]:
            await self.ctx.respond("Not a valid action!")
            return

        item = self.user["inv"][inv_slot]
        match action:
            case "reload":
                if self.user["sp"] >= item["reload cost"]:
                    if not item["reloaded"]:
                        self.user["sp"] -= item["reload cost"]
                        item["reloaded"] = True
                        await self.ctx.respond(
                            f"Reloaded {s_items[item['id']]['name']} in inv slot {inv_slot + 1} "
                            + self.__format_sp(-item["reload cost"])
                        )
                    else:
                        await self.ctx.respond(f"That item is already reloaded!")
                else:
                    await self.ctx.respond(
                        "You do not have enough sex points to reload"
                    )
            case "consume":
                if time.time() - item["last consumed"] > item["consume gap"]:
                    await self.ctx.respond(
                        f"Consumed {s_items[item['id']]['name']} in inv slot {inv_slot + 1}"
                    )
                    item["last consumed"] = time.time()
                else:
                    await self.ctx.respond(
                        f"That item cannot be consumed yet, it will be available to consume in <t:{int(item['last consumed'] + item['consume gap'])}:R>"
                    )
            case "plant":
                if not item["planted"]:
                    item["planted"] = True
                    item["sprout time"] = time.time() + random.randint(
                        item["min sprout time"], item["max sprout time"]
                    )
                else:
                    await self.ctx.respond("Item is already planted!")

    async def sp(self):
        "Shows your amount of sex points"
        await self.ctx.respond(f"Sex points: {self.user['sp']}")

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
                "Do !sex help | <command> to get more info!",
            )
        else:
            command = getattr(
                self, correct_spelling(command.lower(), [i.__name__ for i in commands])
            )
            command_desc = command.__doc__
            command_desc += "\n\nFormat: ```\n!sex " + command.__name__
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
        if cmd == "reset":
            if len(args) == 0:
                self.user = s_template
            else:
                s_users[int(args[0])] = s_template
        if cmd == "give":
            if len(args) == 1:
                self.__give_item(args[0])
            else:
                args[0] = args[0].lower().strip()
                s_users[int(args[1])]["inv"].append(
                    copy.deepcopy(s_items[args[0]]["meta"])
                )
                s_users[int(args[1])]["inv"][-1].update({"id": args[0]})
        if cmd == "sp":
            self.user["sp"] += int(args[0])


SEX.dev.props = {
    "view": lambda self: self.ctx.author.id == 666999744572293170,
    "use": lambda self: self.ctx.author.id == 666999744572293170,
}

props_def = {"view": lambda self: True, "use": lambda self: True}

pastas = load_save("pasta")

pastas = {k.lower(): v for k, v in pastas.items()}

async def autocomplete_pastas(ctx: AutocompleteContext):
    return sorted(list(pastas.keys()), key=lambda x: pastas[x]["votes"], reverse=True)

for i in [
    getattr(SEX(), attr)
    for attr in dir(SEX())
    if callable(getattr(SEX(), attr))
    and hasattr(getattr(SEX(), attr), "__code__")
    and "__" not in getattr(SEX(), attr).__name__
]:
    if "props" not in dir(i):
        i.__func__.props = copy.deepcopy(props_def)
    else:
        i.__func__.props = patch_dict(props_def, i.props)


class PathTrade(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @bridge.bridge_command()
    # async def spam(self, ctx, *, text):
    #    split = list(text)
    #    if len(split) <= 10:
    #        for i in split:
    #            await ctx.send(i)
    #    else:
    #        response = ["I get it's called spam but come on", "You really want me to spam that?? Na", "You are a physcopath if you think imma spam that", "Too much letter, no", "[insert response the says the message is over the character limit in a funny way]", f"{text} -- {ctx.author.nick} A.K.A. Someone who thought this was an acceptable spam amount"]
    #        await ctx.send(f'{random.choice(response)}')
    # @bridge.bridge_command()
    # async def spamcaleb(self, ctx):
    #    await ctx.send()

    @bridge.bridge_command(aliases=["dep"])
    async def dump_eod_path(self, ctx:bridge.BridgeContext, *, text=""):
        """
        Dumps the attached txt file or discord message into the path database
        format: !dump_eod_path <path or attached txt file>
        """
        global paths
        if ctx.author.id in bans:
            await ctx.respond(
                "You have been banned from dumping paths, this is either because you purposely added faulty paths to the database or you knowingly added outdated and or wrong paths.\nContact <@666999744572293170> if this was a mistake."
            )
            return

        combos = []
        if text:
            combos = (
                text.replace("!dep ", "").replace("!dump_eod_path ", "").split("\n")
            )
        elif len(ctx.message.attachments) > 0:
            combos = []
            for i in ctx.message.attachments:
                file = await i.read()
                combos += file.decode("utf8").split("\n")
        else:
            await ctx.respond(
                "You must attach paths to the command, through a text file or in the discord message."
            )
            return
        combos = [
            i.lower().strip()
            for i in [
                " + ".join(sorted([i.strip() for i in i.split("=")[0].split(" + ")]))
                + " = "
                + i.split("=")[-1].strip()
                for i in [i[i.find(".") + 1 :] if "." in i else i for i in combos]
            ]
        ]
        counter = 0
        msg = await ctx.respond(f"Scanning paths...")
        last_edited = time.time()
        amount_of_combos = len(combos)
        for index, i in enumerate(combos):
            if i not in paths and i and "=" in i and "+" in i:
                paths.append(i)
                counter += 1
            if time.time() - last_edited > 3.5:
                await msg.edit(
                    content=f"Found {counter} new paths!\nGone through {round((index+1)/amount_of_combos,5)*100}% of the file."
                )
                last_edited = time.time()
        await msg.edit(
            content=f"Thank you for the paths!\nYou added {counter} new paths!\nThe Brik Bot path database now has {len(paths)} paths!\nDo !paths_download, to get the txt file containing all current paths in the database."
        )
        dump_save("path", paths)

    @bridge.bridge_command(aliases=["pclean"])
    async def paths_clean(
        self, ctx:bridge.BridgeContext, sorting_method="highest_combo_id"
    ):
        if ctx.author.id != 666999744572293170:
            return

        global paths

        paths = [
            i.lower().strip()
            for i in [
                " + ".join(sorted([i.strip() for i in i.split("=")[0].split("+")]))
                + " = "
                + i.split("=")[-1].strip()
                for i in paths
            ]
        ]

        sorting_methods = ["result_id", "highest_combo_id"]
        paths = sorted(list(set(paths)))

        def return_path_value(i):
            if sorting_method == sorting_methods[0]:
                return elements_by_id.get(i.split("=")[:-1].strip(), float("inf"))
            elif sorting_method == sorting_methods[1]:
                return max(
                    [
                        elements_by_id.get(j.strip(), float("inf"))
                        for j in "".join(i.split("=")[:-1]).split(" + ")
                    ]
                )
            else:
                raise Exception(
                    f"Not a valid sorting method, valid sorting methods are {', '.join(sorting_methods)}"
                )

        paths = sorted(paths, key=return_path_value)

        paths = [
            i
            for i in paths
            if i and len(i.split("=")[0].split(" + ")) <= 21 and len(i) < 60000
        ]

        dump_save("path", paths)

        await ctx.respond("Database cleaned!")

    @bridge.bridge_command(aliases=["prem"])
    async def paths_custom_filter(self, ctx:bridge.BridgeContext):
        if ctx.author.id != 666999744572293170:
            return

        global paths

        indexs_to_remove = []

        for index, i in enumerate(paths):
            x = False
            for j in [i.strip() for i in i.split("=")[0].split(" + ")]:
                if j != "ms. pipis":
                    break
            else:
                indexs_to_remove.append(index)

        counter = 0

        for i in indexs_to_remove:
            counter += 1
            paths.pop(i)

        await ctx.respond(f"Removed {counter} paths!")

        if counter != 0:
            await self.paths_custom_filter(ctx)
        else:
            await self.paths_clean(ctx)

    @bridge.bridge_command(aliases=["pdown"])
    async def paths_download(self, ctx:bridge.BridgeContext):
        byte_data = "\n".join(paths).encode()
        byte_stream = io.BytesIO()
        with bz2.BZ2File(byte_stream, mode="w") as bz2_file:
            bz2_file.write(byte_data)

        byte_stream.seek(0)  # Reset the stream position to the beginning

        await ctx.author.send(
            content=f"The Brik Bot path database currently has {len(paths)} paths, please consider adding your own paths!\n To extract this use https://bz2.unzip.online/ or download WinRaR https://www.win-rar.com/download.html?&L=0",
            file=discord.File(byte_stream, filename="sample.txt.bz2"),
        )

    @bridge.bridge_command(aliases=["psearch"])
    async def paths_search(self, ctx:bridge.BridgeContext, *, text):
        text = text.lower().strip()
        msg = ""
        for i in paths:
            if i.split("=")[-1].strip() == text:
                msg += "\n`" + i + "`\n"
                if len(msg) > 2000:
                    msg = msg[:1980] + "..."
                    break
        if msg:
            await ctx.respond(msg)
        else:
            await ctx.respond("No paths could be found for that element :(")

    @bridge.bridge_command(aliases=["parch"])
    async def paths_archive(self, ctx:bridge.BridgeContext):
        if ctx.author.id != 666999744572293170:
            return

        await self.paths_clean(ctx)

        dump_save(f"path_archives/path_archive-{time.time()}", paths)
        await ctx.respond("Archived!")

    @bridge.bridge_command(aliases=["pcount"])
    async def paths_count(self, ctx:bridge.BridgeContext):
        await ctx.respond(
            f"The Brik Bot path database currently has {len(paths)} unique paths"
        )

    @bridge.bridge_command(aliases=["pecount"])
    async def paths_element_count(self, ctx:bridge.BridgeContext):
        await ctx.respond(
            f"The Brik Bot path database currently has {len(set([i.split('=')[-1] for i in paths]))} unique elements"
        )

    @bridge.bridge_command(aliases=["pban"])
    async def path_ban(self, ctx:bridge.BridgeContext, *, id=""):
        if ctx.author.id != 666999744572293170:
            return
        bans.append(id)
        await ctx.respond(f"Banned <@{id}> from adding paths")
        dump_save("path_bans", bans)

    @bridge.bridge_command(aliases=["punban"])
    async def path_unban(self, ctx:bridge.BridgeContext, *, id=""):
        if ctx.author.id != 666999744572293170:
            return
        bans.remove(id)
        await ctx.respond(f"Unbanned <@{id}> from adding paths")
        dump_save("path_bans", bans)

    @bridge.bridge_command(aliases=["prange"])
    async def paths_range(self, ctx:bridge.BridgeContext, start=0, end=50):
        if end - start > 50 or start > end:
            return
        await ctx.respond("\n".join(paths[start:end]))

    @bridge.bridge_command(aliases=["sx"])
    async def sex(self, ctx:bridge.BridgeContext, *, sub_command: str = ""):
        global s_times
        global s_users
        if botid == 0:
            if random.randint(0, 15) != 0:
                s_times += 1
                await ctx.respond(f"You did the sexed!\n\nSex counter: {s_times}")
            else:
                s_times += 10
                await ctx.respond(
                    f"You did the super sexed!!\n\nSex counter: {s_times}"
                )
            dump_save("stimes", s_times)
            return
        if ctx.author.id not in s_users:
            s_users[ctx.author.id] = {}
        patch_dict(s_template, s_users[ctx.author.id])

        user = s_users[ctx.author.id]
        ####

        s_game = SEX(ctx, user)

        commands = [
            getattr(s_game, attr)
            for attr in dir(s_game)
            if callable(getattr(s_game, attr))
            and hasattr(getattr(s_game, attr), "__code__")
            and "__" not in getattr(s_game, attr).__name__
        ]

        if sub_command == "":
            await s_game.__sex__()
        else:
            sub_command = sub_command.split("|")
            command = getattr(
                s_game,
                correct_spelling(
                    sub_command[0].lower(), [i.__name__ for i in commands]
                ),
            )
            if not command.props["use"](s_game):
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
        s_users[ctx.author.id] = s_game.user

        dump_save("stimes", s_times)
        dump_save("sussy", s_users)
    
    
    @bridge.bridge_command(aliases = ["ap"])
    async def addpasta(self, ctx, name, *, text):
        name = name.lower()
        if name in pastas:
            await ctx.respond(f"Pasta {name} already exists!", ephemeral=True)
            return
        if len(text) >= 1900:
            await ctx.respond(f"Pasta {name} is too long!", ephemeral=True)
            return
        pastas[name] = {
            "author" : ctx.author.id,
            "text" : text,
            "votes" : 0,
            "voters" : [],
        }
        dump_save("pasta", pastas)
        await ctx.respond(f"Saved pasta to {name}")
    
    @bridge.bridge_command(aliases = ["lp"])
    async def listpastas(self, ctx):
        embeds: list[discord.Embed] = []
        for index, pasta_page in enumerate(group_by_n(sorted(pastas, key=lambda x: pastas[x]["votes"], reverse=True), 10)):
            embeds.append(discord.Embed(title = f"Available Pastas"))
            for pasta in pasta_page:
                embeds[-1].add_field(name = pasta, value = f"Votes: {pastas[pasta]['votes']} | Author: <@{pastas[pasta]['author']}>", inline=False)
        paginator = pages.Paginator(pages=embeds, loop_pages=True)
        await paginator.respond(ctx)
    
    @bridge.bridge_command(aliases = ["up"])
    @option_decorator("name", autocomplete=autocomplete_pastas)
    async def upvotepasta(self, ctx, name):
        name = name.lower()
        if name not in pastas:
            await ctx.respond(f"{name} does not exist!", ephemeral=True)
            return
        if ctx.author.id in pastas[name]["voters"]:
            await ctx.respond(f"You've already voted on {name}!", ephemeral=True)
            return
        pastas[name]["votes"] += 1
        pastas[name]["voters"].append(ctx.author.id)
        dump_save("pasta", pastas)
        await ctx.respond(f"Upvoted {name}!")
    
    @bridge.bridge_command(aliases = ["dp"])
    @option_decorator("name", autocomplete=autocomplete_pastas)
    async def downvotepasta(self, ctx, name):
        name = name.lower()
        if name not in pastas:
            await ctx.respond(f"{name} does not exist!", ephemeral=True)
            return
        if ctx.author.id in pastas[name]["voters"]:
            await ctx.respond(f"You've already voted on {name}!", ephemeral=True)
            return
        pastas[name]["votes"] -= 1
        pastas[name]["voters"].append(ctx.author.id)
        if pastas[name]["votes"] < -10 or ctx.author.id == pastas[name]["author"]:
            pastas.pop(name)
        dump_save("pasta", pastas)
        await ctx.respond(f"Downvoted {name}!")
    
    @bridge.bridge_command(aliases = ["delp"])
    @option_decorator("name", autocomplete=autocomplete_pastas)
    async def deletepasta(self, ctx, name):
        name = name.lower()
        if ctx.author.id != 666999744572293170:
            await ctx.respond("Only the bot owner can do that!", ephemeral=True)
            return
        if name not in pastas:
            await ctx.respond(f"{name} does not exist!", ephemeral=True)
            return
        pastas.pop(name)
        dump_save("pasta", pastas)
        await ctx.respond(f"Deleted {name}!")
    
    @bridge.bridge_command(aliases = ["copypasta", "copy", "pst"])
    @option_decorator("name", autocomplete=autocomplete_pastas)
    async def pasta(self, ctx, *, name:str):
        name = name.lower()
        if name not in pastas:
            await ctx.respond(f"{name} does not exist!", ephemeral=True)
            return
        await ctx.respond(pastas[name]["text"])

    @bridge.bridge_command(aliases = ["rp"])
    @option_decorator("name", autocomplete=autocomplete_pastas)
    async def randompasta(self, ctx):
        name = random.choice(list(pastas))
        await ctx.respond(f'Pasta "{name}" with {pastas[name]["votes"]} votes:\n' + pastas[name]["text"])
    

def setup(client):
    client.add_cog(PathTrade(client))
