import uuid
import datetime

from app.main import db
from app.main.model.recipe import Recipe, Annotation

#TODO remove - only for debugging
import sys

def update_recipe(data, user, recipe_id):
   rec = Recipe.query.filter_by(id=recipe_id).first()
   if rec is None or rec.username != user:
      return {
         'status': 'Failure',
         'message': 'Could not find recipe',
      }, 404

   updated_rec, updated_annotations = update_fields(data, user)

   #TODO make update actually update, not create new recipe

   for a in updated_annotations:
      a.recipe_id = 1

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

def update_fields(data, user):
   new_annotations = []
   
   #convert ingredients array from DTO to pipe separated string
   ing_list = []
   for index, ing in enumerate(data['ingredients']):
      ing_list.append(ing['ingredient'])
      if 'annotation' in ing:
         new_annotations.append(Annotation(
            text=ing['annotation'],
            placement='ing',
            number=index
         ))

   #convert steps array from DTO to pipe separated string
   stp_list = []
   for index, stp in enumerate(data['steps']):
      stp_list.append(stp['step'])
      if 'annotation' in stp :
         new_annotations.append(Annotation(
            text=stp['annotation'],
            placement='step',
            number=index
         ))

   updated_recipe = Recipe(
      title=data['title'],
      created_on= datetime.datetime.utcnow(),
      cooktime=data['cooktime'],
      preptime=data['preptime'],
      totaltime=data['totaltime'],
      username=user,
      remixcount=data['remixcount'] if 'remixcount' in data else 0,
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
      'message': 'Recipe successfully created.',
   }
   return response_object, 201

      
def get_all_recipes():
   recs = Recipe.query.all()

   formatted = []

   for rec in recs:
      formatted.append(format_recipe(rec))
   
   return formatted

def format_recipe(rec):
   ings = []
   stps = []

   new_rec = rec.__dict__
   print("id: {}, annos: {}".format(rec.id, rec.annotations), file=sys.stderr)

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

   return new_rec

def save_changes(rec, annos):
   rec.annotations = annos.copy()
   db.session.add(rec)
   db.session.add_all(annos)
   db.session.commit()
   print("annotations: {}".format(rec.annotations))

def delete_all_recipes(user):
   Recipe.query.delete(synchronize_session=False)
   db.session.commit()

   return {
      'status': 'success',
      'message': 'All recipes deleted'
   }, 200