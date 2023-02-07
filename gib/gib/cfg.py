#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""configuration class"""


import typing
from dataclasses import dataclass

__all__: tuple[str] = ("Cfg",)


@dataclass(slots=True, kw_only=True)
class Cfg:
    prefix: str
    db_dir: str
    notes_db: typing.Any = None
    note_model: type | None = None
