from flask_restplus import Namespace, fields


class UserDto:
   api = Namespace('user', description='user related operations')
   user = api.model('user', {
      'email': fields.String(required=True, description='user email address'),
      'username': fields.String(required=True, description='user username'),
      'password': fields.String(required=True, description='user password'),
      'public_id': fields.String(description='user Identifier'),
      'name': fields.String(description='users name')
   })

class AuthDto:
   api = Namespace('auth', description='authentication related operations')
   user_auth = api.model('auth_details', {
      'email': fields.String(required=True, description='The email address'),
      'password': fields.String(required=True, description='The user password'),
   })

class RecipeDto:
   api = Namespace('recipe', description='Recipe related operations')
   ingredient_fields = api.model('ingredient', {
      'ingredient': fields.String,
      'annotation': fields.String,
   })

   step_fields = api.model('step', {
      'step': fields.String,
      'annotation': fields.String,
   })

   recipe = api.model('recipe', {
      'title': fields.String,
      'id': fields.Integer,
      'cooktime': fields.String,
      'preptime': fields.String,
      'totaltime': fields.String,
      'username': fields.String,
      'remixcount': fields.Integer,
      'public': fields.Boolean,
      'servings': fields.String,
      'source': fields.String,
      'calories': fields.Integer,
      'cost': fields.Integer,
      'difficulty': fields.Integer,
      'rating': fields.Float,
      'description': fields.String,
      'ingredients': fields.List(
         fields.Nested(ingredient_fields),
         required=True,
         description='The ingredients & associated annotations'),
      'steps': fields.List(
         fields.Nested(step_fields),
         required=True,
         description='The steps & associated annotations')
   })