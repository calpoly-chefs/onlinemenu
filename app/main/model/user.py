from .. import db, flask_bcrypt
import datetime
import jwt
from sqlalchemy.ext.hybrid import hybrid_property
from app.main.model.blacklist import BlacklistToken
from ..config import key

likes = db.Table('likes',
                 db.Column('username', db.Integer, db.ForeignKey('user.username')),
                 db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')))

class User(db.Model):
   """ User Model for storing user related details """
   __tablename__ = "user"

   #TODO add bio, #remixes #recipes #likes, badges, profile pic, etc. Refer to FIGMA

   email = db.Column(db.String(255), unique=True, nullable=False)
   registered_on = db.Column(db.DateTime, nullable=False)
   admin = db.Column(db.Boolean, nullable=False, default=False)
   name = db.Column(db.String(100), unique=False)
   username = db.Column(db.String(50), unique=True, primary_key=True)
   password_hash = db.Column(db.String(100))
   badges = db.Column(db.String(50), unique=False, nullable=True)
   bio = db.Column(db.Text)
   recipes = db.relationship("Recipe")
   following = db.relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.username == user_following.c.user_username,
        secondaryjoin=lambda: User.username == user_following.c.following_username,
        backref='followers'
    )
   liked_recipes = db.relationship("Recipe",
                              secondary=likes,
                              backref="likers")

   @hybrid_property
   def recipe_count(self):
      return len(self.recipes)

   @hybrid_property
   def following_count(self):
      return len(self.following)

   @hybrid_property
   def follower_count(self):
      return len(self.followers)

   @hybrid_property
   def total_likes(self):
      return sum(rec.likes_count for rec in self.recipes)

   @property
   def password(self):
      raise AttributeError('password: write-only field')

   @password.setter
   def password(self, password):
      self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

   def check_password(self, password):
      return flask_bcrypt.check_password_hash(self.password_hash, password)

   def encode_auth_token(self, username):
      """
      Generates the Auth Token
      :return: string
      """
      try:
            payload = {
               'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
               'iat': datetime.datetime.utcnow(),
               'sub': username
            }
            return jwt.encode(
               payload,
               key,
               algorithm='HS256'
            )
      except Exception as e:
            return e

   @staticmethod  
   def decode_auth_token(auth_token):
      """
      Decodes the auth token
      :param auth_token:
      :return: integer|string
      """
      try:
         payload = jwt.decode(auth_token, key)
         is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
         if is_blacklisted_token:
               return 'Token blacklisted. Please log in again.'
         else:
               return payload['sub']
      except jwt.ExpiredSignatureError:
         return 'Signature expired. Please log in again.'
      except jwt.InvalidTokenError:
         return 'Invalid token. Please log in again.'

   def __repr__(self):
      return "<User '{}'>".format(self.username)


user_following = db.Table(
    'user_following',
    db.Column('user_username', db.Integer, db.ForeignKey(User.username), primary_key=True),
    db.Column('following_username', db.Integer, db.ForeignKey(User.username), primary_key=True)
)