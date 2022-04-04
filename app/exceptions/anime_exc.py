from psycopg2.errors import (
    UniqueViolation,
    UndefinedTable,
    OperationalError,
    ProgrammingError,
    lookup,
)

from psycopg2 import Error

from psycopg2.errorcodes import UNIQUE_VIOLATION, UNDEFINED_TABLE


class InvalidKeysAnime(Exception):
    def __init__(self, available_keys: list, invalid_keys: list):

        self.message = {
            "available_keys": available_keys,
            "wrong_keys_sended": invalid_keys,
        }


class AnimeDoesNotExists(Exception):
    def __init__(self):
        self.message = {"error": "Not Found"}


class AnimeAlreadyExists(UniqueViolation):
    def __init__(self):
        self.message = {"error": "Anime already exists"}


class AnimeTableDoesNotExists(lookup(UNDEFINED_TABLE)):
    # lookup(UNDEFINED_TABLE)

    def __init__(self):
        self.message = {"data": []}
