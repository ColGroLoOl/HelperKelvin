import os

import aiosqlite

databaseFile = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def get_blacklisted_users() -> list:
    """
        This function will return the list of all blacklisted users.

    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(databaseFile) as db:
        async with db.execute("SELECT user_id, strftime('%s', created_at) FROM blacklist") as cursor:
            result = await cursor.fetchall()

            return result


async def is_blacklisted(user_id: int) -> bool:
    """
        This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(databaseFile) as db:
        async with db.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,)) as cursor:
            result = await cursor.fetchone()

            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
        This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(databaseFile) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()

        rows = await db.execute("SELECT COUNT(*) FROM blacklist")

        async with rows as cursor:
            result = await cursor.fetchone()

            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
        This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(databaseFile) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()

        rows = await db.execute("SELECT COUNT(*) FROM blacklist")

        async with rows as cursor:
            result = await cursor.fetchone()

            return result[0] if result is not None else 0


async def get_whitelisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(databaseFile) as db:
        async with db.execute("SELECT user_id, strftime('%s', created_at) FROM whitelist") as cursor:
            result = await cursor.fetchall()

            return result


# Whitelist stuff
async def is_whitelisted(user_id: int) -> bool:
    """
        This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(databaseFile) as db:
        async with db.execute("SELECT * FROM whitelist WHERE user_id=?", (user_id,)) as cursor:
            result = await cursor.fetchone()

            return result is not None


async def add_user_to_whitelist(user_id: int) -> int:
    """
        This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(databaseFile) as db:
        await db.execute("INSERT INTO whitelist(user_id) VALUES (?)", (user_id,))
        await db.commit()

        rows = await db.execute("SELECT COUNT(*) FROM whitelist")

        async with rows as cursor:
            result = await cursor.fetchone()

            return result[0] if result is not None else 0


async def remove_user_from_whitelist(user_id: int) -> int:
    """
        This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(databaseFile) as db:
        await db.execute("DELETE FROM whitelist WHERE user_id=?", (user_id,))
        await db.commit()

        rows = await db.execute("SELECT COUNT(*) FROM whitelist")

        async with rows as cursor:
            result = await cursor.fetchone()

            return result[0] if result is not None else 0
