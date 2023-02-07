#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gib commands"""

import subprocess

import discord as dc  # type: ignore
import openai
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

        return (
            "no such note"
            if (
                note := client.cfg.notes_db.session.query(
                    client.cfg.note_model.note_content
                )
                .filter_by(note_id=note_id)
                .first()
            )
            is None
            else "".join(note)
        )

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
    async def _sh(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        """run a shell command"""

        if not cmd:
            return "no shell command specified"

        output: str

        try:
            output = subprocess.check_output(
                str(cmd),
                shell=True,
                timeout=client.cfg.shell_timeout,
                stderr=subprocess.STDOUT,
            ).decode()
        except FileNotFoundError:
            output = "-sh: command not found"
        except subprocess.CalledProcessError as err:
            output = f"{(err.output or b'').decode()}\n( exit code {err.returncode} )"
        except subprocess.TimeoutExpired as err:
            output = f"{(err.output or b'').decode()}\n( timeout after {client.cfg.shell_timeout} s )"

        return f"""```sh
$ {cmd}
```

output :

```
{output[:1800]}
```"""


class FunCmds(gib.cmd.CmdIndex):
    async def _say(self, msg: dc.message.Message, cmd: gib.cmd.Cmd, **_) -> None:
        """say your supplied content deleting your original message"""

        await msg.delete()

        if cmd:
            await msg.channel.send(str(cmd))

    async def _status(self, client: gib.client.Client, cmd: gib.cmd.Cmd, **_) -> str:
        """set or reset the `playing` status"""

        status: str | None = cmd.next_token()  # type: ignore

        await client.change_presence(
            activity=None if status is None else dc.Game(name=status)
        )
        return "i have changed my status"

    async def _gpt(
        self, client: gib.client.Client, msg: dc.message.Message, cmd: gib.cmd.Cmd
    ) -> str:
        """ask an AI to generate you something"""

        if not cmd:
            return "no prompt supplied"
        elif client.cfg.openai_api is None:
            return "no openai support"

        openai.api_key = client.cfg.openai_api

        return (
            openai.Completion.create(  # type: ignore
                model="text-davinci-003",
                prompt=str(cmd),
                temperature=0.5,
                max_tokens=client.cfg.openai_max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )["choices"][0]["text"].strip()
            or "*ai couldnt decide*"
        )


class Cmds(NoteCmds, OsCmds, FunCmds):
    @gib.cmd.noauth
    async def _help(self, **_) -> str:
        """print help page"""

        if not self.cmds:
            return "*no commmands*"

        h: str = "commands :\n\n"

        for cmd, fn in self.cmds.items():
            h += f"**-** {'( all ) ' if getattr(fn, '__noauth__', None) is not None else ''}\
`{cmd}` ( `{fn.__qualname__.split('.', maxsplit=1)[0]}` ) -- {fn.__doc__ or '*no help provided*'}\n"

        return h + "\ncommands marked as `( all )` anyone can run"
