import json

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from utils import check, personas


class GPT(commands.Cog, name="gpt"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="gpt",
        description="Chat with the bot",
    )
    @check.not_blacklisted()
    @check.whitelisted()
    async def gpt(self, context: Context, prompt: str) -> None:
        embed = discord.Embed(
            description=f"*Generating response...*", color=0x9C84EF,
        )
        embed.set_author(name=f"\"{prompt}\"")
        embed.set_footer(text=f"Requested by {context.author.name}#{context.author.discriminator}")

        msg = await context.send(embed=embed)

        self.bot.log.info("Generating response")

        response = self.bot.chat.ask(prompt)

        embed.description = response
        embed.colour = 0x44AA99

        self.bot.log.info(f"Response generated: \"{response[0:30]}\"")

        await msg.edit(embed=embed)

    @commands.hybrid_command(
        name="getgpt",
        description="Chat with the bot",
    )
    @check.not_blacklisted()
    @check.whitelisted()
    async def getgpt(self, context: Context) -> None:
        """
        Dump the history into json and load it into a message
        """
        msg = "Chat History:\n```"
        r = json.loads(json.dumps(self.bot.chat.conversation))
        for i in r["default"]:
            # if i["role"] == "system":
            #    continue

            msg += f"{i['role'].title()}: {i['content']}\n"
        await context.send(msg + "```")

    @commands.hybrid_command(
        name="switchpersona",
        description="Switches between optional jailbreaks"
    )
    @check.not_blacklisted()
    @check.whitelisted()
    @app_commands.choices(persona=[
        app_commands.Choice(name="Standard ChatGPT", value="standard"),
        app_commands.Choice(name="Do Anything Now 11.0", value="dan"),
        app_commands.Choice(name="Superior Do Anything Kelvin", value="sda"),
        app_commands.Choice(name="Evil Confident Kelvin", value="confidant"),
        app_commands.Choice(name="UwU Kelvin", value="uwu"),
        app_commands.Choice(name="BasedGPT v2", value="based"),
        app_commands.Choice(name="OPPO", value="oppo"),
        app_commands.Choice(name="Developer Mode v2", value="dev")
    ])
    async def switchPersona(self, context: Context, persona: app_commands.Choice[str]):
        if str(persona.value) == self.bot.chat.persona:
            await context.send(f"Already set to \"{persona.name}\" persona.")
            return

        self.bot.chat.persona = persona.value
        self.bot.chat.reset(system_prompt=personas.PERSONAS.get(persona.value))

        await context.send(f"Switched to \"{persona.name}\" persona.")
        self.bot.log.info(f"Switched to \"{persona.name}\" persona.")


async def setup(bot):
    await bot.add_cog(GPT(bot))
