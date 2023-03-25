import platform

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from utils import check


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="botinfo",
        description="Get some information about the bot.",
    )
    @check.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
            Get some information about the bot

        :param context: The hybrid command context.
        :return:
        """
        embed = discord.Embed(
            color=0x9C84EF,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="```ColGroLoOl```", inline=True)
        embed.add_field(
            name="Python Version:", value=f"```{platform.python_version()}```", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value="```/```",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @check.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
            Check if the bot is alive

        :param context: The hybrid command context.
        :return:
        """
        embed = discord.Embed(
            title="Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @check.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
            Get the current price of bitcoin

        :param context: The hybrid command context.
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:

                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript"
                    )
                    embed = discord.Embed(title="Bitcoin price", color=0x9C84EF,
                                          description=f"The current price is {data['bpi']['USD']['rate']} :dollar:")
                else:
                    embed = discord.Embed(title="Error!", color=0xE02B2B,
                                          description="There is something wrong with the API, please try again later")

                await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
