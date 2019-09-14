from flask import request
from flask_restplus import Resource

from ..util.dto import RecipeDto
from ..service.recipe_service import get_all_recipes, save_new_recipe, delete_all_recipes, update_recipe
from ..util.decorator import token_required

api = RecipeDto.api
_recipe = RecipeDto.recipe

@api.route('/')
class RecipeList(Resource):
   @api.doc('list of all recipes')
   @api.marshal_list_with(_recipe, envelope='data')
   def get(self):
      """List all recipes"""
      return get_all_recipes()

   @api.response(201, 'Recipe successfully created.')
   @api.doc('create a new recipe')
   @api.expect(_recipe, validate=True)
   @token_required
   def post(self, user):
      """Creates a new User"""
      data = request.json
      return save_new_recipe(data=data, user=user)
   
   @token_required
   def delete(self, user):
      return delete_all_recipes(user)

@api.route('/<int:recipe_id>')
class RecipeSingle(Resource):
   @api.doc('update a recipe\'s annotations')
   @token_required
   @api.expect(_recipe, validate=True)
   def put(self, user, recipe_id):
      """Updates an existing recipe"""
      data = request.json
      return update_recipe(data=data, user=user, recipe_id=recipe_id)