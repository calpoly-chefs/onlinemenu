import datetime

from app.main import db
from app.main.model.user import User, user_following

#TODO remove sys import, was for testing
import sys


def save_new_user(data):
   user = User.query.filter_by(username=data['username']).first()
   if not user:
      new_user = User(
         name=data['name'],
         email=data['email'],
         username=data['username'],
         password=data['password'],
         bio=data['bio'],
         registered_on=datetime.datetime.utcnow()
      )
      save_changes(new_user)
      return generate_token(new_user)
   else:
      response_object = {
         'status': 'fail',
         'message': 'That username is already taken, please try a different one',
      }
      return response_object, 409

def update_existing_user(user, data):
   usr = User.query.filter_by(username=user).first()

   # check if username changed, and if the new username is already taken
   if user != data['username'] and User.query.filter_by(username=data['username']).first() != None:
      return {
         'status': 'fail',
         'message': 'That username is already taken'
      }, 409

   usr.name = data['name']
   usr.email = data['email']
   usr.username = data['username']
   usr.bio = data['bio']

   db.session.commit()
   return {
      'status': 'success',
      'message': 'User successfully updated'
   }, 200


def generate_token(user):
   try:
      # generate the auth token
      auth_token = user.encode_auth_token(user.username)
      response_object = {
         'status': 'success',
         'message': 'Successfully registered.',
         'Authorization': auth_token.decode()
      }
      return response_object, 201
   except Exception as e:
      response_object = {
         'status': 'fail',
         'message': 'Some error occurred. Please try again.'
      }
      return response_object, 401
      
def get_all_users(user):
   users =  User.query.all()
   for usr in users:
      usr.__dict__['is_following'] = usr.is_following(user)
   
   return users


def get_a_user(user, other_user):
   _other_user = User.query.filter_by(username=other_user).first()

   user_dict = _other_user.__dict__
   user_dict['is_following'] = _other_user.is_following(user)
   for r in _other_user.recipes:
      r.__dict__['liked'] = r.has_liked(user)

   return _other_user


def save_changes(data):
   db.session.add(data)
   db.session.commit()

#TODO finish implementing toggle_follow_user
def toggle_follow_user(user, to_follow):
   is_following = (db.session.query(user_following)
               .filter(user_following.c.user_username==user)
               .filter(user_following.c.following_username==to_follow).first() != None)
   usr = User.query.filter_by(username=user).first()
   usr_to_follow = User.query.filter_by(username=to_follow).first()

   if (is_following):
      print("{} already following {}".format(user, to_follow), file=sys.stderr)
      usr.following.remove(usr_to_follow)

   else:
      print("Was not already following", file=sys.stderr)
      usr.following.append(usr_to_follow)

   db.session.add(usr)
   db.session.commit()