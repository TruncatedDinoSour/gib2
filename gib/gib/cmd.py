#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib command parser"""


import typing
from abc import ABC
from dataclasses import dataclass

from . import cfg

__all__: tuple[str, ...] = ("Cmd", "CmdIndex")


@dataclass(slots=True)
class Cmd:
    s: str

    def __init__(self, s: str, cfg: cfg.Cfg) -> None:
        self.s = s.removeprefix(cfg.prefix).strip()

    def remove_token(self, token: str) -> None:
        self.s = self.s.removeprefix(token).strip()

    def next_token(self) -> str | None:
        next_token: str

        try:
            self.remove_token((next_token := self.s.split(maxsplit=1)[0]))
        except IndexError:
            return None

        return next_token

    def __iter__(self) -> "Cmd":
        return self

    def __next__(self) -> str:
        t: str | None = self.next_token()

        if not t:
            raise StopIteration(self)

        return t


class CmdIndex(ABC):
    """a class that has commands
    !! note that you have to start all commands with the _ prefix"""

    _cmds_cache: dict[str, typing.Any] | None = None

    @property
    def cmds(self) -> dict[str, typing.Any]:
        if self._cmds_cache is not None:
            return self._cmds_cache

        d: dict[str, typing.Any] = {
            d[1:]: getattr(self, d) for d in dir(self) if d != "_" and d[0] == "_"
        }

        self._cmds_cache = d
        return d
