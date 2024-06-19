from audioop import add
from distutils.log import info
from importlib.metadata import requires
from itertools import chain
from multiprocessing.connection import wait
import re
from turtle import update
import unicodedata
import discord
from discord import message
from discord.client import Client
from discord.ext import commands, bridge
from numpy import ceil
import random
import asyncio
import math
from num2words import num2words
import shelve
from decimal import Decimal
from better_profanity import profanity
import time
import string
import openai

import subprocess
import shutil
import os

active = {}

floor = math.floor
# file_to_rem = shutil.rmtree(r'C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs\Pu-Items')
# file_to_rem.unlink()
# subprocess.run(r"git -C cogs\Pu-Items pull https://github.com/Cheesy-Brik/Pu-Items.git", shell=True, check=True)

envs = {
    "def": {
        "prompt": "You're an outcome suggester for Elemental 3 clone by carykh. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. It can be abstract, but should make sense. For odd elements, provide a unique, sensible reply. Incorporate each distinct element into the outcome. Do not add anything besides the element name, no ending period. Your output should not include numbers, unless their are numbers in the combo, otherwise it's lazy. There is no maximum character limit or maximum complexity. If you cannot provide an outcome just reply with \"loop\".",
        "start": ["fire", "water", "air", "earth"],
        "desc": "",
        "params": {"temperature": 1.5, "presence_penalty": 0.25, "top_p": 0.4},
    },
    "realistic": {
        "prompt": "You're an outcome suggester for Elemental 3 derivative by carykh. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. The result should be completely realistic, as if you actually tried to combine these things in real life. The result should exist in real life. Feel free to spit out \"nothing\" as a result if that's what should happen. Do not add anything besides the element name, no ending period.",
        "start": ["dirt", "lake", "wind", "sticks", "energy"],
        "desc": "More realistic combos",
        "params": {"temperature": 0},
    },
    "states of matter": {
        "prompt": "You're an outcome suggester for Elemental 3 clone by carykh. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. It can be abstract, but should make a little sense. For odd elements, provide a unique, sensible reply. Being unique is better than bland. Do not add anything besides the element name, no ending period.",
        "start": ["solid", "liquid", "gas", "plasma"],
        "desc": "Start with just the states of matter",
        "params": {"temperature": 1},
    },
    "alternate": {
        "prompt": "You're an outcome suggester for Elemental 3 clone by carykh. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. It can be abstract, but should make sense. For odd elements, provide a unique, sensible reply. Incorporate each distinct element into the outcome. If you think the outcome should have multiple results, separate each result with a |. Please have at least 2 results.",
        "start": ["void", "light", "space", "energy", "fire", "water", "air", "earth"],
        "desc": "Combos have multiple results and alternate starting elements",
        "params": {"temperature": 0.5, "presence_penalty": 0.5},
    },
    "really cool": {
        "prompt": "You're an outcome suggester for an Elemental 3 by carykh mock. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. It can be abstract, but should make sense. For odd elements, provide a unique, sensible reply. Incorporate each distinct element into the outcome. Try to make the result funny and incorporate phrases like 'cool', 'awesome', 'really cool', 'sweet', and 'really fucking cool' frequently. Every element MUST have one these phrases incorporated somehow or just \"bro speak\" like results.",
        "start": [
            "really cool fire",
            "really cool water",
            "really cool air",
            "really cool earth",
        ],
        "desc": "All the elements are really cool",
        "params": {"temperature": 1.5, "logit_bias": {"3608": 50, "27485": 50}},
    },
    "random": {
        "prompt": "You're an outcome suggester for Elemental 3 clone by carykh. Users will share elements, and you'll propose a fitting result. The answer should be only the element, without added context. It can be abstract, but should make sense. For odd elements, provide a unique, sensible reply. Incorporate each distinct element into the outcome. Do not add anything besides the element name, no ending period.",
        "start": ["potato", "tacocat", "microwave", "chonkers"],
        "desc": "So random XD lulz POTATO L M A O",
        "params": {"temperature": 1.8, "presence_penalty": 1, "frequency_penalty": 1},
    },
}


async def grab_elem(*elems, env):
    if env not in combos:
        combos[env] = {}
    if tuple(sorted(elems)) in combos[env]:
        return combos[env][tuple(sorted(elems))]
    system_message = {
        "role": "system",
        "content": envs[env]["prompt"],
    }
    user_message = {"role": "user", "content": "+".join(elems)}
    try:
        result = await openai.ChatCompletion.acreate(
            model="gpt-4-turbo-preview",
            messages=[system_message, user_message],
            timeout=5,
            max_tokens=100,
            **envs[env]["params"],
        )
    except:
        result = await openai.ChatCompletion.acreate(
            model="gpt-4-turbo-preview",
            messages=[system_message, user_message],
            timeout=5,
            max_tokens=100,
            **envs[env]["params"],
        )
    result = result["choices"][0]["message"]["content"]
    result = result.replace(",", "").replace("+", "")
    if result[-1] == ".":
        result = result[:-1]
    if env == "alternate":
        result = result.split("|")
    combos[env][tuple(sorted(elems))] = result.lower().strip()
    return result


def get_hint(element, env):
    d = dict(combos[env])
    d = list(d.keys())
    random.shuffle(d)
    for i in d:
        if combos[env][i].lower() == element:
            return (
                f"Here's a hint for {element.title()}:\n{element.title()} = "
                + " + ".join([j.title() for j in i[:-1]])
                + " + "
                + "".join(["?" if j not in ["-", "_", " "] else j for j in i[-1]])
            )
    return f"No hint for the element {element.title()} could be found"


# test.py
import sys
import shutil

# append current python modules' folder path
# example: need to import module.py present in '/path/to/python/module/not/in/syspath'
sys.path.append(
    r"C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs\Pu-Items"
)
sys.path.append(
    r"C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs\wordle"
)

import puitems as p
import wordle as w

global vidchance
vidchance = 6

global M
M = 10000

botid = eval(open(r"cogs\id.txt", "r", encoding="utf8").read())

creature_tokens = eval(
    open(
        r"C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs\crtokens.txt",
        "r",
        encoding="utf8",
    ).read()
)

global puinv
puinv = eval(open(r"cogs\puinv.txt", "r", encoding="utf8").read())
global cyp
cyp = eval(open(r"cogs\cyp.txt", "r", encoding="utf8").read())


global chain_game
try:
    chain_game = eval(open(r"cogs\chain.txt", "r", encoding="utf8").read())
except:
    chain_game = {}


def puinv_check():
    if botid != 764921656199872523:
        return
    File = open("cogs/puinv.txt", "r", encoding="utf8")
    if File != str(puinv):
        Write = open("cogs/puinv.txt", "w", encoding="utf8")
        Write.write(str(puinv))
        File.close()
        Write.close()


def cyp_check():
    if botid != 764921656199872523:
        return
    File = open("cogs/cyp.txt", "r", encoding="utf8")
    if File != str(cyp):
        Write = open("cogs/cyp.txt", "w", encoding="utf8")
        Write.write(str(cyp))
        File.close()
        Write.close()


def chain_check():
    if botid != 764921656199872523:
        return
    File = open("cogs/chain.txt", "r", encoding="utf8")
    if File != str(chain_game):
        Write = open("cogs/chain.txt", "w", encoding="utf8")
        Write.write(str(chain_game))
        File.close()
        Write.close()


def elem_check():
    if botid != 764921656199872523:
        return
    File = open("cogs/elem.txt", "r", encoding="utf8")
    if File != str(elements):
        Write = open("cogs/elem.txt", "w", encoding="utf8")
        Write.write(str(elements))
        File.close()
        Write.close()
    File = open("cogs/combos.txt", "r", encoding="utf8")
    if File != str(combos):
        Write = open("cogs/combos.txt", "w", encoding="utf8")
        Write.write(str(combos))
        File.close()
        Write.close()


global puitems
puitems = p.puitem

elements = eval(open(r"cogs\elem.txt", "r", encoding="utf8").read())
combos = eval(open(r"cogs\combos.txt", "r", encoding="utf8").read())

sacrifices = {
    "white-flower": {"blade of grass": 50, "wilted flower": 50},
    "ant": {"pebble": 90, "queen ant": 10},
    "stick": {
        "bloody stick": 50,
        "thatch": 30,
        "log": 20,
    },
    "rock": {"basalt": 50, "brimstone": 50},
    "blade of grass": {"red grass": 100},
    "leaf": {"night leaf": 60, "stick": 10, "blade of grass": 10, "rock": 10},
    "pebble": {"piece of dirt": 50, "rock": 20, "ant": 20, "ember": 10},
    "acorn": {"squirrel": 90, "squirrel plush": 10},
    "piece of dirt": {"ash": 50, "grain of sand": 50},
    "blue-flower": {"white-flower": 50, "wilted flower": 50},
    "cheese": {"brick": 99, "brik": 1},
    "frog": {"log": 60, "lily pad": 40},
    "bird": {"feather": 50, "beak": 40, "fire feather": 10},
    "red-flower": {"blue-flower": 50, "wilted flower": 50},
    "squirrel": {"fat squirrel": 90, "squirrel plush": 10},
    "McDonald's": {"piece of beef": 100},
    "green-flower": {"red-flower": 50, "wilted flower": 50},
    "fat squirrel": {"very fat squirrel": 90, "squirrel plush": 10},
    "litter": {
        "ash": 70,
        "scrap metal": 5,
        "cardboard": 5,
        "litter": 5,
        "rope": 5,
        "chunk of asphalt": 5,
        "lock of hair": 5,
    },
    "first edition charizard card": {"cardboard": 100},
    "purple-flower": {"green-flower": 50, "wilted flower": 50},
    "bee hive": {"honey": 34, "bee": 33, "honeycomb": 33},
    "wasp hive": {"wasp": 100},
    "horent hive": {"hornet": 100},
    "mud wasp hive": {"mud wasp": 60, "mud": 40},
    "barrel of toxic sludge": {"skull": 60, "vile of acid": 30, "piece of uranium": 10},
    "black-flower": {"purple-flower": 50, "wilted flower": 50},
}

sacrifice_items = set([])
for i in sacrifices:
    sacrifice_items.update(set(list(sacrifices[i].keys())))

# print(sacrifice_items)

base_items = set(list(puitems.keys()) + list(sacrifice_items))
# print(base_items)
# print(len(base_items))

global ranMax
ranMax = 100
global ranNum
ranNum = random.randint(1, ranMax)
print(ranNum)
global bal
bal = eval(open("cogs/bkc.txt", "r", encoding="utf8").read())


def user_check(id):
    try:
        bal["user:" + str(id)]
    except:
        bal["user:" + str(id)] = Decimal(0)


def bal_check():
    File = open("cogs/bkc.txt", "r", encoding="utf8")
    if File != str(bal):
        Write = open("cogs/bkc.txt", "w", encoding="utf8")
        Write.write(str(bal))


def cr_check():
    Write = open(
        r"C:\Users\User\Desktop\Python Programs\Discord Bots\Brik Bot\cogs\crtokens.txt",
        "w",
        encoding="utf8",
    )
    Write.write(str(creature_tokens))
    Write.close()


creature_luck = {}
creature_combos = {}
creature_phone_want = {}
creature_seeds = {}

global raritys
raritys = {  # Use lambda for func stuff :) aka it reruns it every time it's used
    ":eight_spoked_asterisk: **Common** :eight_spoked_asterisk:": {
        "luck": lambda id: random.randint(0, 1),
        "emoji": ":eight_spoked_asterisk:",
        "shorthand": "common",
        "chance": 4000 * M,
        "animals": [
            "pig",
            "cat",
            "dog",
            "frog",
            "bird",
            "mouse",
            "worm",
            "fish",
            "bee",
            "ant",
            "tree",
            "fly",
        ],
        "traits": [
            "is slightly chilly",
            "is pretty normal",
            "can swim",
            "exists",
            "breathes air",
            "can crouch",
            "has eyes",
            "has an extra nose",
            "has a high pitched voice",
            "is a bit small",
            "is very funny",
            "can jump pretty high",
            "has human hands for feet",
        ],
        "ands": 0,
    },
    ":sparkle: **Uncommon** :sparkle:": {
        "luck": lambda id: 0,
        "emoji": ":sparkle:",
        "shorthand": "uncommon",
        "chance": 1500 * M,
        "animals": [
            "starfish",
            "fox",
            "cockroach",
            "praying mantis",
            "rhino",
            "silkworm",
            "wolf",
            "moutain lion",
            "centipede",
            "bear",
            "pack of wolves",
            "murder of crows",
            "crow",
            "horde of mice",
            "frog",
            "bird",
            "bee",
            "cat",
            "dog",
            "moth",
            "hamster",
            "clam",
        ],
        "traits": [
            "can dig very fast",
            "is colorblind",
            "has a scar through one eye",
            "is very adorable",
            "smells funny",
            "has 3 eyes",
            "has 4 eyes",
            "is very big",
            "has a human face",
            "can shoot webs",
            "can talk",
            "is clearly very cool",
            "knows all your secrets",
        ],
        "ands": 0,
    },
    ":atom: **Rare** :atom:": {
        "luck": lambda id: -4,
        "emoji": ":atom:",
        "shorthand": "rare",
        "chance": 400 * M,
        "animals": [
            "gorilla",
            "sea turtle",
            "sponge",
            "squid",
            "giraffe",
            "dove",
            "penguin",
            "sloth",
            "raven",
            "bear",
            "rhino",
            "crow",
            "tiger",
            "squid",
            "polar bear",
            "panda",
            "stork",
            "crane",
            "eagle",
            "alligator",
            "crocodile",
            "spider",
            "wasp",
            "axolotl",
            "snapping turtle",
            "tapir",
            "boar",
        ],
        "traits": [
            "is long",
            "has venomous fangs",
            "is snazzy",
            "has an ice shield",
            "can self destruct",
            "is grilled",
            "is really loving",
            "has wings",
            "has 4 extra legs",
            "has a sword",
            "can run very fast",
            "can stick to surfaces",
            "can change size",
            "is big",
            "is small",
            "has a sonic screech",
            "has gills",
            "is immune to toxins",
            "spits acid",
            "doesn't need food",
            "has 10 eyes",
        ],
        "ands": 1,
    },
    ":six_pointed_star: **Very Rare** :six_pointed_star:": {
        "luck": lambda id: random.choice([-10, -3, -1, 1]),
        "emoji": ":six_pointed_star:",
        "shorthand": "very rare",
        "chance": 100 * M,
        "animals": [
            "octopus",
            "orca",
            "monkey",
            "paper crane",
            "shark",
            "box jellyfish",
            "jackelope",
            "unicorn",
            "slime",
            "goblin",
        ],
        "traits": [
            "has ice breath",
            "has spoon legs",
            "is in love with the letter h",
            "can detonate any bomb",
            "can enter dreams",
            "can sense heat",
            "can shoot lava",
            "can breath fire",
            "is undead",
            "has armor",
            "shoots lasers out of it's eyes",
        ],
        "ands": 2,
    },
    ":radioactive: **Legendary** :radioactive:": {
        "luck": lambda id: -15,
        "emoji": ":radioactive:",
        "shorthand": "legendary",
        "chance": 80 * M,
        "animals": [
            "treant",
            "minotaur",
            "wyvern",
            "dragon",
            "space turtle",
            "giant squid",
            "dune worm",
            "lava snake",
            "cthulhu",
            "golem",
            "rock",
            "stardust dragon",
            "flesh monster in the form of the letter H",
            "cacademon",
        ],
        "traits": [
            "could destroy a universe at the cost of it's life",
            "can travel through time",
            "is from the 4th dimension",
            "can create black holes",
            "can control dreams",
            "can freeze time",
            "is massive",
            "can make clones of itself",
            "can stop time",
            "eats planets",
            "has a gun",
            "has a flame wall",
            "Can shapeshift",
        ],
        "ands": 3,
    },
    "🥚 **Easter Egg** 🥚": {
        "luck": lambda id: 15,
        "emoji": "🥚",
        "shorthand": "easter egg",
        "chance": 20 * M,
        "messages": [
            "The cake is a lie",
            "Put dispenser here",
            "Don't dig straight down",
            "Never mine at night",
            "Stereo Madness",
            "You feel an evil presence watching you...",
            "The wall of flesh had awoken!",
            "Hey listen!",
            "Hya!",
            "Just beats and shapes",
            "Stanley entered the door on his left",
            "The grandmapocalypse",
            "The cookie has been clicked",
            '"Mr. Freeman"',
            "!craft thatch",
            "Cheesy Brik was here",
        ],
    },
}
raritys[":u5408: **Mythical** :u5408:"] = {
    "luck": lambda id: random.randint(-10, 10),
    "emoji": ":u5408:",
    "shorthand": "mythical",
    "chance": 80 * M,
    "animals": [],
    "traits": [],
    "ands": 4,
}
for i in raritys:
    myth = ":u5408: **Mythical** :u5408:"
    try:
        raritys[myth]["animals"] += raritys[i]["animals"]
        raritys[myth]["traits"] += raritys[i]["traits"]
    except:
        pass

raritys[":milky_way: **Godly** :milky_way:"] = {
    "luck": lambda id: 100,
    "emoji": ":milky_way:",
    "shorthand": "godly",
    "chance": 1 * M,
    "animals": ["̇/ꖌ\||ᔑ ⋮ ̇/⚍╎\||𝙹⋮"],
    "traits": ["is godlike"],
    "ands": 0,
}

raritys[":black_small_square: **NULL** :black_small_square:"] = {
    "luck": lambda id: -100000,
    "emoji": ":black_small_square:",
    "shorthand": "null",
    "chance": 1,
    "animals": ["Nothing"],
    "traits": ["Doesn't Exist"],
    "ands": 0,
}

raritys[":dollar: **Money Maker** :dollar:"] = {
    "requires": "':dollar: **Money Maker Tier**' in creature_tokens[ctx.author.id]['bought']",
    "luck": lambda id: 5,
    "emoji": ":dollar:",
    "shorthand": "money maker",
    "chance": 500 * M,
    "animals": [
        "Cash Cow",
        "money chicken",
        "golden goose",
        "lucky duck",
        "fat pig",
        "green sheep",
        "money tree",
    ],
    "traits": [
        "has fat stacks",
        "is generous",
        "makes six figures",
        "is willing to give to charity",
        "has eyes made of coins",
        "grows money",
        "has eyes made of dollar signs",
        'screams "Cha-Ching!" everytime it sees money',
        "is a captialist",
        "got it's money from it's rich daddy",
        "is an entrepreneur",
    ],
    "ands": 2,
}

raritys[":dizzy: **Starlight** :dizzy:"] = {
    "requires": "':dizzy: **Starlight Tier**' in creature_tokens[ctx.author.id]['bought']",
    "luck": lambda id: 15
    if ":full_moon: **Luck in the Stars**" in creature_tokens[id]["bought"]
    else 0,
    "emoji": ":dizzy:",
    "shorthand": "starlight",
    "chance": 450 * M,
    "animals": [
        "space goat",
        "starchild",
        "sun god",
        "moon rabbit",
        "moon man",
        "star dragon",
        "planet eater",
        "wormhole worm",
        "blackhole worm",
        "space creature",
        "moon lord",
        "star lord",
        "mars god",
        "space eye",
        "space foot",
        "space baby",
        "space fox",
        "star fox",
        "star frog",
    ],
    "traits": [
        "can travel through space",
        "can travel light speed",
        "can eat suns",
        "can create planets",
        "can destroy planets",
        "can warp spacetime",
        "can warp gravity",
        "has no mass",
        "has infinite mass",
        "can create matter",
        "can destroy matter",
        "can create anti-matter",
        "can reverse time",
        "can create life",
        "is a creator",
        "is infinite",
        "is unknowable",
    ],
    "ands": 1,
}

raritys[":four_leaf_clover: **Lucky** :four_leaf_clover:"] = {
    "requires": "':four_leaf_clover: **Lucky Tier**' in creature_tokens[ctx.author.id]['bought']",
    "luck": lambda id: 25,
    "emoji": ":four_leaf_clover:",
    "shorthand": "lucky",
    "chance": 120 * M,
    "animals": [
        "lucky duck",
        "bunny",
        "jackrabbit",
        "pig",
        "king",
        "queen",
        "jack",
        "joker",
        "die",
        "pair of fuzzy dice",
        "a sentient stack of poker chips",
    ],
    "traits": [
        "is lucky",
        "can win poker everytime",
        "cheats at blackjack",
        "is a master at poker",
        "gets thrown out of casinos",
        "doesn't need a rabbit's foot",
        "is made of green",
        "has a 5-leaf clover",
        "loves bingo",
        "loves the lottery",
    ],
    "ands": 0,
}

for i in raritys:
    try:
        print(i)
        print(raritys[i]["animals"])
        print(raritys[i]["traits"])
    except:
        pass


def luck(id, amount):
    global creature_luck
    if id not in creature_luck:
        creature_luck[id] = 0
    creature_luck[id] = round(
        creature_luck[id] + amount * (M / 10000)
    )  # Can't get this right smh
    creature_luck[id] = min(creature_luck[id], M * 2)


creature_shop_items = {
    # Shop Items
    ":dollar: **Money Maker Tier**": {
        "desc": "Unlocks a new rarity, the money maker rarity which will give you 10 Creature Tokens every time you get it",
        "requires": "True",
        "cost": 15,
        "type": "tokens",
        "shorthands": ["money maker", "money maker tier", "money"],
    },
    ":game_die: **Gambler**": {
        "desc": "Your luck has a 2x effect, positive and negative",
        "requires": "True",
        "cost": 25,
        "type": "tokens",
        "shorthands": ["gambler", "gamble"],
    },
    ":drop_of_blood: **Drop of Blood**": {
        "desc": "This randomly appears in the shop and can only bought a short time afterwards, does nothing.",
        "requires": "random.randint(0,5) == 0 or (random.randint(0,1) == 0 and len(creature_tokens[ctx.author.id]['bought']) > 5)",
        "cost": 1000,
        "type": "tokens",
        "shorthands": ["blood", "drop of blood", "drop"],
    },
    ":dizzy: **Starlight Tier**": {
        "desc": "Unlocks a new rarity, the starlight rarity",
        "requires": "True",
        "cost": 75,
        "type": "tokens",
        "shorthands": ["starlight", "starlight tier"],
    },
    ":coin: **2 Sided Coin**": {
        "desc": "Everytime you get 1 Creature Token, you now get 2",
        "requires": "':dollar: **Money Maker Tier**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 500,
        "type": "tokens",
        "shorthands": [
            "2 sided coin",
            "two sided coin",
            "sided coin",
            "two",
            "two coin",
        ],
    },
    ":star2: **Star Tokens**": {
        "desc": "Starlight rarities now give you 1 star token each",
        "requires": "':dizzy: **Starlight Tier**' in creature_tokens[ctx.author.id]['bought'] and len(creature_tokens[ctx.author.id]['bought']) > 1",
        "cost": 200,
        "type": "tokens",
        "shorthands": ["star tokens", "star token"],
    },
    ":oil: **Cloning Tube**": {
        "desc": "You now have a chance to get double creatures at once",
        "requires": "len(creature_tokens[ctx.author.id]['bought']) > 6",  # 7 upgrades bought
        "cost": 1000,
        "type": "tokens",
        "shorthands": ["cloning", "cloning tube"],
    },
    ":comet: **Star Drop**": {
        "desc": "Star Tokens now have a chance to drop from any rarity",
        "requires": "':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 10,
        "type": "stars",
        "shorthands": ["star drops", "star drop"],
    },
    ":microbe: **Common Carbon to Gold**": {
        "desc": "Common rarities now have a small chance to give you 100 Creature Tokens",
        "requires": "':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought'] and ':dollar: **Money Maker Tier**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 45,
        "type": "stars",
        "shorthands": [
            "common carbon",
            "carbon to gold",
            "common carbon to gold",
            "common to gold",
            "common gold",
            "carbon gold",
        ],
    },
    ":wrench: **Robotic Replacements**": {
        "desc": "You will now always get double creatrues",
        "requires": "':oil: **Cloning Tube**' in creature_tokens[ctx.author.id]['bought'] and ':microbe: **Common Carbon to Gold**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 5000,
        "type": "tokens",
        "shorthands": [
            "robot replacements",
            "robotic replacements",
            "robots",
            "robotic replacement",
        ],
    },
    ":chart_with_upwards_trend: **Investment Banking**": {
        "desc": "Money Makers now give you 100 Creature Tokens",
        "requires": "':dollar: **Money Maker Tier**' in creature_tokens[ctx.author.id]['bought'] and ':microbe: **Common Carbon to Gold**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1000,
        "type": "tokens",
        "shorthands": ["investment", "investments", "investment banking"],
    },
    ":8ball: **Luck Analyzer**": {
        "desc": "You can now see your luck with !creatureluck",
        "requires": "':game_die: **Gambler**' in creature_tokens[ctx.author.id]['bought'] and ':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 77,
        "type": "stars",
        "shorthands": ["luck analyzer"],
    },
    ":rocket: **Interstellar Mining**": {
        "desc": "Stralight's now give 8 Star Tokens",
        "requires": "':comet: **Star Drop**' in creature_tokens[ctx.author.id]['bought'] and ':chart_with_upwards_trend: **Investment Banking**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 100,
        "type": "stars",
        "shorthands": ["interstellar mining", "interstellar"],
    },
    ":rosette: **Consistency**": {
        "desc": "Every ceature in a combo chain is guaranteed to give a Creature Token",
        "requires": "True",
        "cost": 10,
        "type": "tokens",
        "shorthands": ["consistency"],
    },
    ":four_leaf_clover: **Lucky Tier**": {
        "desc": "Unlocks a new rarity, the lucky rarity, which will give you a luck boost when found",
        "requires": "':game_die: **Gambler**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 50,
        "type": "tokens",
        "shorthands": ["lucky", "lucky tier"],
    },
    ":full_moon: **Luck in the Stars**": {
        "desc": "Starlight's now give you extra luck",
        "requires": "':four_leaf_clover: **Lucky Tier**' in creature_tokens[ctx.author.id]['bought'] and ':8ball: **Luck Analyzer**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 200,
        "type": "stars",
        "shorthands": ["luck in the stars", "luck stars"],
    },
    ":boom: **Combo Tokens**": {
        "desc": "Combos will now give Combo Tokens",
        "requires": "len(creature_tokens[ctx.author.id]['bought']) > 9",
        "cost": 500,
        "type": "stars",
        "shorthands": ["combo tokens", "tokens combo", "combo token"],
    },
    ":credit_card: **Shop Membership**": {
        "desc": "All upgrade prices are reduced by 10%",
        "requires": "len(creature_tokens[ctx.author.id]['bought']) > 14",
        "cost": 100000,
        "type": "tokens",
        "shorthands": ["shop membership", "membership"],
    },
    ":fire: **Extra Combo**": {
        "desc": "The amount of Combo Tokens you get are doubled",
        "requires": "':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1000,
        "type": "combos",
        "shorthands": ["extra combo"],
    },
    ":u5408: **Mythical Combos**": {
        "desc": "Mythical's are now very likely to be in a combo",
        "requires": "':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 10000,
        "type": "combos",
        "shorthands": ["mythical combos", "mythical combo"],
    },
    ":magic_wand: **Stary Magic**": {
        "desc": "Combos are more likely to drop Star Tokens",
        "requires": "':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought'] and ':comet: **Star Drop**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 5000,
        "type": "combos",
        "shorthands": ["stary", "stary magic"],
    },
    ":dvd: **Space Bucks**": {
        "desc": "Money Makers now drop 4 Star Tokens",
        "requires": "':rocket: **Interstellar Mining**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 100,
        "type": "stars",
        "shorthands": ["space bucks"],
    },
    ":star: **2 Sided Star**": {
        "desc": "Everytime you get 1 Star Token, you now get 2",
        "requires": "':coin: **2 Sided Coin**' in creature_tokens[ctx.author.id]['bought'] and ':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 100,
        "type": "stars",
        "shorthands": ["2 sided star", "two sided star", "sided star "],
    },
    ":magnet: **Magnet**": {
        "desc": "Creature Tokens are a bit more likely to drop randomly",
        "requires": "True",
        "cost": 30,
        "type": "tokens",
        "shorthands": ["magnet"],
    },
    ":test_tube: **Common Carbon to Platnium**": {
        "desc": "Common rarities now have a small chance to give you 1000 Creature Tokens",
        "requires": "':microbe: **Common Carbon to Gold**' in creature_tokens[ctx.author.id]['bought'] and ':oil: **Cloning Tube**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 450,
        "type": "stars",
        "shorthands": [
            "carbon to platnium",
            "common carbon to platnium",
            "common to platnium",
            "common platnium",
            "carbon platnium",
        ],
    },
    ":zap: **Starbody Power**": {
        "desc": "Super Rares have a small chance to drop 100 Star Tokens",
        "requires": "':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought'] and ':microbe: **Common Carbon to Gold**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1000,
        "type": "stars",
        "shorthands": ["starbody power"],
    },
    ":trophy: **Extra Winnings**": {
        "desc": "Legendaries will now drop between 10-25 Creature Tokens",
        "requires": "':rosette: **Consistency**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 55,
        "type": "tokens",
        "shorthands": ["extra winnings"],
    },
    ":hole: **Money Hole**": {
        "desc": "Unlocks the !creaturemoneyhole command in which you can put money into the hole to possibly get something out of it",
        "requires": "':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 10000,
        "type": "tokens",
        "shorthands": ["money hole"],
    },
    ":postal_horn: **Golden Combos**": {
        "desc": "For every Combo Token you get you have a chance to get a Creature Token",
        "requires": "':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 2500,
        "type": "combos",
        "shorthands": ["golden combo", "golden combos"],
    },
    ":shinto_shrine: **Mythical Magic**": {
        "desc": "Mythicals now give 5x Combo Tokens",
        "requires": "':u5408: **Mythical Combos**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 35000,
        "type": "combos",
        "shorthands": ["mythical magic"],
    },
    ":anatomical_heart: **Flesh Coin**": {
        "desc": "Unlocks the very rare flesh coin, can drop from anything. Is unnaffected by usual Token boosters",
        "requires": "':drop_of_blood: **Drop of Blood**' in creature_tokens[ctx.author.id]['bought'] and ':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought'] and len(creature_tokens[ctx.author.id]['bought']) > 9",
        "cost": 65000,
        "type": "tokens",
        "shorthands": ["flesh coin", "flesh"],
    },
    ":wilted_rose: **Bloody Rose**": {
        "desc": "Will appear randomly in streaks and grant take or gain between -250 to +500 Creature Tokens, with the larger numbers being much rarer",
        "requires": "':anatomical_heart: **Flesh Coin**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1,
        "type": "flesh",
        "shorthands": ["bloody rose"],
    },
    ":factory: **Firery Industry**": {
        "desc": "Money makers now give 1000 Creature Tokens",
        "requires": "':rocket: **Interstellar Mining**' in creature_tokens[ctx.author.id]['bought'] and ':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1000000,
        "type": "combos",
        "shorthands": ["firery industry", "industry"],
    },
    ":bone: **Hollow Bones**": {
        "desc": "Will appear randomly giving you 2 to the power of your combo Creature Tokens",
        "requires": "':anatomical_heart: **Flesh Coin**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1,
        "type": "flesh",
        "shorthands": ["hollow bones"],
    },
    ":stars: **Star Slam**": {
        "desc": "Now when stars randomly drop they will give between 1 to 10 stars",
        "requires": "':comet: **Star Drop**' in creature_tokens[ctx.author.id]['bought'] and ':zap: **Starbody Power**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 50000,
        "type": "stars",
        "shorthands": ["star slam"],
    },
    ":nazar_amulet: **Cosmic Horrors**": {
        "desc": "Starlights are slightly more likely to drop Flesh Coins",
        "requires": "':anatomical_heart: **Flesh Coin**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 10,
        "type": "flesh",
        "shorthands": ["cosmic horrors"],
    },
}

creature_hole_items = {
    ":taco: **Magic Taco**": {
        "desc": "Will randomly appear and grant 20 stars",
        "requires": "':star2: **Star Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 1000,
        "type": "stars",
        "shorthands": ["magic taco"],
    },
    ":fortune_cookie: **Fortune Cookie**": {
        "desc": "Will randomly appear and grant a boost in luck",
        "requires": "True",
        "cost": 200,
        "type": "tokens",
        "shorthands": ["fortune cookie"],
    },
    ":telephone: **Strange Telephone**": {
        "desc": "Will randomly appear asking for a certain rarity, if this rarity is gotten next it will grant 5% more to your lowest type of token",
        "requires": "True",
        "cost": 100000,
        "type": "tokens",
        "shorthands": ["strange telephone"],
    },
    ":reminder_ribbon: **Golden Ribbon**": {
        "desc": "Will randomly appear and grant 10 Creature Tokens",
        "requires": "True",
        "cost": 100,
        "type": "tokens",
        "shorthands": ["golden ribbon"],
    },
    ":hot_pepper: **Spicy Pepper**": {
        "desc": "Will randomly appear and grant 100 Combo Tokens",
        "requires": "':boom: **Combo Tokens**' in creature_tokens[ctx.author.id]['bought']",
        "cost": 10000,
        "type": "combos",
        "shorthands": ["spicy pepper"],
    },
    ":ear_of_rice: **Cash Crop**": {
        "desc": "Will randomly appear and grant 10 Creature Tokens and is multiplied by your current combo",
        "requires": "True",
        "cost": 1000000,
        "type": "tokens",
        "shorthands": ["spicy pepper"],
    },
    ":boomerang: **Boomerang**": {
        "desc": "When you get 2 creatures of the same rarity in a row, will appear and give you 10 Creature Tokens",
        "requires": "True",
        "cost": 10000,
        "type": "tokens",
        "shorthands": ["boomerang"],
    },
    ":arrow_double_up: **Level Up**": {
        "desc": "When you get a rarity that was rarer than your previous, you get 50 Creature Tokens",
        "requires": "True",
        "cost": 100000,
        "type": "tokens",
        "shorthands": ["level up"],
    },
    ":hourglass: **Waiting Game**": {
        "desc": "For every hour you don't play you gain 600 Creature Tokens your next creature",
        "requires": "True",
        "cost": 10000000,
        "type": "tokens",
        "shorthands": ["waiting game"],
    },
}

print("shop-" + str(len(creature_shop_items)))
print("hole-" + str(len(creature_hole_items)))


def random_seeds(num=1):
    return (
        (
            "".join(
                random.choice(string.ascii_letters + string.digits) for i in range(20)
            )
        )
        for _ in range(num)
    )


def creature_setup(id):
    luck(id, 0)
    global creature_combos

    global creature_seeds
    if id not in creature_seeds:
        creature_seeds[id] = {"seeds": list(random_seeds(8))}
    if id not in creature_combos:
        creature_combos[id] = {
            "combo": 0,
            "creature_type": "",
            "last_creature_type": "",
        }
    global creature_tokens
    if id not in creature_tokens:
        creature_tokens[id] = {"tokens": 0}
    if "bought" not in creature_tokens[id]:
        creature_tokens[id]["bought"] = []
    if "stars" not in creature_tokens[id]:
        creature_tokens[id]["stars"] = 0
    if "combos" not in creature_tokens[id]:
        creature_tokens[id]["combos"] = 0
    if "flesh" not in creature_tokens[id]:
        creature_tokens[id]["flesh"] = 0
    if "last_time" not in creature_tokens[id]:
        creature_tokens[id]["last_time"] = time.time()
    for i in creature_tokens[id]:
        if i != "bought":
            creature_tokens[id][i] = int(creature_tokens[id][i])
    global creature_phone_want
    if id not in creature_phone_want:
        creature_phone_want[id] = {"type": ""}


def achiements_check(id):
    achieve = list(puinv[id]["achievements"].split("-"))
    new = []
    if (
        "fursuit head" in puinv[id]["inv"]
        and "fursuit right arm" in puinv[id]["inv"]
        and "fursuit left arm" in puinv[id]["inv"]
        and "fursuit right leg" in puinv[id]["inv"]
        and "fursuit left leg" in puinv[id]["inv"]
    ):
        if not "You're a furry now!" in achieve:
            new.append("You're a furry now!")
            achieve.append("You're a furry now!")
    if "ted" in puinv[id]["inv"]:
        if not "What" in achieve:
            new.append("What")
            achieve.append("What")
    if "rock" in puinv[id]["inv"]:
        if not "We will __ you" in achieve:
            new.append("We will __ you")
            achieve.append("We will __ you")
    if "squirrel" in puinv[id]["inv"]:
        if not "Nutty" in achieve:
            new.append("Nutty")
            achieve.append("Nutty")
    if "left airpod" in puinv[id]["inv"]:
        if not "Where have you been" in achieve:
            new.append("Where have you been")
            achieve.append("Where have you been")
    if any("golden" in t for t in puinv[id]["inv"]):
        if not "Riches" in achieve:
            new.append("Riches")
            achieve.append("Riches")
    if "someone's dog" in puinv[id]["inv"] and "someone's cat" in puinv[id]["inv"]:
        if not "Pet Thief" in achieve:
            new.append("Pet Thief")
            achieve.append("Pet Thief")
    if (
        "white-flower" in puinv[id]["inv"]
        and "ant" in puinv[id]["inv"]
        and "pebble" in puinv[id]["inv"]
        and "piece of dirt" in puinv[id]["inv"]
        and "blade of grass" in puinv[id]["inv"]
        and "leaf" in puinv[id]["inv"]
    ):
        if not "The little things" in achieve:
            new.append("The little things")
            achieve.append("The little things")
    if "ant" in puinv[id]["inv"]:
        if puinv[id]["inv"]["ant"] >= 100:
            if not "Ant Colony" in achieve:
                new.append("Ant Colony")
                achieve.append("Ant Colony")
    if "rubik’s cube" in puinv[id]["inv"] and "rubik’s clock" in puinv[id]["inv"]:
        if not "Puzzled" in achieve:
            new.append("Puzzled")
            achieve.append("Puzzled")
    reg2 = {}
    reg3 = []
    for i in puinv:
        reg2[i] = sum(puinv[i]["inv"].values())
    reg4 = sorted(list(reg2.values()), reverse=True)
    for i in reg4:
        reg3.append(list(reg2.keys())[list(reg2.values()).index(i)])
    if id in reg3[0:10]:
        if not "Top 10!" in achieve:
            new.append("Top 10!")
            achieve.append("Top 10!")
    puinv[id]["achievements"] = "-".join(achieve)
    return new


def features_check(new):
    features = []
    if "Riches" in new:
        features.append("temple")
    return features


def pureg(id):
    if botid != 764921656199872523:
        return
    try:
        puinv[id]["inv"]
    except:
        try:
            puinv[id]
            puinv[id] = {"inv": puinv[id]}
        except:
            puinv[id] = {"inv": {}}
    try:
        puinv[id]["rewards"]
    except:
        puinv[id]["rewards"] = {}
    try:
        puinv[id]["achievements"]
    except:
        puinv[id]["achievements"] = ""
        # Hey dumbass, yeh you, split string into list then utilize, dipshit
    puinv_check()


def balance():
    for itr in range(0, 1):
        id = 764921656199872523
        pureg(id)
        random.seed()
        global total
        total = 0
        choice = "error"

        extra = ""
        for i in puitems:
            total = total + puitems[i]["chance"]

        def fetch_item():
            add = 0
            A = random.randint(1, total)
            for i in puitems:
                if A <= puitems[i]["chance"] + add:
                    random.seed()
                    if random.randint(1, 100) == 1:
                        if random.randint(1, 100) == 1:
                            choice = f"platinum {i}"
                        else:
                            choice = f"golden {i}"
                    else:
                        choice = i
                    break
                else:
                    add = add + puitems[i]["chance"]
            ach = list(puinv[id]["achievements"].split("-"))
            if "We will __ you" in ach:
                if random.randint(1, 150) == 1:
                    choice = f"old {choice}"
            if "The little things" in ach:
                if random.randint(1, 75) == 1:
                    choice = f"small {choice}"
            if "Riches" in ach:
                if random.randint(1, 50) == 1:
                    choice = f"gilded {choice}"
            return choice

        choice = fetch_item()
        try:
            puinv[id]["inv"][choice] += 1
        except:
            puinv[id]["inv"][choice] = 1

        A = random.randint(1, total)
        if random.randint(1, 5) == 1:
            extra = fetch_item()
            try:
                puinv[id]["inv"][extra] += 1
            except:
                puinv[id]["inv"][extra] = 1

        puinv_check()
        achiements_check(id)
        # print(itr)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        global botid
        botid = self.client.user.id

    @bridge.bridge_command(aliases=["8Ball"])
    async def _8ball(self, ctx, *, question="none"):
        """
        Provides a random response to a user's question.
        Format: !8ball <question>"""
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        await ctx.respond(
            f"\nQuestion: {question}\nAnswer: {random.choice(responses)} "
        )

    @bridge.bridge_command()
    async def joke(self, ctx, *, text="foobar"):
        joke = []
        joke_types = ["knock knock", "normal", "yo mama"]
        random.seed
        chosen_jt = random.choice(joke_types)
        for i in joke_types:
            if text == i:
                chosen_jt = text
        if chosen_jt == "knock knock":
            joke.append("[ERROR] void error: cheesy brik is too lazy to code this")
        elif chosen_jt == "normal":
            joke.append("[ERROR] void error: cheesy brik is too lazy to code this")
        elif chosen_jt == "yo mama":
            yomama = ["so fat", "so old", "so stupid", "so poor", "so ugly"]
            joke.append(f"yo mama {random.choice(yomama)} she ")
            objects = [
                "dog",
                "cat",
                "stadium",
                "cereal bowl",
                "person",
                "lego figure",
                "gold bar",
                "block of cheese",
                "tv",
                "magic portal",
                "big ipad",
                "person's face always",
                "disgusted face",
            ]
            joke.append(
                f"thought a {random.choice(objects)} was a {random.choice(objects)}"
            )
        await ctx.respond("".join(joke))

    @bridge.bridge_command()
    async def ask(self, ctx, *, txt="Input text dumby"):
        """
        Provides a random answer to a user's input text.
        Format: !ask <text>"""
        answers = [
            "Whaaaaat of course not hahaha",
            "Sure bud",
            "Na",
            "Maybe",
            "Perhaps",
            "N O",
            "Yes",
            "100%",
            "Only if you give me $100",
            "Hahaha Funny Question",
            "Yes",
            "No",
            "Nah",
            "Maybe",
            "Yes",
            "No",
            "Nah",
            "Perhaps",
        ]
        random.seed(txt.lower().replace(" ", ""))
        await ctx.respond(random.choice(answers))

    @bridge.bridge_command(aliases=["mynumb", "mn", "menumb"])
    async def mynumber(self, ctx):
        """
        Generates a random number for the user.
        Format: !mynumber"""
        random.seed(ctx.message.author.id)
        await ctx.respond(f"Your number is {random.randint(-1000000,1000000)}!")

    @bridge.bridge_command(aliases=["minimynumb", "mmn", "minmenumb"])
    async def minimynumber(self, ctx):
        """
        Generates a random mini number for the user.
        Format: !minimynumber"""
        random.seed(ctx.message.author.id)
        await ctx.respond(f"Your mini number is {random.randint(0,1000)}!")

    @bridge.bridge_command(aliases=["miniminimynumb", "mmmn", "minminmenumb"])
    async def miniminimynumber(self, ctx):
        """
        Generates a random mini mini number for the user.
        Format: !miniminimynumber"""
        random.seed(ctx.message.author.id)
        await ctx.respond(f"Your mini mini number is {random.randint(0,100)}!")

    @bridge.bridge_command(aliases=["miniminiminimynumb", "mmmmn", "miniminminmenumb"])
    async def miniminiminimynumber(self, ctx):
        """
        miniminiminimynumber
        Generates a random mini mini mini number for the user.
        Format: !miniminiminimynumber"""
        random.seed(ctx.message.author.id)
        await ctx.respond(f"Your mini mini mini number is {random.randint(0,10)}!")

    # -------------------------------------------------------------------------------------------
    @bridge.bridge_command(aliases=["rats", "rets", "ret"])
    async def rat(self, ctx):
        """
        Retrieves a random rat-related content such as images, gifs, or videos.
        Format: !rat"""
        random.seed()
        limit = 12
        results = []
        L = [
            ":rat:",
            "RATS",
            "https://tenor.com/view/lottery-loser-rat-mouse-gif-12761681",
            "https://tenor.com/view/rat-chuha-%E0%A4%9A%E0%A5%82%E0%A4%B9%E0%A4%BE-gif-10942909",
            "https://www.youtube.com/watch?v=0Z-vtNTAzJk",
            "http://www.80stoysale.com/ratlinks.html",
            "https://i.guim.co.uk/img/media/d30cc5927e878f3b26d81c6e456902e0a296ff02/191_607_4087_2453/master/4087.jpg?width=620&quality=85&auto=format&fit=max&s=98ecead973758c9bc93af640aa3417d6",
            "https://cdn.mos.cms.futurecdn.net/7GCPeSkqz3duhcXkg7E6H7-1200-80.jpg",
            "https://www.youtube.com/watch?v=TGpuREoVG-w",
            "https://tenor.com/view/rat-eating-spaghetti-cute-gif-11451413",
            "https://tenor.com/view/rats-fight-gif-8511891",
            "https://www.youtube.com/watch?v=mNy9HIo3shs&t",
            "https://tenor.com/view/rat-jam-gif-19408520",
        ]
        random.seed()

        await ctx.respond(random.choice(L))

    @bridge.bridge_command(aliases=["frogs", "fr", "ribbit"])
    async def frog(self, ctx):
        """
        Retrieves a random frog-related content such as images, gifs, or videos.
        Format: !frog"""
        random.seed()
        limit = 12
        results = []
        L = [
            "𓆏",
            "FROG",
            ":frog:",
            "https://i.kym-cdn.com/photos/images/original/001/867/424/717.gif",
            "https://i.pinimg.com/originals/6e/d5/22/6ed5223751e5b7de55a8ef9708a1af9b.jpg",
            "https://c8.alamy.com/comp/AEB3XG/a-green-tree-frog-hyla-cinerea-snags-a-hawk-moth-for-dinner-with-its-AEB3XG.jpg",
            "https://cdn.discordapp.com/attachments/176667422500061184/558121257246261248/unknown.png",
            "https://cdn.discordapp.com/attachments/399060508147318784/503638152217362443/30c01fe5-cc72-4839-b008-f5ee5292a0d4.jpg",
            "https://cdn.discordapp.com/attachments/529038653234610196/764656298024239104/KIMG4594.JPG",
            "https://tenor.com/view/frog-kick-flip-skateboard-frog-on-da-board-gif-16388983",
            "https://cdn.discordapp.com/attachments/253369826578399232/803301116871442502/RBtRfTF6oX2krOfXQ5aYum7pSxB0wSXMTaC3gGozPD0.webp",
            "https://cdn.discordapp.com/attachments/709434230651748382/745466260279656528/khk4lykk7jh51.png",
        ]
        random.seed()
        await ctx.respond(random.choice(L))

    # -------------------------------------------------------------------------------------------
    @bridge.bridge_command(aliases=["town"])
    async def city(
        self,
        ctx,
        size=8,
        brkdense=5,
        airdense=1,
        windense=0,
        showunclean=False,
        brk=":blue_square:",
        air="<:__:857378778790363149>",
        win=":window:",
    ):
        """
        Generates a city
        With customizable size and density of building blocks, windows, and air spaces.
        Format: !city | size (default: 8) | brkdense (default: 5) | airdense (default: 1) | windense (default: 0) | showunclean (default: False) | brk (default: ':blue_square:') | air (default: '<:__:857378778790363149>') | win (default: ':window:')
        """
        blocks = []

        for i in range(0, brkdense):
            blocks.append(brk)
        for i in range(0, airdense):
            blocks.append(air)
        for i in range(0, windense):
            blocks.append(win)
        reg1 = []
        reg2 = []
        # Generate random grid
        for i in range(0, size):
            for j in range(0, size):
                reg1.append(random.choice(blocks))
            reg2.append(reg1)
            reg1 = []
        if showunclean:
            reg2.reverse()
            for i in reg2:
                reg1.append("".join(i))
            await ctx.respond("\n".join(reg1) + "\n-")
            reg2.reverse()
            reg1 = []

        # Clean grid
        for i, item in enumerate(reg2):
            if i == 0:
                pass
            else:
                for j, item in enumerate(reg2[i]):
                    index1 = i
                    index2 = j
                    if reg2[index1 - 1][index2] != j:
                        if reg2[index1 - 1][index2] == air:
                            reg2[index1][index2] = air

        for j in range(0, size):
            reg1.append(air)
        reg2 = [x for x in reg2 if x != reg1]

        # Render
        reg1 = []
        reg2.reverse()
        for i in reg2:
            reg1.append("".join(i))

        await ctx.respond(str("\n".join(reg1)))

    @bridge.bridge_command(aliases=["all4", "a4"])
    async def always4(self, ctx, num=1):
        """
        Demonstrates the "Always 4" phenomenon
        By taking the length of a number's name and repeating the process until it reaches 4.
        Format: !always4 | num (default: 1)"""
        if len(num) > 10:
            return
            
        numword = num2words(num)
        newnum = len(numword)
        numlist = [str(numword + "\n-------")]
        while newnum != 4:
            numword = num2words(newnum)
            newnum = len(numword)
            numlist.append(str(numword + "\n-------"))
        numword = num2words(newnum)
        newnum = len(numword)
        numlist.append(numword)
        await ctx.respond(
            str(
                "If you take the length of a numbers name, and then take the name of that length and do the same thing it will come back to four ```"
                + "\n".join(numlist)
                + "```"
            )
        )

    @bridge.bridge_command(aliases=["rc", "randchar"])
    async def randomcharacter(self, ctx, amount=1):
        await ctx.respond("This command has been removed due to spam.")
        return
        """
        Generates a specified number of random Unicode characters.
        Format: !randomcharacter | amount (default: 1)"""
        binary = ""
        randchar = []
        try:
            amount + 1
            i = 1
            while i < amount + 1:
                random.seed()
                binary = ""
                for _ in range(1, random.randint(6, 16)):
                    random.seed()
                    binary = binary + str(random.randint(0, 1))
                try:
                    unicodedata.name(chr(int(binary, 2)))
                    randchar.append(chr(int(binary, 2)))
                    i += 1
                except:
                    pass
            if amount > 1:
                await ctx.respond(f'Your random characters are ``{"".join(randchar)}``')
            else:
                await ctx.respond(f'Your random character is {"".join(randchar)}')
        except:
            await ctx.respond(
                "[ERROR] Correct format\n!randomnumber <(number)__optional__ amount of characters>"
            )

    @bridge.bridge_command(aliases=["mychar", "mechar"])
    async def mycharacter(
        self,
        ctx,
    ):
        """
        Generates a unique personal Unicode character based on the user's ID.
        Format: !mycharacter"""
        random.seed(ctx.message.author.id)
        binary = ""
        randchar = []
        multi = 0
        i = 1
        while i < 2:
            binary = ""
            for _ in range(1, random.randint(6, 16)):
                binary = binary + str(random.randint(0, 1))
            try:
                unicodedata.name(chr(int(binary, 2)))
                randchar.append(chr(int(binary, 2)))
                i += 1
            except:
                pass

        await ctx.respond(f'Your personal character is ``{"``, ``".join(randchar)}``')

    @bridge.bridge_command(aliases=[""])
    async def name(self, ctx, *, text=" "):
        """
        Returns the Unicode character names for each character in the provided text.
        Format: !name | text (default: ' ')"""
        charnames = []
        for i in list(text):
            charnames.append(unicodedata.name(i).title())
        await ctx.respond("|".join(charnames))

    @bridge.bridge_command(aliases=["cr"])
    async def creature(
        self,
        ctx,
    ):
        """Gives you a random creature"""
        creature_setup(ctx.author.id)
        rolls = 1
        if ":oil: **Cloning Tube**" in creature_tokens[ctx.author.id]["bought"]:
            if (
                random.randint(0, 1) == 0
                or ":wrench: **Robotic Replacements**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                rolls += 1
        if ctx.author.id == 666999744572293170 and False:
            rolls = 10
        msgs = []
        for roll in range(0, rolls):
            creature_combos[ctx.author.id]["last_creature_type"] = creature_combos[
                ctx.author.id
            ]["creature_type"]
            random.seed(creature_seeds[ctx.author.id]["seeds"][0])
            total = 0
            choice = "error"
            add = 0

            msg = ""

            for i in raritys:
                if "requires" in raritys[i]:  # Check if the tier has the requirements
                    if eval(
                        raritys[i]["requires"]
                    ):  # If false, skip tier and don't add to total
                        total = total + raritys[i]["chance"]
                else:
                    total = total + raritys[i]["chance"]
            A = random.randint(1, total)
            A = min(
                max(
                    A
                    + creature_luck[ctx.author.id]
                    * (
                        int(
                            ":game_die: **Gambler**"
                            in creature_tokens[ctx.author.id]["bought"]
                        )
                        + 1
                    ),
                    0,
                ),
                total,
            )
            for i in raritys:
                if "requires" in raritys[i]:
                    if not eval(
                        raritys[i]["requires"]
                    ):  # Skip tier checking if conditions not met
                        continue
                if A <= raritys[i]["chance"] + add:
                    choice = i
                    break
                else:
                    add = add + raritys[i]["chance"]
            if (
                ":u5408: **Mythical Combos**"
                in creature_tokens[ctx.author.id]["bought"]
                and creature_combos[ctx.author.id]["last_creature_type"] == "mythical"
                and random.randint(0, 4) < 4
            ):
                choice = ":u5408: **Mythical** :u5408:"

            msg += "You got a:"
            if "animals" in raritys[choice] and "traits" in raritys[choice]:
                ranani = random.choice(raritys[choice]["animals"])
                if random.randint(0, 50) != 0:
                    randtrat = random.choice(raritys[choice]["traits"])
                    extra = ""
                    vstart = 0
                    for i in range(0, raritys[choice]["ands"]):
                        if i == raritys[choice]["ands"] - 1:
                            extra += " and " + random.choice(raritys[choice]["traits"])
                        else:
                            extra += ", " + random.choice(raritys[choice]["traits"])
                    if ranani[0] not in ["a", "e", "i", "o", "u"]:
                        msg += f"\n{choice}\n A *{ranani}* that *{randtrat}{extra}* "
                    else:
                        msg += f"\n{choice}\n An *{ranani}* that *{randtrat}{extra}* "
                    creature_combos[ctx.author.id]["creature_type"] = raritys[choice][
                        "shorthand"
                    ]
                else:
                    if ranani[0] not in ["a", "e", "i", "o", "u"]:
                        msg += f"\n❗{raritys[choice]['emoji']}** Anti-{raritys[choice]['shorthand'].title()} **{raritys[choice]['emoji']}❗\n A *{ranani}*"
                    else:
                        msg += f"\n❗{raritys[choice]['emoji']}** Anti-{raritys[choice]['shorthand'].title()} **{raritys[choice]['emoji']}❗\n An *{ranani}*"
                    creature_combos[ctx.author.id]["creature_type"] = (
                        "anti-" + raritys[choice]["shorthand"]
                    )

            elif "messages" in raritys[choice]:
                msg += f'\n{choice}\n*{random.choice(raritys[choice]["messages"])}*'
                creature_combos[ctx.author.id]["creature_type"] = raritys[choice][
                    "shorthand"
                ]

            if (
                creature_combos[ctx.author.id]["last_creature_type"]
                != creature_combos[ctx.author.id]["creature_type"]
            ):
                creature_combos[ctx.author.id]["combo"] = 0
            else:
                creature_combos[ctx.author.id]["combo"] += 1

            if creature_combos[ctx.author.id]["combo"] > 0:
                msg += f"\n:boom: **Combo: {creature_combos[ctx.author.id]['combo']+1}x{'!'*(creature_combos[ctx.author.id]['combo']//2)}**"
                if (
                    creature_combos[ctx.author.id]["combo"] > random.randint(0, 1)
                    or ":rosette: **Consistency**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    if (
                        random.randint(0, 2) == 0
                        or ":rosette: **Consistency**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        creature_tokens[ctx.author.id]["tokens"] += 1
                        if (
                            not ":coin: **2 Sided Coin**"
                            in creature_tokens[ctx.author.id]["bought"]
                        ):
                            msg += f"\n:coin: **You got a** ***Creature Token*** **!**"
                        else:
                            creature_tokens[ctx.author.id]["tokens"] += 1
                            msg += f"\n:coin: **You got 2** ***Creature Tokens*** **!**"
                if (
                    ":boom: **Combo Tokens**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    tokens = (
                        creature_combos[ctx.author.id]["combo"]
                        * (
                            int(
                                ":fire: **Extra Combo**"
                                in creature_tokens[ctx.author.id]["bought"]
                            )
                            + 1
                        )
                        * 5
                        if (
                            ":shinto_shrine: **Mythical Magic**"
                            in creature_tokens[ctx.author.id]["bought"]
                            and choice == ":u5408: **Mythical** :u5408:"
                        )
                        else 1
                    )
                    creature_tokens[ctx.author.id]["combos"] += tokens
                    msg += f"\n:name_badge: **You got {tokens if tokens > 1 else 'a'}** ***Combo Token{'s' if tokens> 1 else ''}*** **!**"
                    if (
                        ":postal_horn: **Golden Combos**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        combo_gold = 0
                        for i in range(tokens):
                            if random.randint(0, 2) == 0:
                                combo_gold += 1
                        creature_tokens[ctx.author.id]["tokens"] += combo_gold
                        if combo_gold:
                            msg += f"\n:postal_horn: **You got {combo_gold if combo_gold > 1 else 'a'}** ***Creature Token{'s' if combo_gold > 1 else ''}*** **!**"

            else:
                if (
                    random.randint(
                        0,
                        3
                        if ":magnet: **Magnet**"
                        in creature_tokens[ctx.author.id]["bought"]
                        else 5,
                    )
                    == 0
                ):
                    creature_tokens[ctx.author.id]["tokens"] += 1
                    if (
                        not ":coin: **2 Sided Coin**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        msg += f"\n:coin: **You got a** ***Creature Token*** **!**"
                    else:
                        creature_tokens[ctx.author.id]["tokens"] += 1
                        msg += f"\n:coin: **You got 2** ***Creature Tokens*** **!**"

            if choice == ":dollar: **Money Maker** :dollar:":
                creature_tokens[ctx.author.id]["tokens"] += 10
                if (
                    ":chart_with_upwards_trend: **Investment Banking**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    creature_tokens[ctx.author.id]["tokens"] += 90
                    if (
                        ":factory: **Firery Industry**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        creature_tokens[ctx.author.id]["tokens"] += 900
                        msg += (
                            f"\n:dollar: **You got 1000** ***Creature Tokens*** **!!**"
                        )
                    else:
                        msg += (
                            f"\n:dollar: **You got 100** ***Creature Tokens*** **!!**"
                        )
                else:
                    msg += f"\n:dollar: **You got 10** ***Creature Tokens*** **!**"

            if (
                choice == ":dizzy: **Starlight** :dizzy:"
                and ":star2: **Star Tokens**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                creature_tokens[ctx.author.id]["stars"] += 1
                if (
                    ":rocket: **Interstellar Mining**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    creature_tokens[ctx.author.id]["stars"] += 7
                    msg += "\n:star: **You got 8** ***Star Tokens*** **!**"
                else:
                    if (
                        ":star: **2 Sided Star**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        msg += "\n:star: **You got 2** ***Star Tokens*** **!**"
                        creature_tokens[ctx.author.id]["stars"] += 1
                    else:
                        msg += "\n:star: **You got a** ***Star Token*** **!**"
            elif (
                random.randint(0, 12) == 0
                and ":comet: **Star Drop**" in creature_tokens[ctx.author.id]["bought"]
            ):
                tokens = random.randint(1, 10)
                if (
                    ":stars: **Star Slam**" in creature_tokens[ctx.author.id]["bought"]
                    and tokens != 1
                ):
                    msg += f"\n:star: **You got {tokens}** ***Star Tokens*** **!**"
                    creature_tokens[ctx.author.id]["stars"] += tokens
                else:
                    if (
                        ":star: **2 Sided Star**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        msg += "\n:star: **You got 2** ***Star Tokens*** **!**"
                        creature_tokens[ctx.author.id]["stars"] += 2
                    else:
                        msg += "\n:star: **You got a** ***Star Token*** **!**"
                        creature_tokens[ctx.author.id]["stars"] += 1
            elif (
                random.randint(0, 5) == 0
                and ":magic_wand: **Stary Magic**"
                in creature_tokens[ctx.author.id]["bought"]
                and creature_combos[ctx.author.id]["combo"] > 0
            ):
                tokens = random.randint(1, 10)
                if (
                    ":stars: **Star Slam**" in creature_tokens[ctx.author.id]["bought"]
                    and tokens != 1
                ):
                    msg += f"\n:star: **You got {tokens}** ***Star Tokens*** **!**"
                    creature_tokens[ctx.author.id]["stars"] += tokens
                else:
                    if (
                        ":star: **2 Sided Star**"
                        in creature_tokens[ctx.author.id]["bought"]
                    ):
                        msg += "\n:star: **You got 2** ***Star Tokens*** **!**"
                        creature_tokens[ctx.author.id]["stars"] += 2
                    else:
                        msg += "\n:star: **You got a** ***Star Token*** **!**"
                        creature_tokens[ctx.author.id]["stars"] += 1

            if (
                choice == ":dollar: **Money Maker** :dollar:"
                and ":dvd: **Space Bucks**" in creature_tokens[ctx.author.id]["bought"]
            ):
                creature_tokens[ctx.author.id]["stars"] += 4
                msg += "\n:dvd: **You got 4** ***Star Tokens*** **!**"

            if (
                choice == ":eight_spoked_asterisk: **Common** :eight_spoked_asterisk:"
                and ":microbe: **Common Carbon to Gold**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 45) == 0
            ):
                creature_tokens[ctx.author.id]["tokens"] += 100
                if (
                    ":test_tube: **Common Carbon to Platnium**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    creature_tokens[ctx.author.id]["tokens"] += 900
                    msg += "\n:trident: **You got 1000** ***Creature Tokens*** **!!**"
                else:
                    msg += "\n:trident: **You got 100** ***Creature Tokens*** **!!**"

            if (
                choice == ":six_pointed_star: **Very Rare** :six_pointed_star:"
                and ":zap: **Starbody Power**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 40) == 0
            ):
                creature_tokens[ctx.author.id]["stars"] += 100
                msg += "\n:zap: **You got 100** ***Star Tokens*** **!!**"

            if (
                choice == ":radioactive: **Legendary** :radioactive:"
                and ":trophy: **Extra Winnings**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                tokens = random.randint(10, 25)
                creature_tokens[ctx.author.id]["tokens"] += tokens
                msg += f"\n:trophy: **You got {tokens}** ***Creature Tokens*** **!**"

            if (
                ":taco: **Magic Taco**" in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 40) == 0
            ):
                creature_tokens[ctx.author.id]["stars"] += 10
                msg += f"\n:taco: **You got 20** ***Star Tokens*** **!**"

            if (
                ":fortune_cookie: **Fortune Cookie**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 15) == 0
            ):
                luck(ctx.author.id, 40)
                msg += f"\n:fortune_cookie: **Your lucky numbers are {random.randint(1,99)}-{random.randint(1,99)}-{random.randint(1,99)}-{random.randint(1,99)}**"

            if creature_phone_want[ctx.author.id]["type"]:
                actual_names = {
                    "tokens": "Creature Tokens",
                    "stars": "Star Tokens",
                    "combos": "Combo Tokens",
                    "flesh": "Flesh Coins",
                }
                if choice == creature_phone_want[ctx.author.id]["type"]:
                    lowest = "tokens"
                    for i in creature_tokens[ctx.author.id]:
                        if i == "flesh":
                            continue  # Not flesh coins
                        if i in actual_names:
                            if (
                                creature_tokens[ctx.author.id][i]
                                < creature_tokens[ctx.author.id][lowest]
                            ):
                                lowest = i
                    token = lowest
                    token_number = floor(creature_tokens[ctx.author.id][token] * 0.05)
                    creature_tokens[ctx.author.id][token] += token_number

                    msg += f"\n:telephone: **You got {token_number}** ***{actual_names[token]}*** **!**"
                creature_phone_want[ctx.author.id]["type"] = ""
            elif (
                ":telephone: **Strange Telephone**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 20) == 0
            ):
                random.seed()
                total = 0
                tele_choice = "error"
                add = 0

                for i in raritys:
                    if (
                        "requires" in raritys[i]
                    ):  # Check if the tier has the requirements
                        if eval(
                            raritys[i]["requires"]
                        ):  # If false, skip tier and don't add to total
                            total = total + raritys[i]["chance"]
                    else:
                        total = total + raritys[i]["chance"]
                A = random.randint(1, total)
                A = min(
                    max(
                        A
                        + creature_luck[ctx.author.id]
                        * (
                            int(
                                ":game_die: **Gambler**"
                                in creature_tokens[ctx.author.id]["bought"]
                            )
                            + 1
                        ),
                        0,
                    ),
                    total,
                )
                for i in raritys:
                    if "requires" in raritys[i]:
                        if not eval(
                            raritys[i]["requires"]
                        ):  # Skip tier checking if conditions not met
                            continue
                    if A <= raritys[i]["chance"] + add:
                        tele_choice = i
                        break
                    else:
                        add = add + raritys[i]["chance"]
                msg += f"\n:telephone: *Hey go get me a* {tele_choice} *will ya?*"
                creature_phone_want[ctx.author.id]["type"] = tele_choice

            if (
                ":reminder_ribbon: **Golden Ribbon**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 8) == 0
            ):
                creature_tokens[ctx.author.id]["tokens"] += 10
                msg += f"\n:reminder_ribbon: **You got 10** ***Creature Tokens*** **!**"

            if (
                ":hot_pepper: **Spicy Pepper**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 50) == 0
            ):
                creature_tokens[ctx.author.id]["combos"] += 100
                msg += f"\n:hot_pepper: **You got 100** ***Combo Tokens*** **!**"

            if (
                ":ear_of_rice: **Cash Crop**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 12) == 0
            ):
                tokens = 10 * (creature_combos[ctx.author.id]["combo"] + 1)
                creature_tokens[ctx.author.id]["tokens"] += tokens
                msg += (
                    f"\n:ear_of_rice: **You got {tokens}** ***Creature Tokens*** **!**"
                )

            if (
                ":boomerang: **Boomerang**" in creature_tokens[ctx.author.id]["bought"]
                and creature_combos[ctx.author.id]["combo"] % 2
            ):
                creature_tokens[ctx.author.id]["tokens"] += 10
                msg += f"\n:boomerang: **You got 10** ***Creature Tokens*** **!**"

            if (
                ":arrow_double_up: **Level Up**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                if creature_combos[ctx.author.id]["last_creature_type"]:
                    for last in raritys:
                        if (
                            creature_combos[ctx.author.id]["last_creature_type"]
                            == raritys[last]["shorthand"]
                        ):
                            break

                    for current in raritys:
                        if (
                            creature_combos[ctx.author.id]["creature_type"]
                            == raritys[current]["shorthand"]
                        ):
                            break

                    if raritys[last]["chance"] > raritys[current]["chance"]:
                        creature_tokens[ctx.author.id]["tokens"] += 50
                        msg += f"\n:arrow_double_up: **You got 50** ***Creature Tokens*** **!**"

            if (
                ":anatomical_heart: **Flesh Coin**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                chance = 750
                if (
                    choice == ":dizzy: **Starlight** :dizzy:"
                    and ":nazar_amulet: **Cosmic Horrors**"
                    in creature_tokens[ctx.author.id]["bought"]
                ):
                    chance -= 50
                if random.randint(0, chance) == 0:
                    creature_tokens[ctx.author.id]["flesh"] += 1
                    msg += f"\n:anatomical_heart: **You got a** ***Flesh Coin*** **!**"

            random.seed(time.time() // 10)
            if (
                ":wilted_rose: **Bloody Rose**"
                in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 12) == 0
            ):
                random.seed()
                tokens = sum([random.randint(-50, 100) for i in range(5)])
                if not tokens:
                    tokens = 1
                creature_tokens[ctx.author.id]["tokens"] += tokens
                msg += f"\n:wilted_rose: **You {'got' if tokens > -1 else 'lost'} {abs(tokens) if abs(tokens) > 1 else 'a'}** ***Creature Token{'s' if not abs(tokens) == 1 else ''}*** **!**"
            random.seed(creature_seeds[ctx.author.id]["seeds"][0])

            if (
                ":bone: **Hollow Bones**" in creature_tokens[ctx.author.id]["bought"]
                and random.randint(0, 25) == 0
            ):
                tokens = 2 ** (creature_combos[ctx.author.id]["combo"] + 1)
                creature_tokens[ctx.author.id]["tokens"] += tokens
                msg += f"\n:bone: **You got {tokens}** ***Creature Tokens*** **!**"

            creature_seeds[ctx.author.id]["seeds"].pop(0)
            creature_seeds[ctx.author.id]["seeds"].append(list(random_seeds())[0])

            if (
                ":hourglass: **Waiting Game**"
                in creature_tokens[ctx.author.id]["bought"]
            ):
                if time.time() - creature_tokens["last_time"] > 3600:
                    tokens = int(
                        600 * ((time.time() - creature_tokens["last_time"]) // 3600)
                    )
                    creature_tokens[ctx.author.id]["tokens"] += tokens
                    msg += f"\n:hourglass: **You got {tokens}** ***Creature Tokens*** **!**"

            creature_tokens["last_time"] = time.time()

            msg += "\n\n Beta test the web remake: <https://cheesybrik.com/rarity-dev>!"
            
            msgs.append(msg)
            
            luck(ctx.author.id, raritys[choice]["luck"](ctx.author.id))
            cr_check()
        await ctx.respond("\n```​```".join(msgs))

    @bridge.bridge_command(
        aliases=[
            "crtokens",
            "crtoken",
            "strtokens",
            "startokens",
            "combotokens",
            "cmbtokens",
        ]
    )
    async def creaturetokens(self, ctx):
        """
        Displays the user's creature tokens, star tokens, combo tokens, and flesh coins, if available.
        Format: !creaturetokens"""
        creature_setup(ctx.author.id)
        """Displays creature tokens"""
        msg = f":coin:***Creature Tokens***: **{creature_tokens[ctx.author.id]['tokens']}**"
        if ":star2: **Star Tokens**" in creature_tokens[ctx.author.id]["bought"]:
            msg += f"\n:star:***Star Tokens***: **{creature_tokens[ctx.author.id]['stars']}**"
        if ":boom: **Combo Tokens**" in creature_tokens[ctx.author.id]["bought"]:
            msg += f"\n:name_badge:***Combo Tokens***: **{creature_tokens[ctx.author.id]['combos']}**"
        if (
            ":anatomical_heart: **Flesh Coin**"
            in creature_tokens[ctx.author.id]["bought"]
        ):
            msg += f"\n:anatomical_heart:***Flesh Coins***: **{creature_tokens[ctx.author.id]['flesh']}**"
        await ctx.respond(msg)

    @bridge.bridge_command(aliases=["crshop"])
    async def creatureshop(self, ctx):
        """
        Displays the creature shop where users can use their creature tokens to purchase items.
        Format: !creatureshop"""
        creature_setup(ctx.author.id)
        shop = []

        emoji_coin_type = {
            "tokens": ":coin:",
            "stars": ":star:",
            "combos": ":name_badge:",
            "flesh": ":anatomical_heart:",
        }

        for i in creature_shop_items:
            random.seed(time.time() // 10)  # Random numbers on a 10 second time window
            if (
                eval(creature_shop_items[i]["requires"])
                and i not in creature_tokens[ctx.author.id]["bought"]
            ):
                shop.append(
                    f"\n{i} - {emoji_coin_type[creature_shop_items[i]['type']]} *{'{:,}'.format(int(ceil(creature_shop_items[i]['cost'] * 0.9 if ':credit_card: **Shop Membership**' in  creature_tokens[ctx.author.id]['bought'] else creature_shop_items[i]['cost'])))}* \n  {creature_shop_items[i]['desc']}"
                )
        num = 1

        if not shop:
            shop = ["*Nothing to buy*"]

        embed = discord.Embed(
            title=f"**Shop** (Page {num})",
            description="\n".join(shop[(-10 + num * 10) : (0 + num * 10)]),
        )
        embed.set_footer(
            text="Wanna help the development of !creature. Take this short form! https://bit.ly/3z0TTU"
        )
        msg = await ctx.respond(embed=embed)
        if True:
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏹")
            while True:

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [
                        "▶",
                        "◀",
                        "⏹",
                    ]

                try:
                    reaction, user = await self.client.wait_for(
                        "reaction_add", timeout=300, check=check
                    )
                except asyncio.TimeoutError:
                    break
                else:
                    if not user == self.client.user:
                        try:
                            await msg.remove_reaction(emoji=reaction.emoji, member=user)
                        except:
                            pass
                        if str(reaction.emoji) == "▶":
                            if num * 10 < len(shop):
                                num += 1
                        elif str(reaction.emoji) == "◀":
                            if num * 10 > 10:
                                num -= 1
                        elif str(reaction.emoji) == "⏹":
                            break
                    embed = discord.Embed(
                        title=f"**Shop** (Page {num})",
                        description="\n".join(shop[(-10 + num * 10) : (0 + num * 10)]),
                    )
                    embed.set_footer(
                        text="Wanna help the development of !creature. Take this short form! https://bit.ly/3z0TTU"
                    )
                    await msg.edit(content="", embed=embed)
            await msg.remove_reaction(emoji="▶", member=self.client.user)
            await msg.remove_reaction(emoji="◀", member=self.client.user)
            await msg.remove_reaction(emoji="⏹", member=self.client.user)

    @bridge.bridge_command(aliases=["crbuy"])
    async def creaturebuy(self, ctx, *, item=""):
        random.seed(time.time() // 10)
        """
Allows users to buy items from the creature shop using their creature tokens.
Format: !creaturebuy <item>
"""
        actual_names = {
            "tokens": "Creature Tokens",
            "stars": "Star Tokens",
            "combos": "Combo Tokens",
            "flesh": "Flesh Coins",
        }
        creature_setup(ctx.author.id)
        item = item.lower()
        for choice in creature_shop_items:
            if item in creature_shop_items[choice]["shorthands"]:
                break
        else:
            await ctx.respond("Not a valid item")
            return
        if not eval(creature_shop_items[choice]["requires"]):
            await ctx.respond("This cannot be bought")
            return
        if choice in creature_tokens[ctx.author.id]["bought"]:
            await ctx.respond("Already bought")
            return
        if (
            ceil(
                creature_shop_items[choice]["cost"] * 0.9
                if ":credit_card: **Shop Membership**"
                in creature_tokens[ctx.author.id]["bought"]
                else creature_shop_items[choice]["cost"]
            )
            > creature_tokens[ctx.author.id][creature_shop_items[choice]["type"]]
        ):
            await ctx.respond(
                f"Not enough {actual_names[creature_shop_items[choice]['type']]}"
            )
            return
        creature_tokens[ctx.author.id]["bought"].append(choice)
        creature_tokens[ctx.author.id][creature_shop_items[choice]["type"]] -= ceil(
            creature_shop_items[choice]["cost"] * 0.9
            if ":credit_card: **Shop Membership**"
            in creature_tokens[ctx.author.id]["bought"]
            else creature_shop_items[choice]["cost"]
        )

        await ctx.respond(f"You bought {choice}!")
        cr_check()

    @bridge.bridge_command(aliases=["crluck"])
    async def creatureluck(self, ctx):
        """Shows your creature luck if you have the luck analyzer upgrade"""
        if ":8ball: **Luck Analyzer**" in creature_tokens[ctx.author.id]["bought"]:
            await ctx.respond(
                f":four_leaf_clover: **Luck**:{creature_luck[ctx.author.id]}"
            )
        else:
            await ctx.respond(f"You need a shop item to use this command")

    @bridge.bridge_command(aliases=["crdev"])
    async def creaturedev(self, ctx, todo):
        if ctx.author.id == 666999744572293170:
            if todo == "allupgrades":
                for i in creature_shop_items:
                    if i not in creature_tokens[ctx.author.id]["bought"]:
                        creature_tokens[ctx.author.id]["bought"].append(i)
            elif "playerstats" in todo:
                todo = todo.split("|")
                todo[1] = int(todo[1])
                creature_setup(todo[1])
                await ctx.respond(
                    str(creature_luck[todo[1]])
                    + str(creature_tokens[todo[1]])
                    + str(creature_combos[todo[1]])
                )
            elif todo == "clear":
                del creature_tokens[ctx.author.id]
                creature_setup(ctx.author.id)
            elif todo == "top":
                x = {}
                for i in creature_tokens:
                    try:
                        x[self.client.get_user(i).name] = creature_tokens[i]["tokens"]
                    except:
                        pass
                y = sorted(list(x.keys()), key=lambda y: x[y], reverse=True)
                await ctx.respond("\n".join([str((i, x[i])) for i in y]))
            elif todo == "test":
                random.seed(creature_seeds[ctx.author.id]["seeds"][0])

                total = 0
                add = 0

                msg = "You will get a:"

                for i in raritys:
                    if (
                        "requires" in raritys[i]
                    ):  # Check if the tier has the requirements
                        if eval(
                            raritys[i]["requires"]
                        ):  # If false, skip tier and don't add to total
                            total = total + raritys[i]["chance"]
                    else:
                        total = total + raritys[i]["chance"]
                A = random.randint(1, total)
                A = min(
                    max(
                        A
                        + creature_luck[ctx.author.id]
                        * (
                            int(
                                ":game_die: **Gambler**"
                                in creature_tokens[ctx.author.id]["bought"]
                            )
                            + 1
                        ),
                        0,
                    ),
                    total,
                )
                for i in raritys:
                    if "requires" in raritys[i]:
                        if not eval(
                            raritys[i]["requires"]
                        ):  # Skip tier checking if conditions not met
                            continue
                    if A <= raritys[i]["chance"] + add:
                        choice = i
                        break
                    else:
                        add = add + raritys[i]["chance"]
                if (
                    ":u5408: **Mythical Combos**"
                    in creature_tokens[ctx.author.id]["bought"]
                    and creature_combos[ctx.author.id]["last_creature_type"]
                    == "mythical"
                    and random.randint(0, 4) < 4
                ):
                    choice = ":u5408: **Mythical** :u5408:"
                if "animals" in raritys[choice] and "traits" in raritys[choice]:
                    ranani = random.choice(raritys[choice]["animals"])
                    if random.randint(0, 50) != 0:
                        randtrat = random.choice(raritys[choice]["traits"])
                        extra = ""
                        vstart = 0
                        for i in range(0, raritys[choice]["ands"]):
                            if i == raritys[choice]["ands"] - 1:
                                extra += " and " + random.choice(
                                    raritys[choice]["traits"]
                                )
                            else:
                                extra += ", " + random.choice(raritys[choice]["traits"])
                        if ranani[0] not in ["a", "e", "i", "o", "u"]:
                            msg += (
                                f"\n{choice}\n A *{ranani}* that *{randtrat}{extra}* "
                            )
                        else:
                            msg += (
                                f"\n{choice}\n An *{ranani}* that *{randtrat}{extra}* "
                            )
                        creature_combos[ctx.author.id]["creature_type"] = raritys[
                            choice
                        ]["shorthand"]
                    else:
                        if ranani[0] not in ["a", "e", "i", "o", "u"]:
                            msg += f"\n❗{raritys[choice]['emoji']}** Anti-{raritys[choice]['shorthand'].title()} **{raritys[choice]['emoji']}❗\n A *{ranani}*"
                        else:
                            msg += f"\n❗{raritys[choice]['emoji']}** Anti-{raritys[choice]['shorthand'].title()} **{raritys[choice]['emoji']}❗\n An *{ranani}*"
                        creature_combos[ctx.author.id]["creature_type"] = (
                            "anti-" + raritys[choice]["shorthand"]
                        )
                await ctx.respond(msg)
            else:
                exec(todo)

    @bridge.bridge_command(aliases=["crbought"])
    async def creaturebought(self, ctx):
        """Displays what you have bought from the creature shop"""
        creature_setup(ctx.author.id)
        shop = []

        for i in sorted(creature_shop_items):
            random.seed(time.time() // 10)  # Random numbers on a 10 second time window
            if i in creature_tokens[ctx.author.id]["bought"]:
                shop.append(f"\n{i} \n  {creature_shop_items[i]['desc']}")
        for i in sorted(creature_hole_items):
            random.seed(time.time() // 10)  # Random numbers on a 10 second time window
            if i in creature_tokens[ctx.author.id]["bought"]:
                shop.append(f"\n{i} \n  {creature_hole_items[i]['desc']}")

        num = 1

        embed = discord.Embed(
            title=f"**Bought** (Page {num})",
            description="\n".join(shop[(-10 + num * 10) : (0 + num * 10)]),
        )
        embed.set_footer(
            text="Wanna help the development of !creature. Take this short form! https://bit.ly/3z0TTU"
        )
        msg = await ctx.respond(embed=embed)
        if True:
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏹")
            while True:

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [
                        "▶",
                        "◀",
                        "⏹",
                    ]

                try:
                    reaction, user = await self.client.wait_for(
                        "reaction_add", timeout=300, check=check
                    )
                except asyncio.TimeoutError:
                    break
                else:
                    if not user == self.client.user:
                        try:
                            await msg.remove_reaction(emoji=reaction.emoji, member=user)
                        except:
                            pass
                        if str(reaction.emoji) == "▶":
                            if num * 10 < len(shop):
                                num += 1
                        elif str(reaction.emoji) == "◀":
                            if num * 10 > 10:
                                num -= 1
                        elif str(reaction.emoji) == "⏹":
                            break
                    embed = discord.Embed(
                        title=f"**Bought** (Page {num})",
                        description="\n".join(shop[(-10 + num * 10) : (0 + num * 10)]),
                    )
                    embed.set_footer(
                        text="Wanna help the development of !creature. Take this short form! https://bit.ly/3z0TTU"
                    )
                    await msg.edit(content="", embed=embed)
            await msg.remove_reaction(emoji="▶", member=self.client.user)
            await msg.remove_reaction(emoji="◀", member=self.client.user)
            await msg.remove_reaction(emoji="⏹", member=self.client.user)

    @bridge.bridge_command(aliases=["crhole", "crmoneyhole"])
    async def creaturemoneyhole(self, ctx, tokens=0):
        """Adds Creature Tokens into the money hole if you have the money hole"""
        hole_raritys = {
            ":taco: **Magic Taco**": 4,
            ":fortune_cookie: **Fortune Cookie**": 0,
            ":telephone: **Strange Telephone**": 10,
            ":reminder_ribbon: **Golden Ribbon**": 1,
            ":hot_pepper: **Spicy Pepper**": 5,
            ":ear_of_rice: **Cash Crop**": 20,
            ":boomerang: **Boomerang**": 3,
            ":arrow_double_up: **Level Up**": 100,
            ":hourglass: **Waiting Game**": 1000,
        }

        if ":hole: **Money Hole**" in creature_tokens[ctx.author.id]["bought"]:
            tokens == int(tokens)
            if tokens < 0:
                await ctx.respond("The amount you want to give must be positive")
                return
            if tokens == 0:
                await ctx.respond(
                    "\nPlease input how many Creature Tokens you would like to put into the Money Hole (Ex: !crhole 10)\n(Note: The more Creature Tokens that are given, the more likely you are to get something)"
                )
                return
            if tokens > creature_tokens[ctx.author.id]["tokens"]:
                await ctx.respond(f"You don't have {tokens} Creature Tokens")
                return
            possible_items = []
            for i in creature_hole_items:
                if i not in creature_tokens[ctx.author.id]["bought"] and eval(
                    creature_hole_items[i]["requires"]
                ):
                    possible_items.append(i)
            if not possible_items:
                await ctx.respond(
                    f'The hole spat out {tokens if tokens > 1 else "a"} Creature Token{"s" if tokens > 1 else ""}'
                )
                return
            for i in range(tokens):
                choice = random.choice(possible_items)
                if random.randint(0, 5000 + (hole_raritys[choice] * 100)) == 0:
                    break
            else:
                await ctx.respond("The hole spat out nothing")
                creature_tokens[ctx.author.id]["tokens"] -= tokens
                return
            creature_tokens[ctx.author.id]["tokens"] -= i + 1
            creature_tokens[ctx.author.id]["bought"].append(choice)
            msg = (
                f"The hole spat out\n{choice}\n*{creature_hole_items[choice]['desc']}*"
            )
            if i + 1 != tokens:
                tokens -= i + 1
                msg += f'\nAnd the hole spat out {tokens if tokens > 1 else "a"} Creature Token{"s" if tokens > 1 else ""}'
            await ctx.respond(msg)
        else:
            await ctx.respond(f"You need a shop item to use this command")
        cr_check()

    @bridge.bridge_command(aliases=["mycr"])
    async def mycreature(
        self,
        ctx,
    ):
        for i in range(0, 1):
            random.seed(ctx.message.author.id)
            total = 0
            choice = "error"
            add = 0

            for i in raritys:
                total = total + raritys[i]["chance"]
            A = random.randint(1, total)

            for i in raritys:
                if A <= raritys[i]["chance"] + add:
                    choice = i
                    break
                else:
                    add = add + raritys[i]["chance"]

            ranani = random.choice(raritys[choice]["animals"])
            randtrat = random.choice(raritys[choice]["traits"])
            extra = ""
            vstart = 0
            for i in range(0, raritys[choice]["ands"]):
                random.seed(ctx.message.author.id + i * i)
                if i == raritys[choice]["ands"] - 1:
                    extra += " and " + random.choice(raritys[choice]["traits"])
                else:
                    extra += ", " + random.choice(raritys[choice]["traits"])
            for i in ["a", "e", "i", "o", "u"]:
                if ranani[0] == i:
                    vstart = 1
            if vstart != 1:
                await ctx.respond(
                    f"Your creature is:\n{choice}\n A *{ranani}* that *{randtrat}{extra}* "
                )
            else:
                await ctx.respond(
                    f"Your creature is:\n{choice}\n An *{ranani}* that *{randtrat}{extra}* "
                )

    @bridge.bridge_command(aliases=["rs", "randscp"])
    async def randomscp(
        self,
        ctx,
    ):
        """
        Generates and sends a link to a random SCP
        (Secure, Contain, Protect) article from the SCP Foundation website.
        Format: !randomscp"""
        random.seed()
        num = random.randint(0, 5100)
        scp = num
        if num < 100:
            scp = f"0{num}"
            if num < 10:
                scp = f"00{num}"
        await ctx.respond(f"http://www.scpwiki.com/scp-{scp}")

    @bridge.bridge_command(aliases=["mys", "mescp"])
    async def myscp(
        self,
        ctx,
    ):
        """
        Generates and sends a link to a unique SCP
        (Secure, Contain, Protect) article from the SCP Foundation website, based on the user's ID.
        Format: !myscp"""
        random.seed(ctx.message.author.id)
        num = random.randint(0, 5100)
        scp = num
        if num < 100:
            scp = f"0{num}"
            if num < 10:
                scp = f"00{num}"
        await ctx.respond(f"http://www.scpwiki.com/scp-{scp}")

    @bridge.bridge_command(aliases=["rar", "chance"])
    async def rarity(self, ctx, *, text="No Input"):
        decimals = 6
        total = 0
        for i in raritys:
            total = total + raritys[i]["chance"]
        txt = text.lower()
        if text == "No Input":
            await ctx.respond("Put a rairty name after the command")
        else:
            for i in raritys:
                if txt == raritys[i]["shorthand"]:
                    txt = i
                    break
            else:
                if txt in puitems:
                    for i in puitems:
                        total = total + puitems[i]["chance"]
                    await ctx.respond(
                        f'{txt} has a {round(puitems[txt]["chance"] / total * 100, decimals)}% chance of appearing'
                    )
                else:
                    await ctx.respond("Not a valid rarity")
                return
            await ctx.respond(
                f'a {text.lower()} creature has a {round(raritys[txt]["chance"] / total * 100, decimals)}% chance of appearing'
            )

    @bridge.bridge_command(aliases=["pu"])
    async def pickup(
        self,
        ctx,
    ):
        """
        Initiates a pickup event where users can find random items
        With a chance to find an extra item. Items found are added to the user's inventory. Achievements and features can also be unlocked based on the user's progress.
        Format: !pickup"""
        async with ctx.channel.typing():
            pass
        for i in range(0, 1):
            balance()
            id = ctx.author.id
            pureg(id)
            random.seed()
            total = 0
            choice = "error"

            extra = ""
            for i in puitems:
                total = total + puitems[i]["chance"]

            def fetch_item():
                add = 0
                A = random.randint(1, total)
                for i in puitems:
                    if A <= puitems[i]["chance"] + add:
                        random.seed()
                        if random.randint(1, 100) == 1:
                            if random.randint(1, 100) == 1:
                                choice = f"platinum {i}"
                            else:
                                choice = f"golden {i}"
                        else:
                            choice = i
                        break
                    else:
                        add = add + puitems[i]["chance"]
                ach = list(puinv[id]["achievements"].split("-"))
                if "We will __ you" in ach:
                    if random.randint(1, 150) == 1:
                        choice = f"old {choice}"
                if "The little things" in ach:
                    if random.randint(1, 75) == 1:
                        choice = f"small {choice}"
                if "Riches" in ach:
                    if random.randint(1, 50) == 1:
                        choice = f"gilded {choice}"
                return choice

            choice = fetch_item()
            try:
                puinv[id]["inv"][choice] += 1
            except:
                puinv[id]["inv"][choice] = 1

            A = random.randint(1, total)
            if random.randint(1, 5) == 1:
                extra = fetch_item()
                try:
                    puinv[id]["inv"][extra] += 1
                except:
                    puinv[id]["inv"][extra] = 1
            choice_v_start = False
            extra_v_start = False
            if choice[0] in "aeiou":
                choice_v_start = True
            if extra == "":
                if choice_v_start:
                    await ctx.respond(f"You found an {choice}!")
                else:
                    await ctx.respond(f"You found a {choice}!")
            else:
                if extra[0] in "aeiou":
                    extra_v_start = True
                if choice_v_start:
                    if extra_v_start:
                        await ctx.respond(f"You found an {choice} and an {extra}!")
                    else:
                        await ctx.respond(f"You found an {choice} and a {extra}!")
                else:
                    if extra_v_start:
                        await ctx.respond(f"You found a {choice} and an {extra}!")
                    else:
                        await ctx.respond(f"You found a {choice} and a {extra}!")
        puinv_check()

        unlocked = achiements_check(id)
        if unlocked != []:
            for i in unlocked:
                await ctx.respond(f":star2:You got a new achievement!:star2::\n**{i}**")
        unlocked = features_check(unlocked)
        if unlocked != []:
            for i in unlocked:
                await ctx.respond(f":dizzy:You unlocked a command:dizzy::\n**{i}**")

    @bridge.bridge_command(aliases=["puinv"])
    async def pocket(self, ctx, *, txt="all"):
        """
        Displays the user's pocket inventory
        Listing all items collected. Users can view specific items or check another user's inventory by mentioning them. The inventory is displayed in pages, with navigation options for moving between pages.
        Format: !pocket | [item_name] | [@user]"""
        id = ctx.author.id
        pureg(id)
        reg1 = 0
        inv = []
        pageinv = []
        if txt != "all":
            try:
                embed = discord.Embed(
                    title=txt, description=f'{txt}({ puinv[id]["inv"][txt.lower()]})'
                )
                embed.set_author(name=" ")
                embed.set_footer(text=" ")
                await ctx.respond(embed=embed)
                return
            except:
                if ctx.message.mentions != []:
                    id = ctx.message.mentions[0].id
                    try:
                        puinv[id]
                    except:
                        await ctx.respond("That person does not have a pocket")
                        return
                else:
                    await ctx.respond("You don't have any of that item")
                    return
        for i in sorted(
            sorted(list(puinv[id]["inv"].keys())),
            key=lambda item: puinv[id]["inv"][item],
            reverse=True,
        ):
            if puinv[id]["inv"][i] > 0:
                inv.append(f'__**{i}**({ puinv[id]["inv"][i]})__')
                reg1 += 1
            if reg1 == 30:
                pageinv.append("\n".join(inv))
                inv = []
                reg1 = 0
        if reg1 != 30:
            pageinv.append("\n".join(inv))
        embed = discord.Embed(title="Pocket(Page 1)", description=pageinv[0])
        if id == ctx.author.id:
            embed.set_footer(text=ctx.author)
        else:
            embed.set_footer(text=ctx.message.mentions[0])
        msg = await ctx.respond(embed=embed)
        num = 1
        await msg.add_reaction("◀")
        await msg.add_reaction("▶")
        await msg.add_reaction("⏹")
        while True:

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in [
                    "▶",
                    "◀",
                    "⏹",
                ]

            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add", timeout=300, check=check
                )
            except asyncio.TimeoutError:
                break
            else:
                if not user == self.client.user:
                    try:
                        await msg.remove_reaction(emoji=reaction.emoji, member=user)
                    except:
                        pass
                    if str(reaction.emoji) == "▶":
                        if num < len(pageinv):
                            num += 1
                    elif str(reaction.emoji) == "◀":
                        if num > 1:
                            num -= 1
                    elif str(reaction.emoji) == "⏹":
                        break
                embed = discord.Embed(
                    title=f"Pocket(Page {num})", description=pageinv[num - 1]
                )
                if id == ctx.author.id:
                    embed.set_footer(text=ctx.author)
                else:
                    embed.set_footer(text=ctx.message.mentions[0])
                await msg.edit(content="", embed=embed)
        await msg.remove_reaction(emoji="▶", member=self.client.user)
        await msg.remove_reaction(emoji="◀", member=self.client.user)
        await msg.remove_reaction(emoji="⏹", member=self.client.user)
        puinv_check()

    @bridge.bridge_command(aliases=["give"])
    async def putrade(self, ctx, takerat, num1="1", *, txt="1"):
        """
        Initiates a trade between two users
        Where each user offers a specified item and quantity. Users must mention the person they want to trade with and provide the number and name of items being traded. The trade is confirmed by the receiving user by reacting with a ✔️.
        Format: !putrade | @user | num1 | item1 | num2 | item2"""
        id = ctx.author.id
        pureg(id)
        try:
            giverid = ctx.author.id
            takerid = ctx.message.mentions[0].id
            item1 = txt.split(" | ")[0]
            num2 = txt.split(" | ")[1].split(" ")[0]
            item2 = txt.split(" | ")[1].split(" ")[1]
            if puinv[giverid]["inv"][item1] >= int(num1):
                if puinv[takerid]["inv"][item2] >= int(num2):
                    msg = await ctx.respond(
                        f"{takerat} react to this message with ✔️ to confirm the trade"
                    )
                    while True:

                        def check(reaction, user):
                            return user == ctx.message.mentions[0] and str(
                                reaction.emoji
                            ) in ["✔️"]

                        try:
                            reaction, user = await self.client.wait_for(
                                "reaction_add", timeout=60 * 20, check=check
                            )
                        except asyncio.TimeoutError:
                            break
                        else:
                            if not user == self.client.user:
                                try:
                                    await msg.remove_reaction(
                                        emoji=reaction.emoji, member=user
                                    )
                                except:
                                    pass
                                if str(reaction.emoji) == "✔️":
                                    print(1)
                                    puinv[giverid]["inv"][item1] -= int(num1)
                                    print(2)
                                    try:
                                        puinv[takerid]["inv"][item1] += int(num1)
                                        print("3a")
                                    except:
                                        puinv[takerid]["inv"][item1] = int(num1)
                                        print("3b")
                                    puinv[takerid]["inv"][item2] -= int(num2)
                                    print(4)
                                    try:
                                        puinv[giverid]["inv"][item2] += int(num2)
                                        print("4a")
                                    except:
                                        puinv[giverid]["inv"][item2] = int(num2)
                                        print("4b")
                                    await ctx.respond("Trade succesful!")
                                    break
                else:
                    await ctx.respond(
                        "That person can't trade that much or they don't have that item"
                    )
            else:
                await ctx.respond(
                    "You can't trade that much or you don't have that item"
                )
        except:
            await ctx.respond(
                "Proper formatting \"!putrade <@ the person you want to trade with> <number you give> <item you give> | <number they give> <item they give>\"\n(Don't type the <>'s)"
            )
        puinv_check()
        unlocked = achiements_check(id)
        if unlocked != []:
            for i in unlocked:
                await ctx.respond(f":star2:You got a new achievement!:star2::\n**{i}**")
        unlocked = features_check(unlocked)
        if unlocked != []:
            for i in unlocked:
                await ctx.respond(f":dizzy:You unlocked a command:dizzy::\n**{i}**")

    @bridge.bridge_command(aliases=["pulb"])
    async def puleaderboard(self, ctx):
        """
        Displays a leaderboard of the top 10 users
        With the most items in their pockets. The leaderboard is sorted by the total number of items each user has, with the highest number at the top.
        Format: !puleaderboard"""
        id = ctx.author.id
        pureg(id)
        reg1 = 0
        reg2 = {}
        reg3 = []
        lb = []
        for i in puinv:
            if i != 764921656199872523:
                for j in puinv[i]["inv"]:
                    reg1 += puinv[i]["inv"][j]
                reg2[i] = reg1
                reg1 = 0
        reg4 = sorted(list(reg2.values()))
        reg4.reverse()
        for i in reg4:
            reg3.append(list(reg2.keys())[list(reg2.values()).index(i)])
        for i in reg3:
            reg1 += 1
            lb.append(f"{reg1}. **{self.client.get_user(i)}**: *{reg2[i]} items*")
            if reg1 == 10:
                break
        embed = discord.Embed(title="", description="\n".join(lb), color=0xE6C700)
        embed.set_author(name="Top 10 Most Items")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(aliases=["puscr", "pusacrifice"])
    async def temple(self, ctx, *, golden_item):
        """
        Sacrifice golden items for a chance to get 100 items with increased gold and platnium chances
        """
        async with ctx.channel.typing():
            pass
        id = ctx.author.id
        golden_item = golden_item.strip()
        if not "golden" in golden_item:
            golden_item = "golden " + golden_item
        if "Riches" in puinv[id]["achievements"].split("-"):
            if golden_item in puinv[id]["inv"]:
                if puinv[id]["inv"][golden_item] > 0:
                    if random.randint(1, 20) == 1:
                        await ctx.respond(
                            f"sacrifice succesful and bountiful goods incoming"
                        )
                        for i in range(0, 100):
                            id = ctx.author.id
                            pureg(id)
                            random.seed()
                            total = 0
                            choice = "error"
                            extra = ""
                            for i in puitems:
                                total = total + puitems[i]["chance"]

                            def fetch_item():
                                add = 0
                                A = random.randint(1, total)
                                for i in puitems:
                                    if A <= puitems[i]["chance"] + add:
                                        random.seed()
                                        if random.randint(1, 40) == 1:
                                            if random.randint(1, 60) == 1:
                                                choice = f"platinum {i}"
                                            else:
                                                choice = f"golden {i}"
                                        else:
                                            choice = i
                                        break
                                    else:
                                        add = add + puitems[i]["chance"]
                                ach = list(puinv[id]["achievements"].split("-"))
                                if "We will __ you" in ach:
                                    if random.randint(1, 150) == 1:
                                        choice = f"old {choice}"
                                random.seed()
                                if "The little things" in ach:
                                    if random.randint(1, 75) == 1:
                                        choice = f"small {choice}"
                                random.seed()
                                if "Riches" in ach:
                                    if random.randint(1, 50) == 1:
                                        choice = f"gilded {choice}"
                                return choice

                            choice = fetch_item()
                            try:
                                puinv[id]["inv"][choice] += 1
                            except:
                                puinv[id]["inv"][choice] = 1
                            A = random.randint(1, total)
                            if random.randint(1, 5) == 1:
                                extra = fetch_item()
                                try:
                                    puinv[id]["inv"][extra] += 1
                                except:
                                    puinv[id]["inv"][extra] = 1
                            if extra == "":
                                await ctx.respond(f"You found a {choice}!")
                            else:
                                await ctx.respond(
                                    f"You found a {choice} and a {extra}!"
                                )
                        puinv_check()
                        unlocked = achiements_check(id)
                        if unlocked != []:
                            for i in unlocked:
                                await ctx.respond(
                                    f":star2:You got a new achievement!:star2::\n**{i}**"
                                )
                        unlocked = features_check(unlocked)
                        if unlocked != []:
                            for i in unlocked:
                                await ctx.respond(
                                    f":dizzy:You unlocked a command:dizzy::\n**{i}**"
                                )
                    else:
                        await ctx.respond(f"sacrifice failed and golden item lost")
                    puinv[id]["inv"][golden_item] -= 1
                else:
                    await ctx.respond(f"you don't have any of that item")
            else:
                await ctx.respond(f"you don't have any of that item")
        else:
            await ctx.respond(f" you have not unlocked this command yet")

    @bridge.bridge_command(aliases=["achv"])
    async def achievements(self, ctx, *, txt="all"):
        """
        Display the user's achievements or a specific achievement
        Format: !achievements | achievement_name"""
        id = ctx.author.id
        pureg(id)
        reg1 = 0
        inv = []
        pageinv = []
        if txt != "all":
            try:
                embed = discord.Embed(
                    title=txt, description=f'{txt}({ puinv[id]["inv"][txt.lower()]})'
                )
                embed.set_author(name=" ")
                embed.set_footer(text=" ")
                await ctx.respond(embed=embed)
            except:
                await ctx.respond("You don't have that achievment")
        else:
            for i in sorted(puinv[id]["achievements"].split("-"), reverse=True):
                if i != "":
                    inv.append(f":star2:**{i}**")
                    reg1 += 1
                if reg1 == 30:
                    pageinv.append("\n".join(inv))
                    inv = []
                    reg1 = 0
            if reg1 != 30:
                pageinv.append("\n".join(inv))
            embed = discord.Embed(title="Achievments(Page 1)", description=pageinv[0])
            embed.set_author(name=" ")
            embed.set_footer(text=" ")
            msg = await ctx.respond(embed=embed)
            num = 1
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏹")
            while True:

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [
                        "▶",
                        "◀",
                        "⏹",
                    ]

                try:
                    reaction, user = await self.client.wait_for(
                        "reaction_add", timeout=300, check=check
                    )
                except asyncio.TimeoutError:
                    break
                else:
                    if not user == self.client.user:
                        try:
                            await msg.remove_reaction(emoji=reaction.emoji, member=user)
                        except:
                            pass
                        if str(reaction.emoji) == "▶":
                            if num < len(pageinv):
                                num += 1
                        elif str(reaction.emoji) == "◀":
                            if num > 1:
                                num -= 1
                        elif str(reaction.emoji) == "⏹":
                            break
                    embed = discord.Embed(
                        title=f"Achievments(Page {num})", description=pageinv[num - 1]
                    )
                    embed.set_author(name=" ")
                    embed.set_footer(text=" ")
                    await msg.edit(content="", embed=embed)
            await msg.remove_reaction(emoji="▶", member=self.client.user)
            await msg.remove_reaction(emoji="◀", member=self.client.user)
            await msg.remove_reaction(emoji="⏹", member=self.client.user)
        puinv_check()

    @bridge.bridge_command()
    async def localpuvalue(self, ctx, *, item):
        """
        Calculate the percentage of a specific item in all users' inventories
        Format: !localpuvalue | item_name"""
        total = Decimal(0)
        for i in puinv:
            total += Decimal(sum(puinv[i]["inv"].values()))
        item_total = Decimal(0)
        for i in puinv:
            try:
                item_total += Decimal(puinv[i]["inv"][item])
            except KeyError:
                pass
            except:
                raise
        if item_total == Decimal(0):
            await ctx.respond(f"{item} is not found in anyones inventory")
        else:
            await ctx.respond(
                f"{item} is {(item_total/total) * Decimal(100)}% of every item owned by everyone"
            )

    @bridge.bridge_command()
    async def puregister(self, ctx):
        """
        Registers the user in the bot's database to track their inventory and achievements
        Format: !puregister"""
        id = ctx.author.id
        pureg(id)

    @bridge.bridge_command()
    async def minesweeper(self, ctx, rows=8, cols=10, bombs=15, hidden=True):
        """
        Starts a game of Minesweeper
        With a customizable grid size, number of bombs, and whether or not the grid is hidden.
        Format: !minesweeper | rows | cols | bombs | hidden"""
        arr = []
        for i in range(rows):
            arr.append(["0"] * cols)
        for i in range(min(bombs, rows * cols)):
            while True:
                bombx, bomby = (
                    random.randint(0, rows - 1),
                    random.randint(0, cols - 1),
                )
                if arr[bombx][bomby] != ":bomb:":
                    arr[bombx][bomby] = ":bomb:"
                    break
        for x in range(rows):
            for y in range(cols):
                if arr[x][y] != ":bomb:":
                    reg = 0
                    for i in range(3):
                        for j in range(3):
                            try:
                                if not x + (i - 1) < 0 and not y + (j - 1) < 0:
                                    if arr[x + (i - 1)][y + (j - 1)] == ":bomb:":
                                        reg += 1
                            except IndexError:
                                pass
                    if reg == 0:
                        arr[x][y] = ":blue_square:"
                    else:
                        arr[x][y] = f":{num2words(reg)}:"
        disreg = []
        if hidden == True:
            for i in arr:
                disreg.append(f"||{'||||'.join(i)}||")
            await ctx.respond("\n".join(disreg))
        else:
            for i in arr:
                disreg.append(f"{''.join(i)}")
            await ctx.respond("\n".join(disreg))

    @bridge.bridge_command(
        aliases=[
            "chooseyourownadventur",
            "cyoa",
            "cya",
        ]
    )
    async def choose_your_own_adventure(self, ctx):
        """
        Starts a community-driven choose your own adventure game
        Where players can add new paths and outcomes to the story.
        Format: !community_choose_your_own_adventure"""
        cyp_check()
        await ctx.respond(
            f"{list(cyp.keys())[0]}\nWhat do you do?\n(For the bot to respond but an @ at the start of the message ex: @Stand up"
        )
        current_node = cyp[list(cyp.keys())[0]]
        pastnodes = [list(cyp.keys())[0]]
        waiting_for_new_beat = False
        new_action = ""
        while True:

            def check(message):
                return message.author.id == ctx.author.id

            try:
                message = await self.client.wait_for(
                    "message", timeout=120.0, check=check
                )
            except asyncio.TimeoutError:
                break
            else:
                if message.content[0] == "@":
                    current_node = f"cyp"
                    for i in pastnodes:
                        current_node += f'["{i}"]'
                    if waiting_for_new_beat == False:
                        current_node = eval(current_node)
                        try:
                            reply = (
                                str(message.content[1:])
                                .lower()
                                .strip()
                                .replace(" ", "")
                                .replace("\n", "")
                            )
                            current_node[reply]
                            await message.reply(
                                f"You {message.content[1:]} and\n{list(current_node[reply].keys())[0]}\nWhat do you do?",
                                allowed_mentions=discord.AllowedMentions(roles=False),
                            )
                            pastnodes.append(reply)
                            pastnodes.append(list(current_node[reply].keys())[0])
                        except KeyError:
                            new_action = reply
                            await message.reply(
                                "Nobdody has tried that! What do you think happens?"
                            )
                            waiting_for_new_beat = True
                        except:
                            raise
                    else:
                        if profanity.contains_profanity(str(message.content[1:])):
                            await message.reply(
                                "That contains profanity please try again"
                            )
                        else:
                            await message.reply("It is written")
                            add = (
                                f'{current_node}["{new_action}"] = '
                                + f'[ "{message.content[1:]}" : [] ]'.replace(
                                    "[", "{"
                                ).replace("]", "}")
                            )
                            exec(add)
                            break
        cyp_check()

    @bridge.bridge_command(aliases=["ch"])
    async def chain(self, ctx, *, txt):
        # Inialization
        def new_chain():
            reinforced = 0
            if "reinforced" in chain_game["chain"]["links"]:
                reinforced = chain_game["chain"]["links"]["reinforced"]

            chain_game["chain"] = {
                "seed": time.time(),
                "log": [],
                "links": {"normal": reinforced},
                "contributors": [],
                "last addition": 0,
                "reinforce": 0,
            }

        id = ctx.author.id
        try:
            chain_game["chain"]
        except:
            pass
        chain_game["chain"] = new_chain()
        try:
            chain_game["upgrades"]
        except:
            chain_game["upgrades"] = {}
        try:
            chain_game[id]
        except:
            chain_game[id] = {
                "links": 0,
                "upgrades": "-",
                "luck": 1,
                "streak": 0,
                "total made": 0,
            }
        try:
            chain_game[id]["streak"]
        except:
            chain_game[id]["streak"] = 0
        try:
            chain_game[id]["total made"]
        except:
            chain_game[id]["total made"] = chain_game[id]["links"]

        random.seed(chain_game["chain"]["seed"] + time.time())

        # Functions
        def calc_link(link_type, id):
            length = sum(chain_game["chain"]["links"].values())

            amount = 1
            if has(id, "Community"):
                amount += length * 0.05
            if has(id, "Community II"):
                amount += length * 0.05
            if has(id, "Streak") and chain_game["chain"]["last addition"] == id:
                amount += chain_game[id]["streak"] * 0.2
            if has(id, "Micro link technology"):
                amount *= 2
            if link_type == "normal":
                pass
            elif link_type == "golden":
                amount *= 3
            elif link_type == "reinforced":
                pass
            elif link_type == "long":
                pass
            return round(amount)

        def choose(what):
            if isinstance(what, int):
                return random.randint(0, what / chain_game[id]["luck"])
            else:
                return random.choice(what)

        def upgrade(name, desc, cost, requires):
            chain_game["upgrades"][name] = {
                "cost": cost,
                "desc": desc,
                "requires": requires,
            }

        def has(id, *upgrades):
            # No I would not like to talk about it
            x = True
            for i in upgrades:
                if not f"-{i}-" in chain_game[id]["upgrades"]:
                    x = False
            return x

        def a_u(id):
            for i in chain_game["upgrades"]:
                chain_game[id]["upgrades"] += i + "-"

        # Upgrades
        chain_game["upgrades"] = {}
        upgrade(
            "Community",
            "When you add to the chain you get 5% of the chains length more links (rounded of course)",
            50,
            "True",
        )
        upgrade(
            "Selfish",
            "If you have not added any links to the current chain you get double the amount of links for breaking it",
            50,
            "True",
        )
        upgrade(
            "Streak",
            "The more times you add onto the chain in a row the more links you get",
            75,
            "True",
        )
        upgrade(
            "Chain inspector",
            "When using the !chain chain command it allows you to see more information about the chain",
            500,
            "True",
        )

        upgrade(
            "Community II",
            "When you add to the chain you get 5% of the chains length more links (rounded of course) (stacks with the previous tier of upgrade)",
            250,
            "has(id, 'Community')",
        )
        upgrade(
            "Selfish II",
            "If you have not added any links to the current chain you get 1.5 times the amount of links for breaking it (stacks with the previous tier of upgrade)",
            300,
            "has(id, 'Selfish')",
        )

        upgrade(
            "Reinforce",
            "Gives you access to the !chain reinforce command allowing the chain to have a 25% chance not to break when someone trys to break at the cost of 20 links",
            150,
            "len(chain_game[id]['upgrades'].split('-'))-2 >= 2",
        )
        upgrade(
            "Micro link technology",
            "You get double the amount of links when adding to the chain",
            5000,
            "(chain_game[id]['total made'] >= 5000)",
        )
        upgrade(
            "Strong arm",
            "You get double the amount of links when breaking the chain",
            5000,
            "(chain_game[id]['total made'] >= 5000)",
        )

        upgrade(
            "Long links",
            "You now have the chance to add long links to the chain which add 5 more links to the chain than normal but give you the same amount of links",
            2500,
            '(has(id, "Reinforce", "Community", "Community II") and len(chain_game[id][\'upgrades\'].split(\'-\'))-2 >= 4)',
        )
        # Commands

        cmd = txt.split(" ")[0]
        txt = txt.replace(cmd, "").strip().lower()
        if cmd == "add":
            # initilaztion (mostly checks and empty varibles)
            if chain_game["chain"]["last addition"] != id:
                chain_game[id]["streak"] = 0

            link_type = "normal"

            # calc link type
            choice = []
            if choose(50) == 0:
                choice.append("golden")
            if choose(30) == 0 and has(id, "Reinforce"):
                choice.append("reinforced")
            if choose(30) == 0 and has(id, "Long links"):
                choice.append("long")
            if choice:
                link_type = choose(choice)  # fun with python if statements :)

            # spaghetti code after this point, beware

            # pre calc link code
            chain_link_amount = 1
            if link_type == "long":
                chain_link_amount
            try:
                chain_game["chain"]["links"][link_type] += 1
            except:
                chain_game["chain"]["links"][link_type] = 1

            #
            added = calc_link(link_type, id)
            chain_game[id]["links"] += added
            #

            # post calc link code
            if not id in chain_game["chain"]["contributors"]:
                chain_game["chain"]["contributors"] += [id]
            chain_game["chain"]["last addition"] = id

            chain_game[id]["streak"] += 1

            # send message
            if link_type == "normal":
                await ctx.respond(f"You added a link to the chain got {added} link(s)")
            else:
                await ctx.respond(
                    f"You added a {link_type} link to the chain got {added} link(s)"
                )

        elif cmd == "break":
            length = sum(chain_game["chain"]["links"].values())

            mult = 1

            if has(id, "Selfish") and not id in chain_game["chain"]["contributors"]:
                mult *= 2
            if has(id, "Selfish II") and not id in chain_game["chain"]["contributors"]:
                mult *= 1.5

            if has(id, "Strong arm"):
                mult *= 2

            if chain_game["chain"]["reinforce"] == 0 or choose(3) != 0:
                chain_game[id]["links"] += length * mult
                await ctx.respond(
                    f"You broke the chain and got {round(length * mult)} links"
                )
                new_chain()
            else:
                await ctx.respond(
                    "You tried to break the chain but it was reinforced and didn't break\nThe chain's reinforcement is now broken"
                )
            chain_game["chain"]["reinforce"] = 0

        elif cmd == "buy":
            for i in chain_game["upgrades"]:
                if txt == i.lower():
                    txt = i
                    break
            else:
                await ctx.respond("Not a valid upgrade")
                return
            if eval(chain_game["upgrades"][txt]["requires"]):
                if not has(id, txt):
                    if chain_game["upgrades"][txt]["cost"] <= chain_game[id]["links"]:
                        chain_game[id]["links"] -= chain_game["upgrades"][txt]["cost"]
                        chain_game[id]["upgrades"] += txt + "-"
                        await ctx.respond(f"You bought {txt}")
                    else:
                        await ctx.respond(
                            f'You are {chain_game["upgrades"][txt]["cost"] - chain_game[id]["links"]} links away from buying that upgrade!'
                        )
                else:
                    await ctx.respond("You already own this upgrade!")
            else:
                await ctx.respond(
                    choose(
                        [
                            "How'd you find out about this upgrade?",
                            "You can't buy this upgrade!",
                            "Not a valid upgrade (for you)",
                        ]
                    )
                )

        elif cmd == "shop":
            if txt == "":
                upgrades = []
                for i in chain_game["upgrades"]:
                    if eval(chain_game["upgrades"][i]["requires"]):
                        if not has(id, i):
                            if (
                                chain_game["upgrades"][i]["cost"]
                                <= chain_game[id]["links"]
                            ):
                                upgrades.append(
                                    f'**{i}** : {chain_game["upgrades"][i]["cost"]}'
                                )
                            else:
                                upgrades.append(
                                    f'{i} : {chain_game["upgrades"][i]["cost"]}'
                                )
                embed = discord.Embed(title="", description="\n".join(upgrades))
                embed.set_author(name=f"Shop")
                embed.set_footer(
                    text="Do !chain shop <upgrade name> to get more info on an upgrade\nBold means you can afford that upgrade"
                )
                await ctx.respond(embed=embed)
            else:
                for i in chain_game["upgrades"]:
                    if txt == i.lower():
                        txt = i
                        break
                else:
                    await ctx.respond("Not a valid upgrade")
                    return
                if eval(chain_game["upgrades"][txt]["requires"]):
                    embed = discord.Embed(
                        title="",
                        description=f"{chain_game['upgrades'][txt]['desc']}\nCost: {chain_game['upgrades'][txt]['cost']} links",
                    )
                    embed.set_author(name=txt)
                    if not has(id, txt):
                        if (
                            chain_game["upgrades"][txt]["cost"]
                            <= chain_game[id]["links"]
                        ):
                            embed.set_footer(text="You can afford this")
                        else:
                            embed.set_footer(text="You can't afford this")
                    else:
                        embed.set_footer(text="You own this")
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(
                        choose(
                            [
                                "How'd you find out about this upgrade?",
                                "You can't buy this upgrade!",
                                "Not a valid upgrade (for you)",
                            ]
                        )
                    )

        elif cmd == "chain":
            length = sum(chain_game["chain"]["links"].values())
            info = f"The chain is {length} links long"
            if has(id, "Chain inspector"):
                info = f"""Length: **{length}**
Reinforce Level: **{chain_game['chain']['reinforce'] if chain_game['chain']['reinforce'] != 0 else 'None'}**
Reinforced Links: **{chain_game['chain']['links']['reinforced'] if 'reinforced' in chain_game['chain']['links'] else '0'}**
Last Addition: **{self.client.get_user(chain_game['chain']['last addition'])}**
             
Your Streak on this Chain: **{chain_game[id]['streak'] if chain_game['chain']['last addition'] == id else '0'}**
"""

            embed = discord.Embed(title="", description=info)
            embed.set_author(name="Chain")
            await ctx.respond(embed=embed)

        elif cmd == "inv":
            await ctx.respond(f'You have {chain_game[id]["links"]} links')

        # unlocked stuff .-.
        elif cmd == "reinforce":
            if has(id, "Reinforce"):
                if chain_game["chain"]["reinforce"] < 1:
                    if chain_game[id]["links"] >= 20:
                        chain_game["chain"]["reinforce"] = 1
                        chain_game[id]["links"] -= 20
                        await ctx.respond(
                            "The chain has been reinforced at the cost of 20 links"
                        )
                    else:
                        await ctx.respond(
                            "You don't have enough links to reinforce the chain"
                        )
                else:
                    await ctx.respond("The chain has already been reninforced")
            else:
                await ctx.respond("This command requires the reinforce upgrade")

        # dev shit
        elif cmd == "run":
            if id == 666999744572293170:
                eval(txt.replace(cmd, "").strip())
                for i in [
                    str(chain_game)[i : i + 2000]
                    for i in range(0, len(str(chain_game)), 2000)
                ]:
                    await ctx.respond(i)

        else:
            await ctx.respond("Not a valid command")

        chain_check()

    @bridge.bridge_command(aliases=["w"])
    async def wordle(self, ctx):
        """
        Play a game of Wordle
        A word-guessing game where players have 6 attempts to guess a 5-letter word. The game provides feedback on guessed letters.
        Format: !wordle"""
        solution = random.choice(w.wordle_solutions)
        guesses = 0
        board = []
        used_letters = []
        win = False
        await ctx.respond(
            "This is a discord implementation of wordle using the entire wordle database to sharpen your wordle skills\nsimply type your starting word to get going"
        )
        while True:

            def check(message):
                return message.author.id == ctx.author.id

            try:
                message = await self.client.wait_for(
                    "message", timeout=120.0, check=check
                )
            except asyncio.TimeoutError:
                break
            else:
                message.content = message.content.lower()
                if "wordle" in message.content:
                    return
                if len(message.content) != 5:
                    await message.reply("Not a 5 letter word")
                    continue
                if (
                    not message.content in w.wordle_possible
                    and not message.content in w.wordle_solutions
                ):
                    await message.reply("Not a valid word")
                    continue
                blocks = []
                yellowed = []
                for i in range(len(message.content)):
                    if (
                        solution.count(message.content[i])
                        - yellowed.count(message.content[i])
                        >= 1
                        and message.content[i] == solution[i]
                    ):
                        blocks.append(":green_square:")
                        yellowed.append(message.content[i])
                    elif (
                        solution.count(message.content[i])
                        - yellowed.count(message.content[i])
                        and message.content[i] in solution
                    ):
                        blocks.append(":yellow_square:")
                        yellowed.append(message.content[i])
                    else:
                        blocks.append(":black_square_button:")
                        used_letters.append(message.content[i])
                board.append("".join(blocks))
                x = "\n".join(board)
                y = (
                    str(set(used_letters))
                    .replace("'", "")
                    .replace("{", "")
                    .replace("}", "")
                )
                await message.reply(f"Used letters: {y}\n{x}")
                if message.content == solution:
                    win = True
                    break
                if guesses == 5:
                    break
                guesses += 1
        if win:
            await ctx.respond(
                f"Congrats you guessed the word {solution} in {guesses + 1}/6 guesses!"
            )
        else:
            await ctx.respond(f"Sorry, but the word was {solution}.")
        board = "\n".join(board)
        await ctx.respond(f"Your board \n{board}")

    @bridge.bridge_command(aliases=["rt"])
    async def random_translator(self, ctx, *, text=""):
        """
        Create a random text generator that transforms given text in a random way
        When given the same seed and input will ouput the exact same result
        The generators are built with python code so a seed generates python code similar to that of the text commands such as !bold, !color, and !owoify
        Format: !random_translator <text> | <generator complexity (optional)> | <show generated code(optional)> | <seed (optional)> | <weights>
        """

        def randomchar(blank=False, length=1, exclude=[]):
            l = list(filter(lambda i: not i in exclude, string.ascii_lowercase))
            if not blank:
                return random.choice(l)
            else:
                return random.choice(list(l) + [""])

        text = text.split("|")
        input = text[0]
        if not input:
            input = "Test"
        try:
            seed = text[3]
        except IndexError:
            seed = "".join(
                random.choice(string.ascii_letters + string.digits) for i in range(10)
            )
        random.seed(seed)
        try:
            length = int(text[1])
        except IndexError:
            length = 5
        try:
            show_code = text[2]
        except IndexError:
            show_code = True
        try:
            weights = text[4]
        except:
            weights = [4, 2, 2, 2, 7, 2, 1, 3, 1, 7, 1, 1, 10, 6]

        __RETURN__ = {"output": ""}

        def gencode(statements=3, pre="", iterator=0, persist=[]):
            code = eval(str(persist))
            for i in range(statements):
                code.append("\n")
                code.append(pre)
                # Yeh fuck you oop *dabs*

                def choice1():
                    code.append(f"x+= '{random.choice(randomchar(), )}'")

                def choice2():
                    code.append(f"x=x[:-1]")

                def choice3():
                    code.append(
                        f"""for {string.ascii_uppercase[iterator % 26]} in range({random.randint(1,5)}):{gencode(random.randint(1,5), pre + ' ', iterator+1)}"""
                    )

                def choice4():
                    possible = [
                        f'x[{random.randint(0,10000)} % len(x)] if len(x) > 0 else ""',
                        f"'{randomchar()}'",
                        "{0}".format(
                            random.choice(
                                list(
                                    set(
                                        filter(
                                            lambda i: r' =  "' in i and not i[0] == " ",
                                            "".join(persist).split("\n"),
                                        )
                                    )
                                )
                                + ["x"]
                            ).strip()[0]
                        ),
                    ]
                    if iterator > 0:
                        possible.append(
                            f"string.ascii_lowercase[{string.ascii_uppercase[random.randint(0,iterator-1) if iterator != 1 else 0 % 26]} % 26]"
                        )
                    code.append(
                        f"""if {random.choice(possible)} {random.choice(['==', '!=', '>', '<', '>=', '<='])} {random.choice(possible)}:{gencode(random.randint(1,5), pre + ' ', iterator, code)}"""
                    )

                def choice5():
                    code.append(f'{randomchar(exclude=["x"])} =  "{randomchar()}"')

                def choice6():
                    code.append(
                        "x = {0}".format(
                            random.choice(
                                list(
                                    set(
                                        filter(
                                            lambda i: r' =  "' in i and not i[0] == " ",
                                            "".join(persist).split("\n"),
                                        )
                                    )
                                )
                                + ["x"]
                            ).strip()[0]
                        )
                    )

                def choice7():
                    code.append("pass")

                def choice8():
                    code.append(
                        '{0} += "{1}"'.format(
                            random.choice(
                                list(
                                    set(
                                        filter(
                                            lambda i: r' =  "' in i and not i[0] == " ",
                                            "".join(persist).split("\n"),
                                        )
                                    )
                                )
                                + ["x"]
                            ).strip()[0],
                            randomchar(),
                        )
                    )

                def choice9():
                    choice = random.choice(
                        list(
                            set(
                                filter(
                                    lambda i: r' =  "' in i and not i[0] == " ",
                                    "".join(persist).split("\n"),
                                )
                            )
                        )
                        + ["x"]
                    ).strip()[0]
                    code.append(f"{choice}={choice}[:-1]")

                def choice10():
                    code.append(
                        "x += {0}".format(
                            random.choice(
                                list(
                                    set(
                                        filter(
                                            lambda i: r' =  "' in i and not i[0] == " ",
                                            "".join(persist).split("\n"),
                                        )
                                    )
                                )
                                + ["x"]
                            ).strip()[0]
                        )
                    )

                def choice11():
                    code.append(f"x *= 2")

                def choice12():
                    code.append(
                        "{0} *= 2".format(
                            random.choice(
                                list(
                                    set(
                                        filter(
                                            lambda i: r' =  "' in i and not i[0] == " ",
                                            "".join(persist).split("\n"),
                                        )
                                    )
                                )
                                + ["x"]
                            ).strip()[0]
                        )
                    )

                def choice13():
                    code.append(f'x.replace("{randomchar()}", "{randomchar(True)}")')

                def choice14():
                    code.append(
                        random.choice(
                            list(
                                set(
                                    filter(
                                        lambda i: r' =  "' in i and not i[0] == " ",
                                        "".join(persist).split("\n"),
                                    )
                                )
                            )
                            + ["x"]
                        ).strip()[0]
                        + f'.replace("{randomchar()}", "{randomchar(True)}")'
                    )

                choices = {  # Choice weights
                    choice1: weights[0],
                    choice2: weights[1],
                    choice3: weights[2] if len(pre) < 10 else 0,
                    choice4: weights[3] if len(pre) < 10 else 0,
                    choice5: weights[4],
                    choice6: weights[5],
                    choice7: weights[6],
                    choice8: weights[7],
                    choice9: weights[8],
                    choice10: weights[9],
                    choice11: weights[10],
                    choice12: weights[11],
                    choice13: weights[12],
                    choice14: weights[13],
                }

                def choose():
                    total = sum(list(choices.values()))
                    choice = random.randint(0, total)
                    place = 0
                    for i in choices:
                        if choice <= choices[i] + place:
                            choice = i
                            break
                        place += choices[i]
                    choice()

                choose()

            return "".join(code[len(persist) - 1 :] if persist != [] else code)

        code = f"""x = r\'\'\'{input.lower()}\'\'\'
{gencode(length)}
print(x)"""
        # exec(code)
        if len(seed + "seed:\n\n" + code) > 2000:
            await ctx.respond(f"seed:{seed}\n\n")
            if show_code:
                await ctx.respond(f"```{code[:1900]}```")
        else:
            await ctx.respond(f"seed:{seed}\n\n")
            if show_code:
                await ctx.respond(f"```{code}```")

    @bridge.bridge_command(aliases=["ai_elem"])
    async def single_player_elemental(self, ctx, *, theme="def"):
        if "elemental" not in active:
            active["elemental"] = {}
        if ctx.author.id in active["elemental"]:
            if active["elemental"][ctx.author.id]:
                await ctx.respond(
                    "You already have an elemental game active, !leave that one."
                )
                return
        openai.api_key = <OPEN AI API KEY>
        theme = theme.lower()
        if theme not in envs:
            await ctx.respond(
                f"{theme} is not a valid theme. Valid themes are {', '.join(list(envs.keys()))}"
            )
            active["elemental"][ctx.author.id] = False
            return
        active["elemental"][ctx.author.id] = True
        if ctx.author.id not in elements:
            elements[ctx.author.id] = {}
        if type(elements[ctx.author.id]) is list:
            elements[ctx.author.id] = {"def": elements[ctx.author.id]}
        if theme not in elements[ctx.author.id]:
            elements[ctx.author.id][theme] = list(envs[theme]["start"])
        elem_check()
        if theme == "def":
            await ctx.respond(
                "Welcome to single player elemental, type !leave to leave and !elements <page_num> to see your inventory and type !hint/!shint <element> to get a hint for an element."
            )
        else:
            await ctx.respond(
                f"Welcome to single player elemental, type !leave to leave and !elements <page_num> to see your inventory and type !hint/!shint <element> to get a hint for an element.\nTheme:**{theme.title()}**\nDescription:*{envs[theme]['desc']}*"
            )
        last_result = ""
        while True:

            def check(message):
                return message.author.id == ctx.author.id

            try:
                message = await self.client.wait_for(
                    "message", timeout=120.0, check=check
                )
            except asyncio.TimeoutError:
                break
            else:
                if not message.content:
                    continue
                if message.content.lower() == "!leave":
                    break
                elif message.content.lower()[:9] == "!elements":
                    if len(message.content.lower().split(" ")) > 1:
                        page = int(message.content.lower().split(" ")[1]) - 1
                    else:
                        page = 0
                    if page * 15 > len(elements[ctx.author.id][theme]):
                        await message.reply(
                            "You don't have that many pages of your inv"
                        )
                    await message.reply(
                        f"__Page {page+1}/{len(elements[ctx.author.id][theme])//16+1}__\n| "
                        + "\n| ".join(
                            [
                                i.title()
                                for i in sorted(elements[ctx.author.id][theme])[
                                    page * 15 : page * 15 + 15
                                ]
                            ]
                        )
                    )
                    continue
                elif (
                    message.content.lower()[:5] == "!hint"
                    or message.content.lower()[:6] == "!shint"
                ):
                    # message.reply("Not implemented yet")
                    # continue
                    if len(message.content.lower().split(" ")) > 1:
                        element = message.content.lower()[
                            message.content.lower().find(" ") :
                        ]
                    else:
                        await message.reply("You must put an element in")
                        continue
                    await message.reply(get_hint(element.strip().lower(), theme))
                    continue
                elif message.content[0] == "*":
                    if last_result:
                        try:
                            elems = [last_result] * max(
                                min(int(message.content[1:]), 10), 2
                            )
                        except:
                            await message.reply(
                                f"Couldn't convert '{message.content[1:]}' to int"
                            )
                            break
                    else:
                        await message.reply("Combine something first")
                        continue
                elif message.content[0] == "+":
                    if last_result:
                        elems = [last_result]
                        for i in message.content.lower().split("+")[1:]:
                            for j in i.split(","):
                                elems.append(j.strip())
                        if len(elems) == 1:
                            # await message.reply(
                            #    "You must specify 2 or more elements to combine"
                            # )
                            continue
                        invalid_elems = []
                        for i in elems:
                            if i not in elements[ctx.author.id][theme]:
                                invalid_elems.append(i)
                        if invalid_elems:
                            await message.reply(
                                f"You don't have {','.join(invalid_elems)}"
                            )
                            continue
                    else:
                        await message.reply("Combine something first")
                        continue
                else:
                    elems = []
                    for i in message.content.lower().split("+"):
                        for j in i.split(","):
                            elems.append(j.strip())
                    if len(elems) == 1:
                        # await message.reply(
                        #    "You must specify 2 or more elements to combine"
                        # )
                        continue
                    invalid_elems = []
                    for i in elems:
                        if i not in elements[ctx.author.id][theme]:
                            invalid_elems.append(i)
                    if invalid_elems:
                        await message.reply(f"You don't have {','.join(invalid_elems)}")
                        continue
                async with ctx.channel.typing():
                    pass
                if theme != "alternate":
                    try:
                        result = await grab_elem(*elems, env=theme)
                        result = result.lower()
                    except Exception as e:
                        await message.reply(f"Error: {e}")
                        continue
                    if result not in elements[ctx.author.id][theme]:
                        await message.reply(f"You got **{result.title()}** 🆕")
                        elements[ctx.author.id][theme].append(result)
                        last_result = result
                    else:
                        await message.reply(
                            f"You got **{result.title()}** but you already have it."
                        )
                        last_result = result
                else:
                    try:
                        result = await grab_elem(*elems, env=theme)
                        result = [i.lower().strip() for i in result]
                    except Exception as e:
                        await message.reply(f"Error: {e}")
                        continue
                    for i in result:
                        if i not in elements[ctx.author.id][theme]:
                            await message.reply(f"You got **{i.title()}** 🆕")
                            elements[ctx.author.id][theme].append(i)
                            last_result = i
                        else:
                            await message.reply(
                                f"You got **{i.title()}** but you already have it."
                            )
                            last_result = i
                elem_check()
        active["elemental"][ctx.author.id] = False
        await ctx.respond("You left")

    @bridge.bridge_command(aliases=["ai_elem_complex"])
    async def single_player_elemental_ultimate(self, ctx, *, theme="def"):
        if "elemental_complex" not in active:
            active["elemental_complex"] = {}
        if ctx.author.id in active["elemental_complex"]:
            if active["elemental_complex"][ctx.author.id]:
                await ctx.respond(
                    "You already have an elemental complex ranking active WAIT"
                )
                return
        active["elemental_complex"][ctx.author.id] = True

        complex = {i: 0 for i in envs[theme]["start"]}

        def get_complexity(element, traversed, depth=0):
            if not traversed:
                traversed = []
            if element in traversed:
                return False
            if element in complex:
                return complex[element]
            traversed = list(traversed)
            element = element.lower()
            traversed.append(element)
            element_combos = []
            for key, value in combos[theme].items():
                if value.lower() == element:
                    element_combos.append(key)
            complexities = []
            for combo in element_combos:
                highest = 0
                for i in combo:
                    c = get_complexity(i, traversed, depth + 1)
                    if c == False:
                        continue
                    if c > highest:
                        highest = c
                else:
                    complexities.append(highest)
                    if 0 in complexities:
                        return 1
                continue
            if complexities:
                complex[element] = min(complexities) + 1
                return min(complexities) + 1
            else:
                complex[element] = 1
                return 1

        for key, value in combos[theme].items():
            get_complexity(value.lower(), None)

        out = "Most complex elements by rank:\n"

        for info, rank in zip(
            sorted(complex.items(), key=lambda x: x[1], reverse=True), range(10)
        ):
            out += f"{rank+1}. {info[0].title()} - {info[1]}\n"

        active["elemental_complex"][ctx.author.id] = False

        await ctx.respond(out)

    @bridge.bridge_command(aliases=["level"])
    async def brik_bot_level(self, ctx, id=None):
        if id == None:
            id = ctx.author.id

        id = int(id)

        # @fuckit#To steamroll key errors lol
        def get_xp():
            xp: float = 0.0
            try:
                xp += creature_tokens[id]["tokens"] / 100
                xp += creature_tokens[id]["combos"] / 50
                xp += creature_tokens[id]["stars"] / 10
                xp += creature_tokens[id]["flesh"]
            except KeyError:
                pass

            try:
                for i in puinv[id]["inv"]:
                    xp += float(puinv[id]["inv"][i]) / 5.0
            except KeyError:
                pass

            try:
                for i in elements[id]:
                    xp += len(elements[id][i])
            except KeyError:
                pass
            try:
                story = eval(open(r"cogs\story.txt", "r", encoding="utf8").read())
                for i in story:
                    if id in story[i]["authors"]:
                        xp += 1000
            except KeyError:
                pass

            xp = floor(xp)
            return xp

        def get_next_level_xp(level):
            return int((level + 1) ** (1 / 0.49308)) + 1

        xp = int(get_xp())
        level = int(xp**0.49308)

        squares = floor(
            (xp - get_next_level_xp(level - 1))
            / (get_next_level_xp(level) - get_next_level_xp(level - 1))
            * 10
        )

        await ctx.respond(
            f"You are level a **{level}** Brik!\n{xp}/{get_next_level_xp(level)}xp\n<:long_brik_begin:1117269314068820008>{'<:long_brik_middle:1117269312177188905>' * squares}<:long_brik_end:1117269311514476575>{':black_large_square:'*(10-squares)}"
        )

    @bridge.bridge_command(aliases=["bed"])
    async def brik_eodollar(self, ctx: bridge.BridgeContext, element: int = 0):
        if element == 0:
            await ctx.respond(
                "To use please enable discord developer mode (under advanced settings tab).\nThen do ?<element> then right click and copy the message id and then do !brik_eodollar <message id>"
            )
            return
        try:
            msg: discord.Message = await ctx.fetch_message(element)
        except:
            await ctx.respond("Not a valid message")
            return
        if msg.author.id != 819076922867712031:
            await ctx.respond("Not from <@819076922867712031>")
            return
        if len(msg.embeds) != 1:
            await ctx.respond("Not a valid element info message")
            return
        embed = msg.embeds[0]
        if "Info" not in embed.title:
            await ctx.respond("Not a valid element info message")
            return
        fields = {
            "".join(char for char in i.name if ord(char) < 128).lower().strip(): i
            for i in embed.fields
        }
        print(fields)
        try:
            categories = fields["categories"].value.split(", ")
            cat_count = len(categories)
            if "more..." in categories[-1]:
                cat_count += int(
                    categories[-1].replace(" more...", "").replace("and ", "")
                )
        except:
            cat_count = 1
        tree_size = int(fields["tree size"].value.replace(",", ""))
        used_in = int(fields["used in"].value.replace(",", ""))
        made_with = int(fields["made with"].value.replace(",", ""))
        found_by = int(fields["found by"].value.replace(",", ""))
        value = (
            (tree_size - 1) * math.sqrt(used_in + 1) / (math.log(made_with, 1.5) or 1)
            + (-1 / ((tree_size - 1 + 1) or -1) + 1) * cat_count
        ) * (1 - (-1 / 2 * 1 / (found_by + 1) + 1 / 2))
        value /= 5

        await ctx.respond("${:,.2f}".format(round(value, 2)))


# ----------------
def setup(client):
    client.add_cog(Fun(client))
