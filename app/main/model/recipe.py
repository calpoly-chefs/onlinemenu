from app.main import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm.session import object_session
import datetime
import jwt
from app.main.config import key
from app.main.model.user import likes

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
   servings = db.Column(db.String(255), nullable=False)
   source = db.Column(db.String(255), nullable=False)
   calories = db.Column(db.Integer, nullable=True)
   cost = db.Column(db.Float, nullable=True)
   description = db.Column(db.Text)
   f_image = db.Column(db.Integer, nullable=True)
   images = db.relationship('Image',
      order_by='Image.id',
      backref='recipe',
      cascade='all,delete,delete-orphan')
   ingredients = db.relationship('Ingredient',
      order_by='Ingredient.number',
      collection_class=ordering_list('number', count_from=1),
      backref='recipe',
      lazy=True,
      cascade='all,delete,delete-orphan')
   steps = db.relationship('Step',
      order_by='Step.number',
      collection_class=ordering_list('number', count_from=1),
      backref='recipe',
      lazy=True,
      cascade='all,delete,delete-orphan')

   @hybrid_property
   def remix_count(self):
      return len(self.remixes)
   
   @remix_count.expression
   def _remix_count_expression(cls):
      q = db.select([db.func.count(Recipe.parent_id)]).\
                where(Recipe.parent_id == cls.id).\
                label("remix_count")
      return q
      
   @hybrid_property
   def featured_image(self):
      if self.f_image is not None:
         return self.images[self.f_image]
      return None

   @hybrid_property
   def community_images(self):
      return (list(filter(lambda img: img.username != self.username, self.images))
            + [r.featured_image for r in self.remixes if r.featured_image is not None])
   
   @hybrid_property
   def owner_images(self):
      return list(filter(lambda img: img.username == self.username, self.images))

   @hybrid_property
   def likes_count(self):
      return len(self.likers)

   #TODO make has_liked work when nested, as in viewing other user's recipes
   @hybrid_method
   def has_liked(self, username):
      return db.session.query(likes).filter(likes.c.username==username).filter(likes.c.recipe_id==self.id).first() != None

   @likes_count.expression
   def _likes_count_expression(cls):
      return (db.select([db.func.count(likes.c.username).label("likes_count")])
               .where(likes.c.recipe_id == cls.id)
               .label("sum_likes")
               )

   def __repr__(self):
      return "<Recipe '{}'>".format(self.title)

class Ingredient(db.Model):
   """ Ingredient model - to be expanded upon"""
   __tablename__ = "ingredient"

   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, primary_key=True)
   number = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.Text, nullable=False)
   annotation = db.Column(db.String(255), nullable=True)

   def __repr__(self):
      return "<Ingredient {}-{}>".format(self.recipe_id, self.number)

class Step(db.Model):
   """ Step model """
   __tablename__ = "step"

   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, primary_key=True)
   number = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.Text, nullable=False)
   annotation = db.Column(db.String(255), nullable=True)

   def __repr__(self):
      return "<Step {}-{}>".format(self.recipe_id, self.number)
