import json
import os
from typing import Callable, TypeVar

from utils import db_manager
from .exceptions import *

T = TypeVar("T")


def owner() -> Callable[[T], T]:
    """
        This is a custom check to see if the user executing the command is an owner of the bot.

    :return:
    """

    async def predicate(context: commands.Context) -> bool:
        with open(
            f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"
        ) as file:
            data = json.load(file)
        if context.author.id != data["owner"]:
            raise UserNotOwner
        return True

    return commands.check(predicate)


def whitelisted() -> Callable[[T], T]:
    """
        Custom check to see if a user pays me :evil:

    :return:
    """

    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_whitelisted(context.author.id):
            return True

        raise UserNotPaying

    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    """
        Custom check to see if a user is blacklisted.

    :return:
    """

    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_blacklisted(context.author.id) and not owner():
            raise UserBlacklisted
        return True

    return commands.check(predicate)
