from flask import request
from flask_restplus import Resource

from ..util.dto import SearchDto
from ..service.search_service import *
from ..util.decorator import token_required

api = SearchDto.api
_search_all = SearchDto.search_all

@api.route('/')
class SearchAll(Resource):
   @api.doc('search through everything')
   @api.marshal_with(_search_all, envelope='data')
   @token_required
   def get(self, user):
      """search through everything"""
      query = request.args.get("search")
      ret = {}
      print(query, file=sys.stderr)
      ret["recipes"] = search_recipes(query, user)
      ret["users"] = search_users(query, user)
      ret["tags"] = search_tags(query, user)
      return ret, 200