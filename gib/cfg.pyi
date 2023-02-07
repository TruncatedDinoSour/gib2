import typing

class Cfg:
    prefix: str
    db_dir: str
    notes_db: typing.Any
    note_model: Union[type, None]
    def __init__(self, *, prefix, db_dir, notes_db, note_model) -> None: ...
