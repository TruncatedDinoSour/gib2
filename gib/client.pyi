import discord as dc
from .cfg import Cfg
from .cmd import CmdIndex
from _typeshed import Incomplete

class Client(dc.Client):
    cfg: Incomplete
    cmd_index: Incomplete
    def __init__(self, cfg: Cfg, cmd_index: CmdIndex) -> None: ...
    async def on_message(self, msg: dc.message.Message) -> None: ...
