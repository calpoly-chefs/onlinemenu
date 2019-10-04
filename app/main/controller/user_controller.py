from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import *
from ..util.decorator import token_required

api = UserDto.api
_user_short = UserDto.user_short
_user_create = UserDto.user_create
_user_detail = UserDto.user_detail


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user_short, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new User')
    @api.expect(_user_create, validate=True)
    def post(self):
        """Creates a new User"""
        data = request.json
        return save_new_user(data=data)

    


@api.route('/self')
class SelfUser(Resource):
    @api.doc('update the logged in User')
    @api.expect(_user_create, validate=True)
    @token_required
    def put(self, user):
        """ Updates the logged in user """
        return update_existing_user(user=user, data=request.json)

    @api.doc('get self detail')
    @token_required
    @api.marshal_with(_user_detail, envelope='data')
    def get(self, user):
        """ Gets detail about logged in user """
        return get_a_user(user=user, other_user=user)

@api.route('/other/<user_name>')
@api.param('user_name', 'The username of the User')
@api.response(404, 'User not found.')
class OtherUser(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user_detail)
    @token_required
    def get(self, user, user_name):
        """get a user given its Username"""
        user = get_a_user(user=user, other_user=user_name)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/follow/<user_to_follow>')
@api.param('user_to_follow', 'The username of the User to follow/unfollow')
@api.response(404, 'User not found.')
class FollowUser(Resource):
    @api.doc('toggle following a user')
    @token_required
    def post(self, user, user_to_follow):
        return toggle_follow_user(user=user, to_follow=user_to_follow)
