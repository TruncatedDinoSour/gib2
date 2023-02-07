#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib commands"""

import discord as dc  # type: ignore
import sqlalchemy  # type: ignore

import gib


class NoteCmds(gib.cmd.CmdIndex):
    async def _note(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        """add a note"""

        if (note_id := cmd.next_token()) is None:  # type: ignore
            return "missing `note id`"
        elif not cmd.s:
            return "missing note contents"

        try:
            client.cfg.notes_db += client.cfg.note_model(note_id, cmd.s)
        except sqlalchemy.exc.IntegrityError:  # type: ignore
            return "this note already exists"

        return f"saved note `{note_id}`"

    @gib.cmd.noauth
    async def _get(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        """read a note"""

        if (note_id := cmd.next_token()) is None:  # type: ignore
            return "missing `note id`"

        if (
            note := client.cfg.notes_db.session.query(
                client.cfg.note_model.note_content
            )
            .filter_by(note_id=note_id)
            .first()
        ) is not None:
            return "\n".join(f"> {line}" for line in "".join(note).splitlines())

        return "no such note"

    @gib.cmd.noauth
    async def _list(self, client: gib.client.Client, **_) -> str:
        """list all notes"""

        notes_list: str = (
            "\n".join(
                f"**-** {''.join(ent)}"
                for ent in client.cfg.notes_db.session.query(
                    client.cfg.note_model.note_id
                ).all()
            )
            or "*no notes found*"
        )

        return f"""notes :

{notes_list}

use the `get` cmd to read a note, e.g. 'get hello"""

    async def _del(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        """list all notes"""

        if (note_id := cmd.next_token()) is None:  # type: ignore
            return "missing `note id`"
        elif (
            client.cfg.notes_db.session.query(client.cfg.note_model)
            .filter_by(note_id=note_id)
            .first()
            is None
        ):
            return "no such note"

        client.cfg.notes_db -= client.cfg.note_model.note_id == note_id
        return f"deleted note `{note_id}`"


class OsCmds(gib.cmd.CmdIndex):
    pass


class Cmds(NoteCmds, OsCmds):
    @gib.cmd.noauth
    async def _help(self, **_) -> str:
        """print help page"""

        if not self.cmds:
            return "*no commmands*"

        h: str = "commands :\n\n"

        for cmd, fn in self.cmds.items():
            h += f"**-** {'(all) ' if getattr(fn, '__noauth__', None) is not None else ''}\
`{cmd}` (`{fn.__qualname__.split('.', maxsplit=1)[0]}`) -- {fn.__doc__ or '*no help provided*'}\n"

        return h
