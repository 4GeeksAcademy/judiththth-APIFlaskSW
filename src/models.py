from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[list["Favs"]] = relationship(back_populates="user")
             #para que se vean todos los favs en una lista
                                    #relationtship indica con quién va a tener relación esta tabla


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    age: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    eyes: Mapped[str] = mapped_column(String(120), nullable=True)
    origin: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favs"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "eyes": self.eyes,
            "origin": self.origin,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    surface: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favs"]] = relationship(back_populates="planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "surface": self.surface,
        }
    
class Favs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
                            #almacena la info del user_id en una columna
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    user: Mapped["User"] = relationship(back_populates="favorites")
                            #establece la relación con la tabla User
    character: Mapped["Character"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
       }