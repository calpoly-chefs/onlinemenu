import boto3
import os
from sqlalchemy import or_

from app.main import db
from app.main.model.recipe import Recipe, Step, Ingredient
from app.main.model.tag import Tag
from app.main.model.user import User, likes

#TODO remove - only for debugging
import sys

def search_recipes(s, user):
    search = "%{}%".format(s)

    all_recs = Recipe.query.filter(or_(Recipe.title.ilike(search), Ingredient.text.ilike(search))).limit(10).all()

    for rec in all_recs:
        rec.__dict__["has_liked"] = rec.has_liked(user)

    return all_recs


def search_users(s, user):
    search = "%{}%".format(s)

    all_users = (User.query.filter(or_(User.username.ilike(search), User.bio.ilike(search))) 
                .limit(10)                                                                  
                .all())

    for usr in all_users:
        usr.__dict__["is_following"] = usr.is_following(user)

    return all_users

def search_tags(s, user):
    search = "%{}%".format(s)

    all_tags = Tag.query.filter(Tag.tagname.ilike(search)).limit(10).all()

    return all_tags

def search_own_recipes(s, user):
    search = "%{}%".format(s)

    recs = (Recipe.query.filter_by(username=user)                                    
            .filter(or_(Recipe.title.ilike(search), Ingredient.text.ilike(search)))
            .all())

    return recs