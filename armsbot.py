import os
import discord                       # Look at all these imports baby
from PIL import ImageFont, Image, ImageDraw
from armsplayer import ArmsPlayer    # This one is mine
from discord.ext import commands
from dotenv import load_dotenv
from random import randint

REGIONS = ["NA_EAST", "NA_CENTRAL", "NA_WEST", "NORTH_AMERICA", "EASTERN_EUROPE",
           "WESTERN_EUROPE", "CENTRAL_EUROPE", "EUROPE", "ASIA", "AUSTRALIA",
           "SOUTH_AMERICA"]
ALT_REGIONS = {"NAE": "NA_EAST", "NAC": "NA_CENTRAL", "NAW": "NA_WEST", "NA": "NORTH_AMERICA",
               "EUW": "WESTERN_EUROPE", "EUE": "EASTERN_EUROPE", "EUC": "CENTRAL_EUROPE",
               "EU": "EUROPE", "AS": "ASIA", "AU": "AUSTRALIA", "SA": "SOUTH_AMERICA"}
MAINS = ["spring_man", "ribbon_girl", "ninjara", "master_mummy", "min_min",
         "mechanica", "twintelle", "kid_cobra", "byte_and_barq", "helix",
         "max_brass", "lola_pop", "misango", "springtron", "dr.coyle",
         "undecided"]

load_dotenv()                       # The bot token is stored in a .env file,
TOKEN = os.getenv('DISCORD_TOKEN')  # which is not included for privacy reasons.

bot = commands.Bot(command_prefix='?')  # Bot commands designated by ?
bot.remove_command("help")          # Removes the default help command.

users = {}
goodlines = {}
sep = os.sep
font = ImageFont.truetype("Argentum-Sans-Black-Italic{}"   # Here is the font
                          "ArgentumSans-BlackItalic.otf".format(sep), 20)

f = open('users', 'r')
for line in f:                       # Load stored user data from a text file.
    stuff = line.split(":", 1)
    num = stuff[0]
    traits = stuff[1].split(",")
    player = ArmsPlayer(traits[0], traits[1], traits[2], traits[3],
                        traits[4][:-1])
    users[num] = player
    goodlines[num] = line
f.close()

with open("users", "w") as f:
    for line in goodlines.values():  # Clean up redundant values
        f.write(line)


class ProfileCommands(commands.Cog):  # Class storing all the commands of the
    def __init__(self, robot, ppl):   # bot.
        self.bot = robot
        self.users = ppl

    async def setup(self, ctx, user=None):
        if type(user) == discord.Member:   # User argument is for if setup is
            person = user                  # called from another function,
        else:                              # Otherwise uses the author of the
            person = ctx.author            # message that invoked the setup.
        code = "SW-????-????-????"
        region = "Unknown Region"
        main = "undecided"
        # Write defaults to file
        x = open('users', 'a')
        x.write("{}:{},{},{},1,1\n".format(str(person.id), code, region, main))
        x.close()
        self.users[str(person.id)] = ArmsPlayer(code, region, main)

    @commands.command(name='fc')
    async def friend_code(self, ctx, code=None):
        name = str(ctx.author.id)
        if self.users.__contains__(name):
            if code is None:
                await ctx.send("Invalid friend code.")
                return None
            code = code.upper()
            if code[0:3] == "SW-":      # Allows "SW-" at the start, but OK without.
                code = code[3:]
            code = code.replace("-", "")    # Allows dashes to be in the code, but OK without.
            if len(code) == 12 and code.isnumeric():
                p = self.users[name]
                p.fc = "SW-{}-{}-{}".format(code[:4], code[4:8], code[8:])
                x = open("users", "a")
                x.write("{}:{},{},{},{},{}\n".format(name, p.fc, p.region, p.main,
                                                  p.alt, p.bg))
                x.close()
                await ctx.send("Friend code changed successfully!")
            else:
                await ctx.send("Invalid friend code.")
        else:
            await self.setup(ctx)
            await self.friend_code(ctx, code)

    @commands.command(name='region')
    async def region(self, ctx, region=None, region2=None):
        name = str(ctx.author.id)             # Additional args + ALT_REGIONS dict
        if region is not None:                # allows stuff like ?region North America
            region = region.upper()           # instead of strictly North_America,
        if region2 is not None:               # also not case-sensitive.
            region2 = region2.upper()
            region = region + "_" + region2
        if region in ALT_REGIONS:
            region = ALT_REGIONS.get(region)
        if self.users.__contains__(name):
            if region in REGIONS:
                p = self.users[name]
                x = open("users", "a")
                x.write("{}:{},{},{},{},{}\n".format(name, p.fc, region, p.main,
                                                  p.alt, p.bg))
                x.close()
                p.region = region
                await ctx.send("Region changed successfully!")
            else:
                await ctx.send("Invalid region, please enter again.")
        else:
            await self.setup(ctx)
            await self.region(ctx, region)

    @commands.command(name='main')
    async def main(self, ctx, main=None, main2=None, main3=None):
        if main is None:
            await ctx.send("Invalid character, please enter again.")
            return None                     # Additional args allows stuff like
        if main2 is not None:               # ?main Spring Man instead of
            main = main + "_" + main2       # strictly ?main spring_man
        if main3 is not None:
            main = main + "_" + main3
        name = str(ctx.author.id)
        main = main.lower()         # Main is not case sensitive
        if self.users.__contains__(name):
            if main in MAINS:
                p = self.users[name]
                x = open("users", "a")
                x.write("{}:{},{},{},{},{}\n".format(name, p.fc, p.region, main,
                                                  p.alt, p.bg))
                x.close()
                p.main = main
                await ctx.send("Main changed successfully!")
            else:
                await ctx.send("Invalid character, please enter again.")
        else:
            await self.setup(ctx)
            await self.main(ctx, main)

    @commands.command(name='alt')
    async def alt(self, ctx, alt):
        alt = int(alt)
        if alt < 1 or alt > 4:            # Characters have only 4 alts.
            await ctx.send("Invalid input. Alt number must be between 1-4.")
        else:
            name = str(ctx.author.id)
            if self.users.__contains__(name):
                p = self.users[name]
                x = open("users", "a")
                x.write("{}:{},{},{},{},{}\n".format(name, p.fc, p.region, p.main,
                                                  str(alt), p.bg))
                x.close()
                p.alt = alt
                await ctx.send("Alt changed successfully!")
            else:
                await self.setup(ctx)
                await self.alt(ctx, alt)

    @commands.command(name='bg')
    async def bg(self, ctx, bg):
        bg = int(bg)
        if bg < 1 or bg > 10:      # There are 10 bg colours to choose from.
            await ctx.send("Invalid input. Bg number must be between 1-10.")
        else:
            name = str(ctx.author.id)
            if self.users.__contains__(name):
                p = self.users[name]
                x = open("users", "a")
                x.write("{}:{},{},{},{},{}\n".format(name, p.fc, p.region, p.main,
                                                     p.alt, str(bg)))
                x.close()
                p.bg = bg
                await ctx.send("Bg changed successfully!")
            else:
                await self.setup(ctx)
                await self.bg(ctx, bg)

    @commands.command(name='me')
    async def me(self, ctx, user=None):
        if type(user) == discord.Member:    # Checking if ?me was called on
            person = user                   # someone other than the message author
        else:
            person = ctx.author
        name = str(person.id)
        if self.users.__contains__(name):
            p = self.users[name]
            region = p.region.replace("_", " ").title()
            if region[0:2] == "Na":
                region = region[0] + region[1].upper() + region[2:]
            bg = Image.open("sprites{}partybg{}.png".format(sep, p.bg)).copy()
            char = Image.open("sprites{}{}_{}.png".format(sep, p.main, p.alt))
            bg.paste(char, (66, 10), char)
            draw = ImageDraw.Draw(bg)        # PIL nonsense
            draw.text((10, 140), str(person.name), fill='white', font=font)
            draw.text((10, 170), p.fc, fill='white', font=font)
            draw.text((10, 200), region, fill='white', font=font)
            bg.save("temp.png")
            await ctx.send(file=discord.File("temp.png"))
        else:
            await self.setup(ctx, user)
            await self.me(ctx, user)
            if type(user) != discord.Member:
                await ctx.send("Be sure to set up your profile using ?fc, "
                               "?region, and ?main.")

    @commands.command(name='whois')
    async def whois(self, ctx):
        pinged = ctx.message.mentions    # Only works for pinging other members.
        if len(pinged) == 0:
            await self.me(ctx)
            return None
        for user in pinged:              # Can ping multiple users in 1 command.
            await self.me(ctx, user)

    @commands.command(name='pipis')
    async def pipis(self, ctx):          # Ignore this
        await ctx.send("Where's all the pipis?")

    @commands.command(name='help')
    async def help(self, ctx):           # Sends the help image.
        await ctx.send(file=discord.File("sprites{}armsbothelp.png".format(sep)))

    @commands.command(name='rnd')
    async def rnd(self, ctx, arg=None):
        if arg is None or arg.lower() == 'all':
            await self.rnd(ctx, 'c')         # Randomly rolls both arms and char
            await self.rnd(ctx, 'a')         # by default
            return None
        arg = arg.lower()
        if arg == 'arms' or arg == 'arm' or arg == 'a':
            temp = Image.open("sprites{}ARMS{}bg.png".format(sep, sep))
            im = temp.copy()
            int1 = randint(1, 42)
            int2 = randint(1, 42)
            while int1 == int2:
                int2 = randint(1, 42)        # Picks three unique nums between
            int3 = randint(1, 42)            # 1 - 42.
            while int1 == int3 or int2 == int3:
                int3 = randint(1, 42)
            arm1 = Image.open("sprites{}ARMS{}{}.png".format(sep, sep, str(int1)))
            arm2 = Image.open("sprites{}ARMS{}{}.png".format(sep, sep, str(int2)))
            arm3 = Image.open("sprites{}ARMS{}{}.png".format(sep, sep, str(int3)))
            im.paste(arm1, (0, 0), arm1)      # Dumbass hack where the filenames
            im.paste(arm2, (184, 0), arm2)    # for the pngs of the ARMS are literally
            im.paste(arm3, (368, 0), arm3)    # "1.png" "25.png", etc bcuz I'm lazy
            im.save("temp.png")
            await ctx.send(file=discord.File("temp.png"))
        elif arg == 'char' or arg == 'character' or arg == 'c':
            temp = randint(0, 14)
            char = MAINS[temp]        # Randomly pick a character.
            await ctx.send(file=discord.File("sprites{}{}_1.png".format(sep, char)))
        else:
            await self.rnd(ctx, 'c')
            await self.rnd(ctx, 'a')


bot.add_cog(ProfileCommands(bot, users))   # Adding the commands to the bot
bot.run(TOKEN)      # This runs the bot

# Welcome to the end of the file, I'm sorry you had to see all that
