from typing import Any

import uuid6
from django.db import models


class UUIDv7Field(models.UUIDField):
    def __init__(self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        kwargs.setdefault('default', uuid6.uuid7)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        super().__init__(*args, **kwargs)
