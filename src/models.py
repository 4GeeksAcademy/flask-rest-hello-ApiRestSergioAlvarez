from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ='user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites_characters_list: Mapped[list['FavCharacters']] = relationship(back_populates='user')
    favorites_starships_list: Mapped[list['FavStarships']] = relationship(back_populates='user')
    favorites_planets_list: Mapped[list['FavPlanets']] = relationship(back_populates='user')
    
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
            
        }
        
    def __repr__(self):
        return f'email: {self.email}'


class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    favorites : Mapped[list['FavCharacters']] = relationship(back_populates='people')
    
    def __repr__(self):
        
         return f'{self.name}'
     
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight
        }
    
class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    passengers: Mapped[int] = mapped_column(Integer)
    favorites : Mapped[list['FavStarships']] = relationship(back_populates='starships_list')
    
    
    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'passengers': self.passengers,
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    population: Mapped[int] = mapped_column(Integer)
    galaxy: Mapped[str] = mapped_column(String(120))
    favorites : Mapped[list['FavPlanets']] = relationship(back_populates='planets')
    
    def __repr__(self):
        return f'{self.name}'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'galaxy': self.galaxy
        }
    
class FavCharacters(db.Model):
    __tablename__ = 'fav_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_characters_list')
    people: Mapped['Characters'] = relationship(back_populates='favorites')
    
    def __repr__(self):
        return f'al usuario {self.user} le gusta {self.people}'
    
    
class FavPlanets(db.Model):
    
    __tablename__ = 'fav_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planets: Mapped['Planets'] = relationship(back_populates='favorites')
    user: Mapped['User'] = relationship(back_populates='favorites_planets_list')
    
    def __repr__(self):
        return f'al usuario {self.user} le gusta {self.planets}'
    

class FavStarships(db.Model):
    __tablename__ = 'fav_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    starships_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_starships_list')
    starships_list: Mapped['Starships'] = relationship(back_populates='favorites')
    
    def __repr__(self):
        return f'al usuario {self.user} le gusta {self.starships_list}'
    
