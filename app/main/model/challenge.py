from app.main import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm.session import object_session
from sqlalchemy.types import DateTime
from app.main.config import key

#TODO remove - only for debugging
import sys

class Challenge(db.Model):
   """ Challenge Model for storing recipe challenges """
   __tablename__ = "challenge"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
   recipe = db.relationship("Recipe",
            backref=db.backref("challenge", uselist=False))
   start_date = db.Column(db.DateTime)
   end_date = db.Column(db.DateTime)
   
   @hybrid_property
   def num_contestants(self):
      return self.recipe.remix_count

   @hybrid_property
   def top_three(self):
      return self.recipe.remixes[:3]