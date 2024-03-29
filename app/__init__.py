# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.recipe_controller import api as recipe_ns
from .main.controller.search_controller import api as search_ns
from .main.controller.challenge_controller import api as challenge_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    },
}

api = Api(blueprint,
          title='littleChef back end',
          version='0.1',
          description='The REST API running the tinyWaiter',
          authorizations=authorizations,
          security='Bearer Auth'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns)
api.add_namespace(recipe_ns, path='/recipes')
api.add_namespace(search_ns, path='/search')
api.add_namespace(challenge_ns, path="/challenges")