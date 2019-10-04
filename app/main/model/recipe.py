from .. import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
import datetime
import jwt
from ..config import key

#TODO remove - only for debugging
import sys

class Recipe(db.Model):
   """ Recipe Model for storing recipes """
   __tablename__ = "recipe"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String(255), nullable=False)
   created_on = db.Column(db.DateTime, nullable=False)
   cooktime = db.Column(db.String(255), nullable=False)
   preptime = db.Column(db.String(255), nullable=False)
   totaltime = db.Column(db.String(255), nullable=False)
   username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
   remixes = db.relationship("Recipe", backref=db.backref('parent', remote_side=[id]))
   parent_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
   public = db.Column(db.Boolean)
   difficulty = db.Column(db.Integer, nullable=True)
   likes = db.Column(db.Integer, nullable=True)
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
      cascade='all,delete,delete-orphan')

   @hybrid_property
   def remix_count(self):
      print("Remixes: {}".format(self.remixes), file=sys.stderr)
      return len(self.remixes)
   
   @remix_count.expression
   def _remix_count_expression(cls):
      q = db.select([db.func.count(Recipe.parent_id)]).\
                where(Recipe.parent_id == cls.id).\
                label("remix_count")
      return q

   @hybrid_property
   def likes_count(self):
      return len(self.likers)

   @likes_count.expression
   def _likes_count_expression(cls):
      return (db.select([db.func.count(likes.c.username).label("likes_count")])
               .where(likes.c.recipe_id == cls.id)
               .label("sum_likes")
               )

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
