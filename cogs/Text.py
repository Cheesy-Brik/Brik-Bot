from typing import final
import discord
from discord.ext import bridge, commands
import random
import time
import string
import asyncio

import openai


global ghost
ghost = "-/-"

current_chats = {}

rate_limit = {}

botid = eval(open(r"cogs\id.txt", "r", encoding="utf8").read())

def ow_story_check():
    if botid != 764921656199872523:
        return
    File = open("cogs/story.txt", "r", encoding="utf8")
    if File != str(story):
        Write = open("cogs/story.txt", "w", encoding="utf8")
        Write.write(str(story))
        File.close()
        Write.close()

story = eval(open(r"cogs\story.txt", "r", encoding="utf8").read())

def title(word):
    for i in range(len(word)):
        if word[i] in string.ascii_letters:
            word = list(word)
            word[i] = word[i].upper()
            return "".join(word)
    return word

def get_last_word(book):
    if len(story[book]["pages"][-1]) > 1:
        return story[book]["pages"][-1][-1]
    elif len(story[book]["pages"]) > 1:
        return story[book]["pages"][-2][-1]
    else:
        return ""

class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(aliases=["b"])
    async def bold(self, ctx, *, text:str="bold"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        await ctx.respond(f" **{text[:r]}** ")

    @bridge.bridge_command(aliases=["i"])
    async def italics(self, ctx, *, text="italics"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        await ctx.respond(f" *{text[:r]}* ")

    @bridge.bridge_command(aliases=["u"])
    async def underline(self, ctx, *, text="underline"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        await ctx.respond(f" __{text[:r]}__ ")

    @bridge.bridge_command(aliases=["h"])
    async def hide(self, ctx, *, text="hidden"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        await ctx.respond(f" ||{text[:r]}|| ")

    @bridge.bridge_command(aliases=["s"])
    async def strikethrough(self, ctx, *, text="strikethrough"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        await ctx.respond(f" ~~{text[:r]}~~ ")

    @bridge.bridge_command(aliases=["C"])
    async def color(self, ctx, color="white", *, text="color"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))

        if color == "white":
            await ctx.respond(f"```html\n{text[:r]}```")
        elif color == "green":
            await ctx.respond(f"```css\n{text[:r]}```")
        elif color == "red":
            await ctx.respond(f"```diff\n- {text[:r]}```")
        elif color == "cyan":
            await ctx.respond(f"```fix\n= {text[:r]}```")
        elif color == "gray":
            await ctx.respond(f"```bash\n# {text[:r]}```")
        elif color == "blue":
            await ctx.respond(f"```md\n# {text[:r]}```")
        elif color == "orange":
            await ctx.respond(f"```fix\n{text[:r]}```")
        else:
            await ctx.respond("Unidentified Color")

    @bridge.bridge_command(aliases=["sh"])
    async def superhide(self, ctx, *, text="superhidden"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        split = list(text[:r])
        final = "||||".join(split)
        await ctx.respond(f"||{final}||")

    @bridge.bridge_command(aliases=["E"])
    async def embed(self, ctx, *, text="text"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        split = text[:r].split("|")
        if len(split) == 2:
            split.append(" ")
            split.append("000000")
        elif len(split) == 3:
            split.append("000000")
        else:
            pass
        embed = discord.Embed(
            title=" ",
            description=split[1],
            color=eval("0x" + str(split[3].lower().strip())),
        )
        embed.set_author(name=split[0])
        embed.set_footer(text=split[2])
        await ctx.respond(embed=embed)

    @bridge.bridge_command(aliases=["OwO"])
    async def owoify(self, ctx, *, text="nuzzles you o"):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        final = (
            text[:r]
            .replace("r", "w")
            .replace("R", "W")
            .replace("l", "w")
            .replace("L", "W")
            .replace("you", "u")
            .replace("You", "U")
            .replace("YOU", "U")
            .replace("o", "owo")
            .replace("O", "OwO")
            .replace("f", "fw")
            .replace("F", "Fw")
        )
        await ctx.respond(f"{final}")

    @bridge.bridge_command(aliases=["ud"])
    async def updown(self, ctx, *, text):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        split = list(text[:r])
        for i in split:
            if split.index(i) % 2 == 0:
                split[split.index(i)] = i.upper()
            else:
                split[split.index(i)] = i.lower()
        await ctx.respond(f'{"".join(split)}')

    @bridge.bridge_command()
    async def hify(self, ctx, *, text):
        r = len(text)
        if text.endswith(ghost):
            await ctx.message.delete()
            r = -(len(ghost))
        final = str(text)
        for i in ["a", "e", "i", "o", "u"]:
            final = final.replace(i, "h")
            final = final.replace(i.upper(), "h")
        await ctx.respond(final[:r])

    @bridge.bridge_command()
    async def spoof(self, ctx, *, text):
        if len(text.split("|")) > 1:
            replace = float(text.split("|")[-1])
            text = text.split("|")[0].strip()
        else:
            replace = 1

        replacement_dict = {
            # Lowercase replacements
            "a": "а", # CYRILLIC SMALL LETTER A
            "b": "Ь", # CYRILLIC CAPITAL LETTER SOFT SIGN
            "c": "с", # CYRILLIC SMALL LETTER ES
            "d": "ԁ", # CYRILLIC SMALL LETTER KOMI DE
            "e": "е", # CYRILLIC SMALL LETTER IE
            "f": "f", # There is no replacement for "f", so we keep it as it is.
            "g": "g", # There is no replacement for "g", so we keep it as it is.
            "h": "һ", # CYRILLIC SMALL LETTER SHHA
            "i": "і", # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
            "j": "ј", # CYRILLIC SMALL LETTER JE
            "k": "k", # GREEK SMALL LETTER KAPPA
            "l": "l", # There is no replacement for "l", so we keep it as it is.
            "m": "m", # There is no replacement for "m", so we keep it as it is.
            "n": "п", # CYRILLIC SMALL LETTER PE
            "o": "о", # CYRILLIC SMALL LETTER O
            "p": "р", # CYRILLIC SMALL LETTER ER
            "q": "ԛ", # CYRILLIC SMALL LETTER KOMI DZJE
            "r": "ɾ", # CYRILLIC SMALL LETTER GHE
            "s": "ѕ", # CYRILLIC SMALL LETTER DZE
            "t": "t", # CYRILLIC SMALL LETTER TE
            "u": "υ", # GREEK SMALL LETTER UPSILON
            "v": "ν", # GREEK SMALL LETTER NU
            "w": "w", # There is no replacement for "w", so we keep it as it is.
            "x": "х", # CYRILLIC SMALL LETTER HA
            "y": "у", # CYRILLIC SMALL LETTER U
            "z": "z", # There is no replacement for "z", so we keep it as it is.

            # Uppercase replacements
            "A": "А", # CYRILLIC CAPITAL LETTER A
            "B": "В", # CYRILLIC CAPITAL LETTER VE
            "C": "С", # CYRILLIC CAPITAL LETTER ES
            "D": "D", # There is no replacement for "D", so we keep it as it is.
            "E": "Е", # CYRILLIC CAPITAL LETTER IE
            "F": "F", # There is no replacement for "F", so we keep it as it is.
            "G": "G", # There is no replacement for "G", so we keep it as it is.
            "H": "H", # There is no replacement for "H", so we keep it as it is.
            "I": "I", # There is no replacement for "I", so we keep it as it is.
            "J": "J", # There is no replacement for "J", so we keep it as it is.
            "K": "K", # There is no replacement for "K", so we keep it as it is.
            "L": "L", # There is no replacement for "L", so we keep it as it is.
            "M": "М", # CYRILLIC CAPITAL LETTER EM
            "N": "N", # There is no replacement for "N", so we keep it as it is.
            "O": "О", # CYRILLIC CAPITAL LETTER O
            "P": "Р", # CYRILLIC CAPITAL LETTER ER
            "Q": "Q", # There is no replacement for "Q", so we keep it as it is.
            "R": "R", # There is no replacement for "R", so we keep it as it is.
            "S": "S", # There is no replacement for "S", so we keep it as it is.
            "T": "T", # There is no replacement for "T", so we keep it as it is.
            "U": "U", # There is no replacement for "U", so we keep it as it is.
            "V": "V", # There is no replacement for "V", so we keep it as it is.
            "W": "W", # There is no replacement for "W", so we keep it as it is.
            "X": "X", # There is no replacement for "X", so we keep it as it is.
            "Y": "Y", # There is no replacement for "Y", so we keep it as it is.
            "Z": "Z", # There is no replacement for "Z", so we keep it as it is.
            " ": "\u00A0",
        }
        
        shuffled_range = list(range(len(text)))
        random.shuffle(shuffled_range)

        text = list(text)

        for i in range(round(len(text)*replace)):
            text[shuffled_range[i]] = replacement_dict.get(text[shuffled_range[i]], text[shuffled_range[i]])
            
        await ctx.respond("".join(text))
    
    @bridge.bridge_command(aliases=["pt"])
    async def poorly_translate(self, ctx, *, text):
        return
        """
        Poorly tranlate words using google tranlate
        Format: !poorly_translate <text> | <translation amount>
        Note: Increasing how many times it translate will mean a slower response time
        """
        random.seed(text)
        try:
            text.split("|")
            text = text.split("|")[0]
            amount_of_translation = int(text.split("|")[1])
        except:
            amount_of_translation = 3

        async with ctx.channel.typing():
            pass
        base = text
        reg = str(base)

        for _ in range(amount_of_translation):
            reg = ts.google(
                reg,
                from_language="auto",
                to_language=random.choice(list(language_map.keys())),
            )
        await ctx.respond(
            f'This:\n{base}\nTurned into:\n{ts.google(reg, from_language="auto", to_language= "en")}'
        )

    @bridge.bridge_command(aliases=["sug"])
    async def ai_suggest(self, ctx, *, text):
        openai.api_key = <OPEN AI API KEY>

        if ctx.author.id not in rate_limit:
            rate_limit[ctx.author.id] = 0

        # System message
        system_message = {
            "role": "system",
            "content": "You are a result suggester for a clone of elemental 3 by carykh, users will provide a list of elements and you will provide a reasonable result for those elements. Your response should just be the element with no additional context or reasoning. It doesn't have to be realistic it just has to make some amount of sense. If you are provided with refrences to strange elements, feel free to respond with a strange response. A unique response is better than a generic one and try to include every unique element in the result somehow.",
        }
        if len(text.split("|")) > 1:

            if time.time() - rate_limit[ctx.author.id] < 30:
                await ctx.respond(
                    "Rate Limit: You can only ask for extra detail every 30 seconds."
                )
                return

            system_message["content"] = system_message["content"].replace(
                "Your response should just be the element with no additional context or reasoning.",
                "Your response should include a reasoning for the combination, the format should be <element name> <2 new lines> <reasoning>. The reasoning should brief, max 3 sentences.",
            )
            text = text.split("|")[0]
        if time.time() - rate_limit[ctx.author.id] < 3:
            await ctx.respond(
                "Rate Limit: You can only ask for ai combos every 3 seconds."
            )
            return
        # User message
        user_elements = text
        user_message = {"role": "user", "content": user_elements}

        rate_limit[ctx.author.id] = time.time()

        # Make API call
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[system_message, user_message]
        )

        # Extract the assistant's reply
        assistant_reply = response["choices"][0]["message"]["content"]

        await ctx.respond(assistant_reply.title())

    @bridge.bridge_command(aliases=["ows"])
    async def one_word_story(self, ctx, *, text:str):
        book = "1"
        punctuation = ",\"'“”"
        endings = ".?!"
        
        if book not in story:
            story[book] = {"pages" : [[]], "authors" : [], "last_author" : 0}
        
        if len(text.split(" ")) > 1:
            await ctx.respond("Not 1 word!")
            return
        if ctx.author.id == story[book]["last_author"] and ctx.author.id != 666999744572293170:
            await ctx.respond("You cannot add 2 words in a row!")
            return
        
        text == text.lower().strip()
        is_punc = True
        for i in text:
            if i not in endings and i not in punctuation:
                is_punc = False
                break
        
        if is_punc:
            if get_last_word(book) in endings:
                await ctx.respond("Cannot add punctuation twice in a row!")
                return
                
        
        
        if len("".join(story[book]["pages"][-1])) + len(text) > 1800:
            story[book]["pages"].append([])
        story[book]["pages"][-1].append(text)
        if ctx.author.id not in story[book]["authors"]:
            story[book]["authors"].append(ctx.author.id)
        story[book]["last_author"] = ctx.author.id
        
        
        msg = await ctx.respond("Added word! (You can still edit your message to change it).")
        
        ow_story_check()
        
        while True:

            def check(before, after):
                return before.author == ctx.message.author and before.content != after.content and after.id == ctx.message.id

            try:
                before, text = await self.client.wait_for(
                    'message_edit', check=check, timeout=300
                )
            except asyncio.TimeoutError:
                break
            else:
                text = text.content[text.content.find(" ")+1:]
                
                if story[book]["last_author"] == ctx.author.id:
                    await msg.edit(content = "Edited word! (You can still edit your message to change it).")
                if len(text.split(" ")) > 1:
                    await ctx.respond("Not 1 word!")
                    return
                
                text == text.lower().strip()
                is_punc = True
                for i in text:
                    if i not in endings and i not in punctuation:
                        is_punc = False
                        break
        
                if is_punc:
                    if get_last_word(book) in endings:
                        await ctx.respond("Cannot add punctuation twice in a row!")
                        return
                
                story[book]["pages"][-1][-1] = text
                
                ow_story_check()
        
        await msg.edit(content = "Added word! (You can no longer edit your message to change the word).")
        
        ow_story_check()

    @bridge.bridge_command(aliases=["owsp"])
    async def one_word_story_page(self, ctx, page = -1):
        book = "1"
        
        punctuation = ",\"'“”"
        endings = ".?!"
        
        text = ""
        
        if page == -1:
            page = len(story[book]["pages"]) - 1
        else:
            if len(story[book]["pages"]) - 1 < page-1:
                await ctx.respond(f'There are only {len(story[book]["pages"])} pages!')
                return
            page = page-1
        page_text = f'Page ({len(story[book]["pages"])}/{page+1})\n'
        
        for count, word in enumerate(story[book]["pages"][page]):
            text = word.lower().strip()
            is_punc = True
            for i in text:
                if i not in endings and i not in punctuation:
                    is_punc = False
                    break
            if not is_punc:
                if count != 0:
                    if story[book]["pages"][page][count-1][-1] in endings:
                        text = " " + title(text)
                    else:
                        text = " " + text
                elif page != 0:
                    text = "..." + text
                else:
                    text = title(text)
            page_text += text
        
        if page < len(story[book]["pages"])-1:
            page_text.append("...")
        
        await ctx.respond("".join(page_text))
    
    @bridge.bridge_command()
    async def remove_word(self, ctx, page = -1, word = -1):
        book = "1"
        if ctx.author.id != 666999744572293170:
            return
        try:
            story[book]["pages"][int(page)].pop(int(word))
            await ctx.respond("Removed word")
        except Exception as e:
            await ctx.respond(e)
        ow_story_check()

def setup(client):
    client.add_cog(Text(client))
