# internal
import asyncio
import datetime
import json
import os
import platform
import random
import sys

import aiosqlite
from revChatGPT.V3 import Chatbot

# external
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot as DiscordBot, Context

# local
import kelvinlog
import utils.exceptions

path = os.path.realpath(os.path.dirname(__file__))

# check for config file
if not os.path.isfile(f"{path}\\config.json"):
    sys.exit("\"config.json\" not found")
else:
    with open(f"{path}\\config.json") as file:
        config = json.load(file)

# Register the bot as usual
bot = DiscordBot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=discord.Intents.default(),
    help_command=None
)

# Prepare some stuff
bot.boottime = datetime.datetime.now()

log = kelvinlog.getLogger("HelperKelvin")
log.setProcess("preInit")

bot.log = log
bot.config = config

bot.chat = Chatbot(api_key=config["openai_token"])
bot.chat.persona = "standard"
bot.chat.reset(system_prompt="You are a helpful assistant giving short and helpful answers")

bot.log.info(
    f"Running on {platform.system()} {platform.release()}, Python {platform.python_version()}, trying to Login")


@bot.event
async def on_ready() -> None:
    """
    Code executed when the bot is ready, used to log basic information
    and start presence cycle
    """
    bot.log.setProcess("init")
    bot.log.info(f"Logged in as {bot.user.name}")

    presenceCycle.start()

    if config["sync_commands_globally"]:
        bot.log.info("Syncing commands globally...")
        await bot.tree.sync()

    bot.log.setProcess("main")
    bot.uptime = datetime.datetime.now()
    bot.log.info(f"Finished after {bot.uptime - bot.boottime}")


@bot.event
async def on_command_completion(context: Context) -> None:
    """
        Triggered everytime a command is triggered (with success)

    :param context:
    :return:
    """
    exCommand = str(context.command.qualified_name.split(" ")[0])

    if context.guild:
        bot.log.info(
            f"Executed \"{exCommand}\" command in {context.guild.name}  (ID: {context.guild.id}) by {context.author} "
            f"(ID: {context.author.id})")
    else:
        bot.log.info(f"Executed \"{exCommand}\" command in DM by {context.author} (ID: {context.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    Triggered upon failing to execute a command
    """
    if isinstance(error, utils.exceptions.UserBlacklisted):
        embed = discord.Embed(
            description="You are blacklisted from using the bot!", color=0xE02B2B
        )
        msg = await context.send(embed=embed)
        await msg.delete(delay=5)

        if context.guild:
            bot.log.warn(
                f"{context.author} (ID: {context.author.id}) tried to execute a command in the guild "
                f"{context.guild.name} (ID: {context.guild.id}), but the user is blacklisted from using the bot.")
        else:
            bot.log.warn(f"{context.author} (ID: {context.author.id}) tried to execute a command in the bot's DMs, "
                         f"but the user is blacklisted from using the bot.")

    if isinstance(error, utils.exceptions.UserNotPaying):
        embed = discord.Embed(
            description="You are not allowed to use this feature!", color=0xE02B2B
        )
        msg = await context.send(embed=embed)
        await msg.delete(delay=5)

        if context.guild:
            bot.log.warn(
                f"{context.author} (ID: {context.author.id}) tried to execute a command in the guild "
                f"{context.guild.name} (ID: {context.guild.id}), but the user is not paying.")
        else:
            bot.log.warn(f"{context.author} (ID: {context.author.id}) tried to execute a command in the bot's DMs, "
                         f"but the user is not paying.")

    if isinstance(error, utils.exceptions.UserNotOwner):
        embed = discord.Embed(
            description="You tried to use an owner command!", color=0xE02B2B
        )

        msg = await context.send(embed=embed)
        await msg.delete(delay=5)

        if context.guild:
            bot.log.warn(
                f"{context.author} (ID: {context.author.id}) tried to execute an owner command in the guild "
                f"{context.guild.name} (ID: {context.guild.id}), but the user is not the owner of the bot.")
        else:
            bot.log.warn(
                f"{context.author} (ID: {context.author.id})"
                f" tried to execute an owner command in the bot's DMs, but the user is not the owner of the bot."
            )
    else:
        raise error


@tasks.loop(minutes=1.0)
async def presenceCycle() -> None:
    """
    Some magic using the discord rich presence
    """
    statuses = ["with fire", "House Building Simulator", "with ur mom :P"]

    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


async def initDB() -> None:
    """
    Loads the database I guess
    """
    bot.log.info("Loading database")

    async with aiosqlite.connect(f"{path}/database/database.db") as db:
        with open(f"{path}/database/schema.sql") as f:
            await db.executescript(f.read())
        await db.commit()

    bot.log.info("Database loaded")


async def loadCogs() -> None:
    """
    Loads the commands in categories
    """
    bot.log.info("Trying to load cogs")
    try:
        # grab extensions
        for f in os.listdir(f"{path}\\\\cogs"):
            if f.endswith(".py"):
                extension = f[:-3]

                try:
                    await bot.load_extension(f"cogs.{extension}")
                    bot.log.info(f"Loaded extension \"{extension}\"")

                except discord.ext.commands.errors.NoEntryPointError:
                    bot.log.warn(f"Skipped file \"{f}\"")

                except Exception as e:
                    exception = f"{type(e).__name__}: e"
                    bot.log.warn(f"Failed to load extension {extension:\n{exception}}")

    except FileNotFoundError:
        bot.log.warn("Error loading cogs, folder missing?")


def main() -> None:
    asyncio.run(initDB())
    asyncio.run(loadCogs())

    # Actually starting the bot, but we usin our own logger
    bot.run(config["token"], log_handler=None)


if __name__ == '__main__':
    main()
