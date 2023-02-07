import typing

class Cfg:
    prefix: str
    db_dir: str
    notes_db: typing.Any
    note_model: Union[type, None]
    shell_timeout: int
    init_status: Union[str, None]
    def __init__(self, *, prefix, db_dir, notes_db, note_model, shell_timeout, init_status) -> None: ...
