from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FavPlanets (db.Model):
     __tablename__ = 'favplanets'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = False)

     def serialize(self):
             return {
                 "id": self.id,
                 "user_id": self.user_id,
                 "planet_id": self.planet_id,
             }

class FavPeople (db.Model):
     __tablename__ = 'favpeople'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
     people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = False)

     def serialize(self):
             return {
                 "id": self.id,
                 "user_id": self.user_id,
                 "people_id": self.people_id
             }


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets = db.relationship('Planets', secondary='favplanets', backref='users')
    people = db.relationship('People', secondary='favpeople', backref='users')

    def __repr__(self):
        return '<Users %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "planets":[planet.serialize() for planet in self.planets] if self.planets else None,
            "people":[person.serialize() for person in self.people] if self.people else None
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    specie = db.Column(db.String())
    
    def __repr__(self):
            return '<People %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "specie": self.specie,
            }
    

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(), nullable=False, unique = True)
  
    def __repr__(self):
            return '<Planets %r>' % self.name

    def serialize(self):
            return {
                "id": self.id,
                "name": self.name,

            }