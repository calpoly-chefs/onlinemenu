import uuid
import datetime

from app.main import db
from app.main.model.recipe import Recipe, Annotation
from app.main.model.user import User, likes

#TODO remove - only for debugging
import sys

def update_recipe(data, user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()
   if rec is None or rec.username != user:
      return {
         'status': 'Failure',
         'message': 'Could not find recipe',
      }, 404

   updated_annotations = extract_annotations(data)

   #set foreign key for each annotation
   for a in updated_annotations:
      a.recipe_id = recipe_id

   print("annotations: {}".format(updated_annotations))
   rec.annotations = updated_annotations.copy()
   db.session.add_all(updated_annotations)
   db.session.add(rec)
   db.session.commit()
   print("annotations: {}".format(rec.annotations))


   return {
         'status': 'Success',
         'message': 'Recipe updated',
      }, 200

def extract_annotations(data):
   new_annotations = []
   
   #separate ingredients from annotations, build association
   for index, ing in enumerate(data['ingredients']):
      if 'annotation' in ing:
         new_annotations.append(Annotation(
            text=ing['annotation'],
            placement='ing',
            number=index
         ))

   #separate steps from annotations, build an association
   for index, stp in enumerate(data['steps']):
      if 'annotation' in stp :
         new_annotations.append(Annotation(
            text=stp['annotation'],
            placement='step',
            number=index
         ))

   return new_annotations

def update_fields(data, user):
   new_annotations = []
   
   #separate ingredients from annotations, build association
   ing_list = []
   for index, ing in enumerate(data['ingredients']):
      ing_list.append(ing['ingredient'])
      if 'annotation' in ing:
         new_annotations.append(Annotation(
            text=ing['annotation'],
            placement='ing',
            number=index
         ))

   #separate steps from annotations, build an association
   stp_list = []
   for index, stp in enumerate(data['steps']):
      stp_list.append(stp['step'])
      if 'annotation' in stp :
         new_annotations.append(Annotation(
            text=stp['annotation'],
            placement='step',
            number=index
         ))

   #TODO query parent_id and make sure that circular dependencies are not allowed. (recipe remixing itself)

   updated_recipe = Recipe(
      title=data['title'],
      parent_id=data['parent_id'] if 'parent_id' in data else None,
      created_on= datetime.datetime.utcnow(),
      cooktime=data['cooktime'],
      preptime=data['preptime'],
      totaltime=data['totaltime'],
      username=user,
      public=data['public'],
      servings=data['servings'],
      source=data['source'],
      calories=data['calories'],
      cost=data['cost'],
      description=data['description'],
      ingredients="|".join(ing_list),
      steps="|".join(stp_list)
   )

   return (updated_recipe, new_annotations)

def save_new_recipe(data, user):
   new_recipe, new_annotations = update_fields(data, user)
   save_changes(new_recipe, new_annotations)
   response_object = {
      'status': 'success',
      'message': 'Recipe successfully created.'
   }
   return response_object, 201

def toggle_recipe_like(user, recipe_id):
   has_liked = (db.session.query(likes).filter(likes.c.username==user).filter(likes.c.recipe_id==recipe_id).first() != None)
   usr = User.query.filter_by(username=user).first()
   rec = Recipe.query.filter_by(id=recipe_id).first()

   if (has_liked):
      print("Has liked, unliking", file=sys.stderr)
      usr.liked_recipes.remove(rec)

   else:
      print("No like, liking", file=sys.stderr)
      usr.liked_recipes.append(rec)

   db.session.add(usr)
   db.session.commit()


   
def get_all_recipes(user):
   recs = Recipe.query.all()

   formatted = []

   for rec in recs:
      formatted.append(format_recipe(rec, user))
   
   return formatted

def get_one_recipe(user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()

   if (rec is None):
      return {
         'status': 'fail',
         'message': 'recipe not found'
      }, 404

   return format_recipe(rec, user)

def format_recipe(rec, user):
   ings = []
   stps = []

   new_rec = rec.__dict__

   for index, stp in enumerate(rec.steps.split('|')):
      a = list(filter(lambda x: (x.placement == "step" and x.number == index), rec.annotations))
      stps.append({
         "step": stp,
         "annotation": a[0].text if a else None
      })

   for index, ing in enumerate(rec.ingredients.split('|')):
      a = list(filter(lambda x: (x.placement == "ing" and x.number == index), rec.annotations))
      ings.append({
         "ingredient": stp,
         "annotation": a[0] if a else None
      })

   new_rec['steps'] = stps
   new_rec['ingredients'] = ings
   new_rec['has_liked'] = (db.session.query(likes).filter(likes.c.username==user).filter(likes.c.recipe_id==rec.id).first() != None)

   return rec

def save_changes(rec, annos):
   rec.annotations = annos.copy()
   db.session.add(rec)
   db.session.add_all(annos)
   db.session.commit()
   print("annotations: {}".format(rec.annotations))

def delete_one_recipe(user, recipe_id):
   db.session.delete(Recipe.query.filter(Recipe.username==user).filter(Recipe.id == recipe_id).first())
   db.session.commit()

   return {
      'status': 'success',
      'message': "Recipe {} deleted".format(recipe_id)
   }, 200