from .. import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
import datetime
import jwt
from ..config import key

#TODO remove - only for debugging
import sys

tag_recipes = db.Table("tag_recipes",
   db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Tag(db.Model):
   """ Tag Model for storing tags"""
   __tablename__ = "tag"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   tagname = db.Column(db.String(255), nullable=False, unique=True)
   recipes = db.relationship("Recipe", secondary=tag_recipes, backref="tags")
   

   @hybrid_property
   def recipe_count(self):
      return len(self.recipes)

   @recipe_count.expression
   def _recipe_count_expression(cls):
      return (db.select([db.func.count(tag_recipes.c.recipe_id).label("recipe_count")])
               .where(tag_recipes.c.tag_id == cls.id)
               .label("sum_recipes")
               )

   def __repr__(self):
      return self.tagname