from pony import orm

db = orm.Database()

class User(db.Entity):
    telegram_id = orm.Required(str)
    spotify_id = orm.Optional(str)
    spotify_access_token = orm.Optional(str)
    spotify_refresh_token = orm.Optional(str)
