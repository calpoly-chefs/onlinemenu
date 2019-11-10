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
      'annotation': fields.String(required=False, nullable=True, default=""),
      'number': fields.Integer
   })

   step_fields = api.model('step', {
      'text': fields.String,
      'annotation': fields.String(required=False, nullable=True, default=""),
      'number': fields.Integer
   })

   image_metadata = api.model('image_metadata', {
      'url': fields.String,
      'username': fields.String,
      'profile_image': fields.String,
      'is_remix': fields.Boolean,
      'recipe_id': fields.Integer
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
      'liked': fields.Boolean(default=False, required=False),
      'tags': fields.List(fields.String)
   })

   recipe_create = api.model('recipe_create', {
      'title': fields.String(nullable=True),
      'parent_id': fields.Integer(nullable=True),
      'cooktime': fields.String(nullable=True),
      'preptime': fields.String(nullable=True),
      'totaltime': fields.String(nullable=True),
      'public': fields.Boolean(nullable=True),
      'servings': fields.String(nullable=True),
      'source': fields.String(required=True),
      'calories': fields.Integer,
      'cost': fields.Integer,
      'difficulty': fields.Integer,
      'description': fields.String(nullable=True),
      'ingredients': fields.List(
         fields.Nested(ingredient_fields),
         required=True,
         description='The ingredients & associated annotations'),
      'steps': fields.List(
         fields.Nested(step_fields),
         required=True,
         description='The steps & associated annotations'),
      'tags': fields.List(fields.String,
         nullable=True,
         description='Tags associated with this recipe')
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
      'liked': fields.Boolean(default=False, required=False),
      'description': fields.String,
      'featured_image': fields.String,
      'owner_images': fields.List(fields.String),
      'community_images': fields.List(
         fields.Nested(image_metadata)
      ),
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
      'is_following': fields.Boolean(required=False)
   })

   user_self = api.clone('user_self', user_short, {
      'email': fields.String(required=True, description='user email address'),
      'bio': fields.String(),
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
      'follower_count': fields.String(),
   })

   user_create = api.model('user_create', {
      'email': fields.String(required=True, description='user email address'),
      'username': fields.String(required=True, description='user username'),
      'password': fields.String(required=True, description='user password'),
      'name': fields.String(required=True, description='users name'),
      'bio': fields.String(required=True, description="users bio")
   })

   user_detail = api.clone('user_detail', user_short, {
      'email': fields.String(required=True, description='user email address'),
      'bio': fields.String(),
      'total_likes': fields.Integer(),
      'following': fields.List(
         fields.Nested(user_short),
         required=False,
         description="The other users that a user follows"),
      'recipes': fields.List(
         fields.Nested(RecipeDto.recipe_short),
         required=False,
         description="All of a User's Recipes, in short form"),
   })


class SearchDto:
   api = Namespace('search', description='search related operations')
   search_tag = api.model('search_tag', {
      'tagname': fields.String,
      'recipe_count': fields.Integer
   })
   search_all = api.model('search_all', {
      'recipes': fields.List(
         fields.Nested(RecipeDto.recipe_short),
         required=False,
         description="All matching Recipes, in short form"),
      'users': fields.List(
         fields.Nested(UserDto.user_short),
         required=False,
         description="All matching users, in short form"
      ),
      'tags': fields.List(
         fields.Nested(search_tag),
         required=False,
         description="All matching tags, as strings"
      )
   })
   search_recipe = api.model('search_recipe', {
      'recipes': fields.List(
         fields.Nested(RecipeDto.recipe_short)
      )
   })


class ChallengeDTO:
   api = Namespace('callenge', description='challenges')
   challenge_short = api.model('challenge_short', {
      'recipe': fields.Nested(RecipeDto.recipe),
      'top_three': fields.List(
         fields.Nested(RecipeDto.recipe_short)
      )
   })
   challenge_create = api.model('challenge_create', {
      'ingredients': fields.List(
         fields.Nested(RecipeDto.ingredient_fields),
         required=True,
         description='The required ingredients for the challenge'),
      'title': fields.String(required=True)
   })