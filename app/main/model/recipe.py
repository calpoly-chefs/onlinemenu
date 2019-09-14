from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Recipe(db.Model):
   """ Recipe Model for storing recipes """
   __tablename__ = "recipe"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String(255), nullable=False)
   created_on = db.Column(db.DateTime, nullable=False)
   cooktime = db.Column(db.String(255), nullable=False)
   preptime = db.Column(db.String(255), nullable=False)
   totaltime = db.Column(db.String(255), nullable=False)
   username = db.Column(db.String(50), nullable=False)
   remixcount = db.Column(db.Integer, nullable=False)
   public = db.Column(db.Boolean)
   difficulty = db.Column(db.Integer, nullable=True)
   rating = db.Column(db.Float, nullable=True)
   servings = db.Column(db.String(255), nullable=False)
   source = db.Column(db.String(255), nullable=False)
   calories = db.Column(db.Integer, nullable=True)
   cost = db.Column(db.Float, nullable=True)
   description = db.Column(db.Text) 
   ingredients = db.Column(db.Text)
   steps = db.Column(db.Text)
   annotations = db.relationship('Annotation',
      backref='recipe',
      lazy=True,
      cascade='all, delete-orphan')


   def __repr__(self):
      return "<Recipe '{}'>".format(self.title)

class Annotation(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
   text = db.Column(db.String(255), nullable=False)
   placement = db.Column(db.String(4), nullable=False)
   number = db.Column(db.Integer, nullable=False)

   def __repr__(self):
      return "<Annotation '{}' '{}' '{}' '{}'>".format(self.recipe_id, self.placement, self.number, self.text)
