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

def size_of_dict(d):
    total_length = 0
    for key, value in d.items():
        total_length += len(key)
        if isinstance(value, dict):
            total_length += size_of_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    total_length += size_of_dict(item)
                else:
                    total_length += len(str(item))
        else:
            total_length += len(str(value))
    return total_length

def cmd(func=None, *, aliases=[]):
    if func is None:
        def wrapper(func):
            _register_cmd(func, aliases)
            return func
        return wrapper
    else:
        _register_cmd(func, aliases)
        return func

def _register_cmd(func, aliases):
    registry = _cmd_registry
    names = [func.__name__, *aliases]
    for name in names:
        registry[name] = func

def build_document_emebed_list(text:str) -> list:
    embeds = []
    for line in text.split("\n"):
        embeds.append(Embed(description=line))
    return embeds

@cmd
async def echo(out, _, user, __, *text:str):
    await out(" ".join(text))

@cmd
async def see(out, vfs, user, _, filepath:str=""):
    path = ""
    if filepath:
        path = filepath
    else:
        path = user["current_dir"]
    dirs = ""
    files = ""
    for name, file in sorted(traverse_by_path(vfs, path)["data"].items()):
        if name.startswith("."):
            continue
        if "rlocked" in file["args"]:
            continue
        if "rprivate" in file["args"]:
            if user["id"] != file["owner"]:
                continue
        if file['type'] != "dir":
            files += f"\n| {name}.{file['type']}"
        else:
            dirs += f"\n> {name}"
            
    await out(dirs + "\n" + files)

@cmd
async def goto(out, vfs, user, _, filepath:str=""):
    if filepath.startswith("main"):
        path = filepath
    else:
        path = user["current_dir"] + ">" + filepath
    file = traverse_by_path(vfs, path)
    if not file:
        await out("Not a valid file or dir")
        return
    if "rlocked" in file["args"]:
        await out("Not a valid file or dir")
        return
    if "rprivate" in file["args"]:
        if user["id"] != file["owner"]:
            await out("Not a valid file or dir")
            return
    user["current_dir"] = path
    await out(f"Moved to {user['current_dir']}")

@cmd
async def back(out, vfs, user, _, amount:int=1):
    print(amount)
    user["current_dir"] = ">".join(user["current_dir"].split(">")[:-amount])
    await out(f"Moved to {user['current_dir']}")

@cmd
async def create(out, vfs, user, _, file_type:str, name:str, filepath=None, *args):
    if filepath:
        path = filepath
    else:
        path = user["current_dir"]
    directory = traverse_by_path(vfs, path)
    if directory["type"] != "dir":
        await out("This file is not a directory")
        return
    if "wlocked" in directory["args"] and user["level"] != "System Admin":
        await out("You cannot write to this directory")
        return
    if "wpublic" not in directory["args"] and user["level"] != "System Admin":
        if directory["owner"] != user["id"]:
            await out("You do not own this directory")
            return
    
    if not args:
        args = []
    
    base_file = {
        "type" : file_type,
        "args" : args,
        "owner" : user["id"],
        "data" : {
            "." : {}
        }
    }
    
    for i in "<>#@":
        if i in name:
            await out(f"{i} not allowed in file names")
            return
    
    if name not in directory["data"]:
        directory["data"][name] = base_file
        await out(f"Created {name}.{file_type}")
    else:
        base_file["args"] = args or directory["data"][name]["args"]
        base_file["owner"] = directory["data"][name]["owner"]
        if "wlocked" not in directory["data"][name]["args"] or user["level"] == "System Admin":
            if user["id"] == directory["data"][name]["owner"] or "wpublic" in directory["data"][name]["args"] or user["level"] == "System Admin":
                directory["data"][name] = base_file
                await out(f"File {name} written over")
            else:
                await out("You cannot write to this file")
                return
        else:
            await out("You cannot write to this file")
            return   

@cmd
async def write(out, vfs, user, msg:discord.Message, filepath:str, text:str=""):
    if filepath.startswith("main"):
        path = filepath
    else:
        path = user["current_dir"] + ">" + filepath
    file = traverse_by_path(vfs, path)
    if "wlocked" not in file["args"] or user["level"] == "System Admin" or user["level"] == "System Admin":
        if user["id"] == file["owner"] or "wpublic" in file["args"] or user["level"] == "System Admin":
            if file["type"] in ["image"] and user["level"] != "System Admin":
                file["data"]["."] = msg.attachments[0].proxy_url
                await out(f"File {filepath} written over")
            else:
                file["data"]["."] = text
                await out(f"File {filepath} written over")
        else:
            await out("You cannot write to this file")
            return
    else:
        await out("You cannot write to this file")
        return

@cmd
async def append(out, vfs, user, _, filepath:str, text:str=""):
    if filepath.startswith("main"):
        path = filepath
    else:
        path = user["current_dir"] + ">" + filepath
    file = traverse_by_path(vfs, path)
    if "wlocked" not in file["args"] or user["level"] == "System Admin" or user["level"] == "System Admin":
        if user["id"] == file["owner"] or "wpublic" in file["args"] or user["level"] == "System Admin":
            if file["type"] in ["image"] and user["level"] != "System Admin":
                await out(f"File type cannot be appended to")
            else:
                file["data"]["."] += "\n" + text
                await out(f"Added to {filepath}")
        else:
            await out("You cannot write to this file")
            return
    else:
        await out("You cannot write to this file")
        return

@cmd
async def read(out, vfs, user, _, filepath:str=""):
    if filepath:
        if filepath.startswith("main"):
            path = filepath
        else:
            path = user["current_dir"] + ">" + filepath
    else:
        path = user["current_dir"]
    
    file = traverse_by_path(vfs, path)
    
    if file["type"] in ["image"]:
        await out("", embed = Embed(image = file["data"]["."]))
    if file["type"] in  ["document"]:
        build_document_emebed_list(file["data"]["."])
    else:
        await out(file["data"]["."])

@cmd
async def info(out, vfs, user, _, filepath:str=""):
    if filepath:
        if filepath.startswith("main"):
            path = filepath
        else:
            path = user["current_dir"] + ">" + filepath
    else:
        path = user["current_dir"]
    
    file = traverse_by_path(vfs, path)
    
    author_obj = vfs['user-data'][file['owner']]
    name = path.split(">")[-1]
    byte = size_of_dict(file["data"])#Close enough?
    file_type = file["type"]
    txt = f"""Name: {name}
File Type: {file_type}
Author: {author_obj['name'] + (f" ({author_obj['level']})" if author_obj['level'] != "User" else "")}
Size: {byte}

"""
    arg_replacements = {
        "wlocked" : "Locked File",
        "rlocked" : "Hidden File",
        "wpublic" : "Public File",
        "rprivate": "Private File"
    }
    if file["args"]:
        txt += "Flags: "
        for i in file["args"]:
            if i in arg_replacements:
                i = arg_replacements[i]
            txt += i + ", "
        txt = txt.removesuffix(", ")
    await out(txt)

@cmd
async def delete(out, vfs, user, _, filepath:str):
    if filepath.startswith("main"):
        path = filepath
    else:
        path = user["current_dir"] + ">" + filepath
    
    file = traverse_by_path(vfs, path)
    parent = traverse_by_path(vfs, path.removesuffix(">" + path.split(">")[-1]))
    if "wlocked" not in file["args"] or user["level"] == "System Admin":
        if user["id"] == file["owner"] or "wpublic" in file["args"] or user["level"] == "System Admin":
            parent["data"].pop(path.split(">")[-1])
            await out(f"Deleted {path.split('>')[-1]}")
        else:
            await out("You cannot delete this file")
            return
    else:
        await out("You cannot delete this file")
        return

vfs_start = {
    "main" : {
        "type" : "dir",
        "args" : ["wlocked"],
        "owner" : "sys",
        "data" : {
            "." : "The main directory for the Brik Wall",
            "help" : {
                "type" : "text",
                "args" : [],
                "owner" : "666999744572293170",
                "data" : {
                    "." : ("""Hello! Welcome the Brik Bot 2000 Virtual Command Line Interface (BB2VCLI)
This is not a real os or file system, it is virtually managed through any user with cmd line operations

Since this is a public space where technically anyone can do anything (that I allow) here are the rules/guidelines:
1. I (Cheesy Brik) reserve the right to restrict, remove, or in someone block access to anything stored on the Brik Wall (Virtual File System)
2. Nothing on the Brik Wall is permanent nor forever, note that other users may manipulate your work or remove it. While I will try to mitigate griefing, it's inevitable that some things will be lost
3. No slurs, hate speech, nsfw, overt suggestive content, overly vulgar material, malicious misinformation, or content that is illegal
4. No personal data, not even of yourself
5. No overt malicious use of bugs/holes. While it's fine to pen test, once a bug is found only poke at it as much as you need to and do not cause large amounts of damage

So now to get started -

use \"see\" to see the current directory you are in and what files there are
use \"goto\" to move to a directory
use \"read\" to read a files contents""")
                }
            },
            "user-documents" : {
                "type" : "dir",
                "args" : ["wpublic"],
                "owner" : "sys",
                "data" : {
                    "." : ("The root directory for all publicly added user documents")
                }
            }
        },
    },
    "user-data" : {
        "type" : "dir",
        "args" : ["wlocked", "rlocked"],
        "data" : {},
        "owner" : "666999744572293170",
        "666999744572293170" : {
            "name" : "Cheesy Brik",
            "current_dir":"main",
            "id" : "666999744572293170",
            "level" : "System Admin",
        },
        "sys" : {
            "name" : "BB2VCLI",
            "current_dir":"",
            "id" : "0",
            "level" : "System",
        },
    }
}

vfs = load_save("brikbotos", vfs_start)

class Cmd(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener("on_message")
    async def cmd(self, message:discord.Message):
        if message.author == self.client.user:
            return
        if not message.content:
            return
        if message.content[0] != ">":
            return
        message_text = message.content[1:]
        if not message_text:
            return
        
        async def say(text, embed = None):
            if len(text) > 1900:
                end_message = f"..."
                text = text[:1900-len(end_message)] + end_message
            await message.reply(f"```{text}```" if text else "", embed=embed)
        
        
        base_user = {
            "name" : message.author.name,
            "current_dir":"main",
            "id" : str(message.author.id),
            "level" : "User",
        }
        
        if str(message.author.id) not in vfs["user-data"]:
            vfs["user-data"][str(message.author.id)] = {}
        
        user_obj = vfs["user-data"][str(message.author.id)]

        user_obj = patch_dict(base_user, user_obj)
        
        if message_text.split(" ")[0] not in _cmd_registry:
            await say(f"{message_text.split(' ')[0]} is not a command, did you mean {correct_spelling(message_text.split(' ')[0], list(_cmd_registry.keys()))}?")
            return
        else:
            args = " ".join(message_text.split(" ")[1:]).split("|")
            if args == ['']:
                args = []
            cmd_func = _cmd_registry[message_text.split(" ")[0]]
            cmd_args = [i.strip().replace("`", "\`") for i in args]
            for cmd_arg_index, new_type in zip(range(len(cmd_args)), list(get_type_hints(cmd_func).values())[4:]):
                cmd_args[cmd_arg_index] = new_type(cmd_args[cmd_arg_index])
            print(cmd_args)
            await cmd_func(say, vfs, user_obj, message, *cmd_args)
            dump_save("brikbotos", vfs)
        
            
                
        

def setup(client):
    client.add_cog(Cmd(client))
