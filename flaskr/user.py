from flask_login import UserMixin

from .db import get_db


class User(UserMixin):
    def __init__(self, id_, name, email, access_token, id_token):
        self.id = id_
        self.name = name
        self.email = email
        self.access_token = access_token
        self.id_token = id_token

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT id, name, email, access_token, id_token FROM user WHERE id = ?", (user_id, )
        ).fetchone()
        if not user:
            return None

        user = User(id_=user[0], name=user[1], email=user[2], access_token=user[3], id_token=user[4])
        return user

    @staticmethod
    def create(id_, name, email, access_token, id_token):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, access_token, id_token)"
            " VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, access_token, id_token),
        )
        db.commit()
