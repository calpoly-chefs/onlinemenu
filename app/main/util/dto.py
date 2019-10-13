from flask_restplus import Namespace, fields


class AuthDto:
   api = Namespace('auth', description='authentication related operations')
   user_auth = api.model('auth_details', {
      'username': fields.String(required=True, description='The user username'),
      'password': fields.String(required=True, description='The user password'),
   })

class RecipeDto:
   api = Namespace('recipe', description='Recipe related operations')
   ingredient_fields = api.model('ingredient', {
      'text': fields.String,
      'annotation': fields.String(required=False),
      'number': fields.Integer
   })

   step_fields = api.model('step', {
      'text': fields.String,
      'annotation': fields.String(required=False),
      'number': fields.Integer
   })

   recipe_short = api.model('recipe_short', {
      'title': fields.String,
      'id': fields.Integer,
      'totaltime': fields.String,
      'username': fields.String,
      'remix_count': fields.Integer,
      'likes_count': fields.Integer,
      'description': fields.String,
      'featured_image': fields.String,
      'tags': fields.List(fields.String)
   })

   recipe_create = api.model('recipe_create', {
      'title': fields.String,
      'parent_id': fields.Integer,
      'id': fields.Integer,
      'cooktime': fields.String,
      'preptime': fields.String,
      'totaltime': fields.String,
      'username': fields.String,
      'public': fields.Boolean,
      'servings': fields.String,
      'source': fields.String,
      'calories': fields.Integer,
      'cost': fields.Integer,
      'difficulty': fields.Integer,
      'description': fields.String,
      'featured_image': fields.String,
      'images': fields.List(fields.String),
      'ingredients': fields.List(
         fields.Nested(ingredient_fields),
         required=True,
         description='The ingredients & associated annotations'),
      'steps': fields.List(
         fields.Nested(step_fields),
         required=True,
         description='The steps & associated annotations'),
      'tags': fields.List(fields.String)
   })

   recipe = api.model('recipe', {
      'title': fields.String,
      'parent_id': fields.Integer,
      'id': fields.Integer,
      'cooktime': fields.String,
      'preptime': fields.String,
      'totaltime': fields.String,
      'username': fields.String,
      'remix_count': fields.Integer,
      'public': fields.Boolean,
      'servings': fields.String,
      'source': fields.String,
      'calories': fields.Integer,
      'cost': fields.Integer,
      'difficulty': fields.Integer,
      'likes_count': fields.Integer,
      'has_liked': fields.Boolean,
      'description': fields.String,
      'featured_image': fields.String,
      'images': fields.List(fields.String),
      'remixes': fields.List(
         fields.Nested(recipe_short),
         required=False,
         description="All remixes of this recipe, in short form"),
      'ingredients': fields.List(
         fields.Nested(ingredient_fields),
         required=True,
         description='The ingredients & associated annotations'),
      'steps': fields.List(
         fields.Nested(step_fields),
         required=True,
         description='The steps & associated annotations'),
      'tags': fields.List(fields.String)
   })

class UserDto:
   api = Namespace('user', description='user related operations')

   user_short = api.model('user_short', {
      'username': fields.String(required=True, description='user username'),
      'name': fields.String(description='users name'),
      'recipe_count': fields.Integer(),
      'following_count': fields.Integer(),
      'total_likes': fields.Integer(),
      'badges': fields.String(),
   })

   user_self = api.model('user_self', {
      'email': fields.String(required=True, description='user email address'),
      'username': fields.String(required=True, description='user username'),
      'name': fields.String(description='users name'),
      'bio': fields.String(),
      'recipe_count': fields.Integer(),
      'total_likes': fields.Integer(),
      'badges': fields.String(),
      'following': fields.List(
         fields.Nested(user_short),
         required=False,
         description="The other users that a user follows"),
      'followers': fields.List(
         fields.Nested(user_short),
         required=False,
         description="The users that follow this user"),
      'recipes': fields.List(
         fields.Nested(RecipeDto.recipe_short),
         required=False,
         description="All of a User's Recipes, in short form"),
      'following_count': fields.String(),
      'follower_count': fields.String(),
   })

   user_create = api.model('user_create', {
      'email': fields.String(required=True, description='user email address'),
      'username': fields.String(required=True, description='user username'),
      'password': fields.String(required=True, description='user password'),
      'name': fields.String(description='users name'),
      'bio': fields.String(description="users bio")
   })

   user_detail = api.model('user_detail', {
      'email': fields.String(required=True, description='user email address'),
      'username': fields.String(required=True, description='user username'),
      'name': fields.String(description='users name'),
      'bio': fields.String(),
      'recipe_count': fields.Integer(),
      'total_likes': fields.Integer(),
      'badges': fields.String(),
      'is_following': fields.Boolean(),
      'following': fields.List(
         fields.Nested(user_short),
         required=False,
         description="The other users that a user follows"),
      'recipes': fields.List(
         fields.Nested(RecipeDto.recipe_short),
         required=False,
         description="All of a User's Recipes, in short form"),
   })