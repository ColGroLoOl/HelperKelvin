import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from utils import check, db_manager


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    # Blacklist stuff
    @commands.hybrid_group(
        name="blacklist",
        description="[owner] Get the list of all blacklisted users.",
    )
    @check.owner()
    async def blacklist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.
        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.\n\n**Subcommands:**\n"
                            "`add` - Add a user to the blacklist.\n`remove` - Remove a user from the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="show",
        description="[owner] Shows the list of all blacklisted users.",
    )
    @check.owner()
    async def blacklist_show(self, context: Context) -> None:
        """
        Shows the list of all blacklisted users.
        :param context: The hybrid command context.
        """
        blacklisted_users = await db_manager.get_blacklisted_users()
        if len(blacklisted_users) == 0:
            embed = discord.Embed(
                description="There are currently no blacklisted users.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(title="Blacklisted Users", color=0x9C84EF)
        users = []
        for bluser in blacklisted_users:
            user = self.bot.get_user(int(bluser[0])) or await self.bot.fetch_user(
                int(bluser[0])
            )
            users.append(f"• {user.mention} ({user}) - Blacklisted <t:{bluser[1]}>")
        embed.description = "\n".join(users)
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="add",
        description="[owner] Lets you add a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be added to the blacklist")
    @check.owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.
        :param context: The hybrid command context.
        :param user: The user that should be added to the blacklist.
        """
        user_id = user.id
        if await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is already in the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully added to the blacklist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="[owner] Lets you remove a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be removed from the blacklist.")
    @check.owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Lets you remove a user from not being able to use the bot.
        """
        user_id = user.id
        if not await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is not in the blacklist.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = await db_manager.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully removed from the blacklist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    # whitelist
    @commands.hybrid_group(
        name="whitelist",
        description="[owner] Get the list of all whitelisted users.",
    )
    @check.owner()
    async def whitelist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.\n\n**Subcommands:**\n"
                            "`add` - Add a user to the Whitelist.\n`remove` - Remove a user from the Whitelist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @whitelist.command(
        base="whitelist",
        name="show",
        description="[owner] Shows the list of all whitelisted users.",
    )
    @check.owner()
    async def whitelist_show(self, context: Context) -> None:
        """
        Shows the list of all whitelisted users.
        :param context: The hybrid command context.
        """
        whitelisted_users = await db_manager.get_whitelisted_users()
        if len(whitelisted_users) == 0:
            embed = discord.Embed(
                description="There are currently no whitelisted users.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(title="Whitelisted Users", color=0x9C84EF)
        users = []
        for bluser in whitelisted_users:
            user = self.bot.get_user(int(bluser[0])) or await self.bot.fetch_user(
                int(bluser[0])
            )
            users.append(f"• {user.mention} ({user}) - whitelisted <t:{bluser[1]}>")
        embed.description = "\n".join(users)
        await context.send(embed=embed)

    @whitelist.command(
        base="whitelist",
        name="add",
        description="[owner] Lets you add a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be added to the Whitelist")
    @check.owner()
    async def whitelist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.
        :param context: The hybrid command context.
        :param user: The user that should be added to the Whitelist.
        """
        user_id = user.id
        if await db_manager.is_whitelisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is already in the Whitelist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await db_manager.add_user_to_whitelist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully added to the Whitelist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the Whitelist"
        )
        await context.send(embed=embed)

    @whitelist.command(
        base="whitelist",
        name="remove",
        description="[owner] Lets you remove a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be removed from the Whitelist.")
    @check.owner()
    async def whitelist_remove(self, context: Context, user: discord.User) -> None:
        """
        Lets you remove a user from not being able to use the bot.
        """
        user_id = user.id
        if not await db_manager.is_whitelisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is not in the Whitelist.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = await db_manager.remove_user_from_whitelist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully removed from the Whitelist",
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the "
                 f"whitelist"
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
