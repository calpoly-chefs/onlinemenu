import boto3
import os
import datetime

from app.main import db
from app.main.config import Config
from app.main.model.recipe import Recipe, Step, Ingredient
from app.main.model.tag import Tag
from app.main.model.user import User, likes

#TODO remove - only for debugging
import sys


def add_one_image(user, recipe_id, img):

   rec = Recipe.query.filter_by(id=recipe_id).first()
   if rec is None or rec.username != user:
      return {
         'status': 'fail',
         'message': 'Could not find recipe',
      }, 404

   img_name = '{}-{}'.format(recipe_id, len(rec.images) + 1 if rec.images != None else 1)

   client = boto3.client('s3',
                          endpoint_url='https://littlechef-images.s3-us-west-2.amazonaws.com',
                          aws_access_key_id=os.environ['S3_KEY'],
                          aws_secret_access_key=os.environ['S3_SECRET_KEY'])

   client.put_object(Body=img,
                      Bucket=os.environ['S3_BUCKET'],
                      Key=img_name,
                      ContentType='image/png')

   # workaround to add image to array
   imgs = []
   if rec.images != None:
      imgs = rec.images.copy()
   img_name = "{}/{}".format(Config.CDN_URL, img_name)
   imgs.append(img_name)
   rec.images = imgs

   db.session.add(rec)
   db.session.commit()

   return {
      'status': 'success',
      'message': 'Image successfully uploaded',
      'url': img_name
   }
   

def update_recipe(data, user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()
   if rec is None or rec.username != user:
      return {
         'status': 'fail',
         'message': 'Could not find recipe',
      }, 404

   for t in data['tags']:
      tag = Tag.query.filter_by(tagname=t).first()
      if tag == None:
         tag = Tag(tagname=t)
      rec.tags.append(tag)

   # TODO there might be a better way to do this (query all ingredients with recipe and match numbers???)
   for s in data['steps']:
      step = Step.query.filter_by(recipe_id=recipe_id).filter_by(number=s['number']).first()
      if 'annotation' in s:
         step.annotation = s['annotation']
      else:
         step.annotation = None
      db.session.add(step)

   for i in data['ingredients']:
      ing = Ingredient.query.filter_by(recipe_id=recipe_id).filter_by(number=i['number']).first()
      if 'annotation' in i:
         ing.annotation = i['annotation']
      else:
         i['annotation'] = None
      db.session.add(ing)

   rec.featured_image = data['featured_image'] if 'featured_image' in data else rec.featured_image

   db.session.commit()

   return {
         'status': 'Success',
         'message': 'Recipe updated',
      }, 200


def save_new_recipe(data, user):
   new_recipe = Recipe(
      title=data['title'],
      parent_id=data['parent_id'] if 'parent_id' in data and Recipe.query.filter_by(id=data['parent_id']).first != None else None,
      created_on=datetime.datetime.utcnow(),
      cooktime=data['cooktime'],
      preptime=data['preptime'],
      totaltime=data['totaltime'],
      username=user,
      public=data['public'],
      servings=data['servings'] if 'servings' in data else None,
      source=data['source'],
      calories=data['calories'] if 'calories' in data else None,
      cost=data['cost'] if 'cost' in data else None,
      difficulty=data['difficulty'] if 'difficulty' in data else None,
      description=data['description']
   )

   for t in data['tags']:
      tag = Tag.query.filter_by(tagname=t).first()
      if tag == None:
         tag = Tag(tagname=t)
      new_recipe.tags.append(tag)

   for i in data['ingredients']:
      new_recipe.ingredients.append(Ingredient(
         text=i['text'], 
         annotation=i['annotation'] if 'annotation' in i else None
      ))

   for s in data['steps']:
      new_recipe.steps.append(Step(
         text=s['text'],
         annotation=s['annotation'] if 'annotation' in s else None
      ))


   db.session.add(new_recipe)
   db.session.add_all(new_recipe.ingredients)
   db.session.add_all(new_recipe.steps)
   db.session.add_all(new_recipe.tags)

   db.session.commit()

   response_object = {
      'status': 'success',
      'message': 'Recipe successfully created.',
      'id': new_recipe.id
   }
   return response_object, 201

def toggle_recipe_like(user, recipe_id):
   usr = User.query.filter_by(username=user).first()
   rec = Recipe.query.filter_by(id=recipe_id).first()
   has_liked = rec.has_liked(user)

   if (has_liked):
      usr.liked_recipes.remove(rec)

   else:
      usr.liked_recipes.append(rec)

   db.session.add(usr)
   db.session.commit()
   
   return {
      'status': 'success',
      'message': 'unliked' if has_liked else 'liked'
   }, 200

   
def get_all_recipes(user):
   recs = Recipe.query.all()
   
   for rec in recs:
      rec.__dict__['liked'] = rec.has_liked(user)

   return recs

def get_one_recipe(user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()

   if (rec is None):
      return {
         'status': 'fail',
         'message': 'recipe not found'
      }, 404

   rec.__dict__['liked'] = rec.has_liked(user)

   return rec

def delete_one_recipe(user, recipe_id):
   db.session.delete(Recipe.query.filter(Recipe.username==user).filter(Recipe.id == recipe_id).first())
   db.session.commit()

   return {
      'status': 'success',
      'message': "Recipe {} deleted".format(recipe_id)
   }, 200