from flask import request
from flask_restplus import Resource

from app.main.service.challenge_service import *
from app.main.util.decorator import token_required
from app.main.util.dto import ChallengeDTO

import sys

api = ChallengeDTO.api
_challenge_short = ChallengeDTO.challenge_short
_challenge_create = ChallengeDTO.challenge_create

@api.route('/current')
class CurrentChallenge(Resource):
   @api.doc('get the current challenge')
   @api.marshal_with(_challenge_short, envelope='data')
   @token_required
   def get(self, user):
      """Get the currently active challenge"""
      return get_current_challenge(user=user)

@api.route('/')
class ChallengeAdmin(Resource):
    @api.doc('create a challenge')
    @api.expect(_challenge_create)
    @token_required
    def post(self, user):
        if user != 'remy':
            return {'status':'fail'}, 401
        return create_challenge(data=request.json, user=user)