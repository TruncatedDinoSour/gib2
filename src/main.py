#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib2"""

import os
import sys
from warnings import filterwarnings as filter_warnings

import sqlalchemy  # type: ignore

import gib
import gib_bot

CFG: gib.cfg.Cfg = gib.cfg.Cfg(prefix="'", db_dir="db")  # type: ignore
NOTES_DB: gib.sql.SQLiteDB = gib.sql.SQLiteDB("notes", CFG)


@NOTES_DB.table
class Note:
    note_id: sqlalchemy.Column[str] = sqlalchemy.Column(
        sqlalchemy.String, primary_key=True
    )
    note_content: sqlalchemy.Column[str] = sqlalchemy.Column(sqlalchemy.String)


CFG.notes_db = NOTES_DB
CFG.note_model = Note


def main() -> int:
    """entry/main function"""

    if (token := os.environ.get("TOKEN")) is None:
        print(
            " !! please set the TOKEN environment variable to your discord bot token",
            file=sys.stderr,
        )
        return 1

    NOTES_DB.init()
    gib.client.Client(CFG, cmd_index=gib_bot.cmd.Cmds()).run(token)

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
