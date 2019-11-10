import boto3
import os
import datetime

from app.main import db
from app.main.config import Config
from app.main.model.recipe import Recipe, Step, Ingredient
from app.main.model.tag import Tag
from app.main.model.user import User, likes
from app.main.model.image import Image

#TODO remove - only for debugging
import sys


def add_one_image(user, recipe_id, img):

   rec = Recipe.query.filter_by(id=recipe_id).first()
   if rec is None or rec.public != True:
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

   img_name = "{}/{}".format(Config.CDN_URL, img_name)
   img = Image(url=img_name, username=user)
   rec.images.append(img)

   db.session.add(img)
   db.session.add(rec)
   db.session.commit()

   return {
      'status': 'success',
      'message': 'Image successfully uploaded',
      'url': img_name
   }
   

def update_recipe(data, user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()

   #Make sure rec exists and is owned by user
   if rec is None or rec.username != user:
      return {
         'status': 'fail',
         'message': 'Could not find recipe',
      }, 404

   #update rec fields if given
   rec.title = data['title'] if 'title' in data else rec.title
   rec.cooktime = data['cooktime'] if 'cooktime' in data else rec.cooktime
   rec.preptime = data['preptime'] if 'preptime' in data else rec.preptime
   rec.totaltime = data['totaltime'] if 'totaltime' in data else rec.totaltime
   rec.f_image = data['featured_image'] if 'featured_image' in data else rec.f_image
   rec.description = data['description'] if 'description' in data else rec.description
   rec.difficulty = data['difficulty'] if 'difficulty' in data else rec.difficulty
   rec.public = data['public'] if 'public' in data else rec.public
   rec.calories = data['calories'] if 'calories' in data else rec.calories
   rec.cost = data['cost'] if 'cost' in data else rec.cost


   if 'tags' in data:
      #set recipe's tags to only those in request (add/remove tags)
      rec.tags = []
      for t in data['tags']:
         tag = Tag.query.filter_by(tagname=t).first()
         if tag == None:
            tag = Tag(tagname=t)
         rec.tags.append(tag)

   if 'steps' in data:
      for num, s in enumerate(data['steps'], start=1):
         step = Step.query.filter_by(recipe_id=recipe_id).filter_by(number=num).first()
         
         #create step if it does not exist
         if not step:
            step = Step(
               text=s['text'],
               annotation=s['annotation'] if 'annotation' in s else None)
            rec.steps.append(step)

         #step already exists, update it's annotation
         else:
            step.text = s['text']
            if 'annotation' in s:
               step.annotation = s['annotation']
            else:
               step.annotation = None
         db.session.add(step)

   if 'ingredients' in data:
      for num, i in enumerate(data['ingredients'], start=1):
         ing = Ingredient.query.filter_by(recipe_id=recipe_id).filter_by(number=num).first()
         #create ingredient if it did not yet exist
         if not ing:
            ing = Ingredient(
               text=i['text'],
               annotation=i['annotation'] if 'annotation' in i else None)
            rec.ingredients.append(ing)

         #ingredient already exists, update it's annotation
         else:
            ing.text = i['text']
            if 'annotation' in i:
               ing.annotation = i['annotation']
            else:
               i['annotation'] = None
         db.session.add(ing)

   db.session.commit()

   return {
         'status': 'Success',
         'message': 'Recipe updated',
      }, 200


def save_new_recipe(data, user):

   new_recipe = Recipe(
      title=data['title'] if 'title' in data else "None",
      parent_id=data['parent_id'] if 'parent_id' in data and Recipe.query.filter_by(id=data['parent_id']).first != None else None,
      created_on=datetime.datetime.utcnow(),
      cooktime=data['cooktime'] if 'cooktime' in data else "None",
      preptime=data['preptime'] if 'preptime' in data else "None",
      totaltime=data['totaltime'] if 'totaltime' in data else "None",
      username=user,
      public=data['public'] if 'public' in data else True,
      servings=data['servings'] if 'servings' in data else "None",
      source=data['source'] if 'source' in data else 'None',
      calories=data['calories'] if 'calories' in data else None,
      cost=data['cost'] if 'cost' in data else None,
      difficulty=data['difficulty'] if 'difficulty' in data else None,
      description=data['description'] if 'description' in data else None
   )
   if 'tags' in data:
      for t in data['tags']:
         tag = Tag.query.filter_by(tagname=t).first()
         if tag == None:
            tag = Tag(tagname=t)
         new_recipe.tags.append(tag)

   if 'ingredients' in data:
      for i in data['ingredients']:
         new_recipe.ingredients.append(Ingredient(
            text=i['text'], 
            annotation=i['annotation'] if 'annotation' in i else None
         ))

   if 'steps' in data:
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