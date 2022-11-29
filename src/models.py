from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(250))
    diameter = db.Column(db.Integer)

    def __repr__(self):
        return '<Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "diameter": self.diameter,
            "description": self.description
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(250))
    gender = db.Column(db.String(80))
    height = db.Column(db.Integer)

    def __repr__(self):
        return '<Characters %r>' % self.id
    
    def serialize(self):
        return {
                "name": self.name,
                "description": self.description,
                "gender": self.gender,
                "height": self.height
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.id 

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }