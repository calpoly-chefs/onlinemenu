from app.main.service.recipe_service import save_new_recipe
from datetime import datetime, timedelta
from app.main import db
from app.main.model.challenge import Challenge

import sys

def get_current_challenge(user):
    now = datetime.now()

    chal = Challenge.query.filter(Challenge.end_date >= now).first()

    chal.recipe.__dict__['liked'] = False

    for r in chal.top_three:
        r.__dict__['liked'] = r.has_liked(user)

    return chal

def create_challenge(data, user):
    now = datetime.now()

    rec = {}
    rec['title'] = data['title']
    rec['cooktime'] = 'Up to you!'
    rec['preptime'] = 'Who knows yet??'
    rec['totaltime'] = '???'
    rec['public'] = True
    rec['servings'] = '???'
    rec['calories'] = 0
    rec['cost'] = 0
    rec['source'] = 'challenge'
    rec['difficulty'] = 10
    rec['description'] = 'The weekly challenge for the week of {}/{}!' \
                        .format(now.month, now.day)
    rec['ingredients'] = data['ingredients']
    rec['steps'] = {}
    rec['tags'] = {'Challenge'}

    rid = save_new_recipe(data=rec, user=user)[0]
    rid = rid['id']

    chal = Challenge(
            recipe_id=rid,
            start_date=now,
            end_date=now+timedelta(days=7)
            )

    db.session.add(chal)
    db.session.commit()