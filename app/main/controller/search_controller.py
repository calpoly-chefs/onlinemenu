from flask import request
from flask_restplus import Resource

from app.main.util.dto import SearchDto
from app.main.service.search_service import *
from app.main.util.decorator import token_required

api = SearchDto.api
_search_all = SearchDto.search_all
_search_recipe = SearchDto.search_recipe


@api.route('/')
class SearchAll(Resource):
   @api.doc(params={'search' : 'The query string to search for'})
   @api.marshal_with(_search_all, envelope='data')
   @token_required
   def get(self, user):
      """search through everything"""
      query = request.args.get("search")
      ret = {}
      ret["recipes"] = search_recipes(query, user)
      ret["users"] = search_users(query, user)
      ret["tags"] = search_tags(query, user)
      return ret, 200

@api.route('/own')
class SearchOwn(Resource):
   @api.doc(params={'search' : 'The query string to search for'})
   @api.marshal_with(_search_recipe, envelope='data')
   @token_required
   def get(self, user):
      """search through a users recipes"""
      query = request.args.get("search")
      ret = {}
      ret["recipes"] = search_own_recipes(query, user)
