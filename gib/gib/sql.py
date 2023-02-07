#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""light wrapper for sqlalchemy"""

import os
import string
import typing
from dataclasses import dataclass

import sqlalchemy  # type: ignore
from sqlalchemy.orm import Session, declarative_base  # type: ignore

from .cfg import Cfg

__all__: tuple[str] = ("SQLiteDB",)


@dataclass(slots=True)
class SQLiteDB:
    engine: sqlalchemy.engine.base.Engine
    base: typing.Any
    session: Session

    def __init__(self, db_name: str, cfg: Cfg) -> None:
        if not os.path.exists(cfg.db_dir):
            os.mkdir(cfg.db_dir)

        self.engine = sqlalchemy.create_engine(
            f"sqlite:///{os.path.join(cfg.db_dir, ''.join(c if c in string.ascii_letters else '_' for c in db_name))}.db?check_same_thread=False"
        )
        self.base = declarative_base()
        self.session = sqlalchemy.orm.Session(self.engine)  # type: ignore

    def table(self, cls: typing.Any) -> typing.Any:
        cls.__tablename__ = cls.__name__
        return type(cls.__name__, (dataclass(cls), self.base), {})

    def init(self) -> None:
        self.base.metadata.create_all(self.engine)

    def commit(self) -> None:
        self.session.commit()

    def __iadd__(self, what: typing.Any) -> "SQLiteDB":
        self.session.add(what)
        self.commit()
        return self

    def __isub__(self, what: sqlalchemy.sql.elements.BinaryExpression) -> "SQLiteDB":  # type: ignore
        self.session.execute(what.left.table.delete().where(what))  # type: ignore
        self.commit()
        return self
