from app.exceptions import InvalidKeysAnime, AnimeDoesNotExists
from app.models import conn_cur, commit_close
from psycopg2 import sql


class Anime:

    available_keys = ["anime", "released_date", "seasons"]

    def __init__(self, **kwargs):

        self.verify_keys(kwargs)
        self.anime = str(kwargs["anime"]).lower().title()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    def register_anime(self):
        conn, cur = conn_cur()

        query = """
            CREATE TABLE IF NOT EXISTS animes (
                id            BIGSERIAL     PRIMARY KEY,
                anime         VARCHAR(100)  NOT NULL UNIQUE,
                released_date DATE          NOT NULL,
                seasons       INT           NOT NULL
            );

            INSERT INTO animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *;
        """

        cur.execute(query, tuple(self.__dict__.values()))

        added_anime = cur.fetchone()

        commit_close(conn, cur)

        return self.serialize_anime(added_anime)

    @classmethod
    def get_all(cls):
        conn, cur = conn_cur()

        query = """
            SELECT * FROM animes;
            """

        cur.execute(query)

        res = cur.fetchall()

        if not res:
            return res

        commit_close(conn, cur, commit=False)

        return [cls.serialize_anime(anime) for anime in res]

    @classmethod
    def anime_by_id(cls, id: int):
        conn, cur = conn_cur()

        query = sql.SQL(
            """
            SELECT * FROM animes WHERE id = {id};
            """
        ).format(id=sql.Literal(id))

        cur.execute(query)

        res = cur.fetchone()

        if not res:
            raise AnimeDoesNotExists

        commit_close(conn, cur, commit=False)

        return cls.serialize_anime(res)

    @classmethod
    def update_anime(cls, anime_id: int, data: dict):

        cls.verify_keys(data)

        conn, cur = conn_cur()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]
        sql_user_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}
            RETURNING *;
            """
        ).format(
            id=sql_user_id,
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cur.execute(query)

        updated_anime = cur.fetchone()

        commit_close(conn, cur)

        return cls.serialize_anime(updated_anime)

    @classmethod
    def delete_anime(cls, anime_id: int):
        conn, cur = conn_cur()

        query = sql.SQL(
            """
            DELETE FROM animes
            WHERE id = {anime_id}
            RETURNING *;
        """
        ).format(anime_id=sql.Literal(anime_id))

        cur.execute(query)

        res = cur.fetchone()
        print(res)
        if not res:
            raise AnimeDoesNotExists

        commit_close(conn, cur)

        return "deleted"

    @classmethod
    def verify_keys(cls, kwargs):
        invalid_keys = []

        for key in list(kwargs.keys()):
            if key not in cls.available_keys:
                invalid_keys.append(key)

        if invalid_keys:
            raise InvalidKeysAnime(cls.available_keys, invalid_keys)

    @classmethod
    def get_column_titles(cls):
        titles = []
        conn, cur = conn_cur()

        query = """
            SELECT 
                column_name 
            FROM 
                INFORMATION_SCHEMA.COLUMNS 
            WHERE 
                TABLE_NAME = 'animes'
            ORDER BY ordinal_position; --mantém a ordem das colunas do banco
        """

        cur.execute(query)

        column_titles = cur.fetchall()

        for e in column_titles:
            titles.append(e[0])

        commit_close(conn, cur)

        return titles

    @classmethod
    def serialize_anime(cls, anime: list[tuple]):

        column_titles = cls.get_column_titles()
        return dict(zip(column_titles, anime))
