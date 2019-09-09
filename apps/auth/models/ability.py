from library.api.db import EntityWithNameModel, db


class Ability(EntityWithNameModel):
    handler = db.Column(db.String(100))
