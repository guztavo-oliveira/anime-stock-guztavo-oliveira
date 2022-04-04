from flask import request, jsonify
from app.models.animes_model import Anime
from app.exceptions import (
    InvalidKeysAnime,
    AnimeAlreadyExists,
    AnimeTableDoesNotExists,
    AnimeDoesNotExists,
)
from http import HTTPStatus
from psycopg2.errors import UniqueViolation, UndefinedTable, lookup
from psycopg2.errorcodes import UNIQUE_VIOLATION, UNDEFINED_TABLE


def register_anime():
    data = request.get_json()

    try:
        anime = Anime(**data)
        return jsonify(anime.register_anime()), HTTPStatus.CREATED

    except InvalidKeysAnime as e:
        return e.message, HTTPStatus.UNPROCESSABLE_ENTITY

    except UniqueViolation:
        return {"error": "Anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY


def get_all_animes():
    try:
        return {"data": Anime.get_all()}, HTTPStatus.OK
    except UndefinedTable:
        return {"data": []}


def get_anime_by_id(anime_id: int):
    try:
        return {"data": [Anime.anime_by_id(anime_id)]}, HTTPStatus.OK
    except UndefinedTable:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except AnimeDoesNotExists as e:
        return e.message, HTTPStatus.NOT_FOUND


def update_anime(anime_id: int):
    data = request.get_json()

    try:
        return Anime.update_anime(anime_id, data), HTTPStatus.OK
    except InvalidKeysAnime as e:
        return e.message, HTTPStatus.UNPROCESSABLE_ENTITY
    except UndefinedTable:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except AnimeDoesNotExists as e:
        return e.message, HTTPStatus.NOT_FOUND
    except UniqueViolation:
        return {"error": "Anime already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY


def remove_anime(anime_id: int):
    try:
        return Anime.delete_anime(anime_id), HTTPStatus.NO_CONTENT
    except UndefinedTable:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except AnimeDoesNotExists as e:
        return e.message, HTTPStatus.NOT_FOUND
