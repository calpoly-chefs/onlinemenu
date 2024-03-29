from app.main.model.user import User
from ..service.blacklist_service import save_token

import sys

class Auth:

   @staticmethod
   def login_user(data):
      try:
         # fetch the user data
         user = User.query.filter_by(username=data.get('username')).first()
         print("AUTH ATTEMPT:\n\tuname: {}\n\tpass: {}\n\tmatch: {}".format(data.get('username'), data.get('password'), user.check_password(data.get('password')), file=sys.stderr))
         if user and user.check_password(data.get('password')):
               auth_token = user.encode_auth_token(user.username)
               if auth_token:
                  response_object = {
                     'status': 'success',
                     'message': 'Successfully logged in.',
                     'authorization': auth_token.decode()
                  }
                  return response_object, 200
         else:
               response_object = {
                  'status': 'fail',
                  'message': 'username or password does not match.'
               }
               return response_object, 401

      except Exception as e:
         print(e)
         response_object = {
               'status': 'fail',
               'message': 'Try again'
         }
         return response_object, 500

   @staticmethod
   def logout_user(data):
      if data:
         auth_token = data.split(" ")[1]
      else:
         auth_token = ''
      if auth_token:
         resp = User.decode_auth_token(auth_token)
         if not isinstance(resp, str):
               # mark the token as blacklisted
               return save_token(token=auth_token)
         else:
               response_object = {
                  'status': 'fail',
                  'message': resp
               }
               return response_object, 401
      else:
         response_object = {
               'status': 'fail',
               'message': 'Provide a valid auth token.'
         }
         return response_object, 403

   @staticmethod
   def get_logged_in_user(new_request):
      # get the auth token
      auth_token = new_request.headers.get('authorization')
      print('JWT: {}'.format(auth_token), file=sys.stderr)
      print(dict(new_request.headers), sys.stderr)
      if auth_token:
         uname = User.decode_auth_token(auth_token)
         print('uname: {}'.format(uname), file=sys.stderr)
         if isinstance(uname, str):
               user = User.query.filter_by(username=uname).first()
               if user != None:
                  response_object = {
                     'status': 'success',
                     'data': {
                        'username': user.username,
                        'admin': user.admin,
                        'name': user.name,
                        'registered_on': str(user.registered_on)
                     }
                  }
                  return response_object, 200
                  
         response_object = {
            'status': 'fail',
            'message': 'Invalid auth token'
         }
         return response_object, 401
      else:
         response_object = {
               'status': 'fail',
               'message': 'Provide a valid auth token.'
         }
         return response_object, 401