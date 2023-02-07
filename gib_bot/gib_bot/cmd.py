#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib commands"""

import discord as dc  # type: ignore
import sqlalchemy  # type: ignore

import gib


class NoteCommands(gib.cmd.CmdIndex):
    async def _note(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        if (note_id := cmd.next_token()) is None:  # type: ignore
            return "missing `note id`"
        elif not cmd.s:
            return "missing note contents"

        try:
            client.cfg.notes_db += client.cfg.note_model(note_id, cmd.s)
        except sqlalchemy.exc.IntegrityError:  # type: ignore
            return "this note already exists"

        return f"saved note `{note_id}`"

    async def _get(
        self, client: gib.client.Client, msg: dc.message.Message, cmd: gib.cmd.Cmd
    ) -> str:
        if (note_id := cmd.next_token()) is None:  # type: ignore
            return "missing `note id`"

        if (
            note := client.cfg.notes_db.session.query(client.cfg.note_model.note_content)
            .filter_by(note_id=note_id)
            .first()
        ) is not None:
            return "\n".join(f"> {line}" for line in "".join(note).splitlines())

        return "no such note"


class Cmds(NoteCommands):
    pass
