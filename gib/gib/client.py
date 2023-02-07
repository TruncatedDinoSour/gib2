#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib client"""

import typing

import discord as dc  # type: ignore

from .cfg import Cfg
from .cmd import Cmd, CmdIndex

__all__: tuple[str, ...] = ("Client",)


class Client(dc.Client):
    def __init__(self, cfg: Cfg, cmd_index: CmdIndex) -> None:
        self.cfg: Cfg = cfg
        self.cmd_index: CmdIndex = cmd_index

        super().__init__(intents=dc.Intents.all())

    async def on_message(self, msg: dc.message.Message) -> None:
        if msg.author.bot or not msg.content.startswith(self.cfg.prefix):
            return

        cmd: Cmd = Cmd(msg.content, self.cfg)
        cmd_ret: typing.Any = None

        if (c := cmd.next_token()) is None:
            await msg.reply("no command specified")
            return

        if (cmd_fn := self.cmd_index.cmds.get(c)) is not None:
            if getattr(cmd_fn, "__noauth__", None) is None:
                try:
                    bot_roles: list[dc.role.Role] = msg.channel.guild.get_member(  # type: ignore
                        self.user.id  # type: ignore
                    ).roles  # type: ignore
                except AttributeError:
                    await msg.reply("failed to get bot roles")
                    return

                if not any(
                    role in msg.author.roles and not role.name[0] == "@"  # type: ignore
                    for role in bot_roles
                ):
                    await msg.reply("you have no permissions to this command")
                    return

            cmd_ret = await cmd_fn(client=self, msg=msg, cmd=cmd)
        else:
            await msg.reply("no such command")

        if type(cmd_ret) is str:
            await msg.reply(cmd_ret)
