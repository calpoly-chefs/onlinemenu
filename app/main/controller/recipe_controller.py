from flask import request
from flask_restplus import Resource

from ..util.dto import RecipeDto
from ..service.recipe_service import *
from ..util.decorator import token_required
from werkzeug.datastructures import FileStorage

api = RecipeDto.api
_recipe = RecipeDto.recipe
_recipe_short = RecipeDto.recipe_short
_recipe_create = RecipeDto.recipe_create

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

@api.route('/')
class RecipeList(Resource):
   @api.doc('list of all recipes')
   @api.marshal_list_with(_recipe_short, envelope='data')
   @token_required
   def get(self, user):
      """List all recipes"""
      return get_all_recipes(user), 200

   @api.response(201, 'Recipe successfully created.')
   @api.doc('create a new recipe')
   @api.expect(_recipe_create, validate=True)
   @token_required
   def post(self, user):
      """Creates a new Recipe"""
      data = request.json
      return save_new_recipe(data=data, user=user)



@api.route('/<int:recipe_id>')
class RecipeSingle(Resource):
   @api.doc('update a recipe\'s annotations')
   @token_required
   @api.expect(_recipe_create, validate=True)
   def put(self, user, recipe_id):
      """Updates an existing recipe"""
      data = request.json
      return update_recipe(data=data, user=user, recipe_id=recipe_id)

   @api.doc('get a single recipe in detail')
   @api.marshal_with(_recipe, envelope='data')
   @token_required
   def get(self, user, recipe_id):
      return get_one_recipe(user=user, recipe_id=recipe_id)

   @api.doc('delete a single recipe')
   @token_required
   def delete(self, user, recipe_id):
      return delete_one_recipe(user, recipe_id)

@api.route('/<int:recipe_id>/like')
class RecipeSingleLike(Resource):
   @api.doc('toggle liking a recipe')
   @token_required
   def post(self, user, recipe_id):
      return toggle_recipe_like(user=user, recipe_id=recipe_id)

@api.route('/<int:recipe_id>/images')
class RecipeImageManager(Resource):
   @api.doc('upload an image to a recipe')
   @api.expect(upload_parser)
   @token_required
   def put(self, user, recipe_id):
      return add_one_image(user, recipe_id, request.files['file'])
   