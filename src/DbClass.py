import json
import random
from typing import Any

from dataclasses import dataclass, field, fields

from .JsonEncoder import Decoder
from .JsonEncoder.DefaultJsonEncoder import DefaultJsonEncoder


@dataclass
class DbClass:
    _id: Any = field(init=False, default_factory=lambda: random.randint(0, 2 ** 64))
    json_encoder = DefaultJsonEncoder

    def __post_init__(self):
        for field in fields(self):
            for decoder in Decoder.__subclasses__():
                if decoder.is_valid(field.type):
                    setattr(self, field.name, decoder.decode(getattr(self, field.name)))
                    break

    def get_db_representation(self) -> dict:
        from .DbClassLiteral import DbClassLiteral
        return json.loads(
            json.dumps(
                dict(
                    (
                        field.name,
                        value._id
                        if isinstance(value := getattr(self, field.name), DbClass) and not isinstance(value, DbClassLiteral)
                        else value,
                    )
                    for field in fields(self)
                ),
                cls=self.json_encoder,
            )
        )
