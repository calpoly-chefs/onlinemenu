from bs4 import BeautifulSoup
import requests
import re
import unicodedata


class AbstractScraper:
   def __init__(self, url):
      r = requests.get(url)
      c = r.content
      self.soup = BeautifulSoup(c, "lxml")

   def normalize_caseless(self, text):
      return unicodedata.normalize("NFKD", text.casefold())

   def caseless_include(self, left, right):
      return self.normalize_caseless(left) in self.normalize_caseless(right) or self.normalize_caseless(right) in self.normalize_caseless(left)

   def is_stem_of_el(self, lst, el):
      for e in lst:
         if (e in el) or (el in e):
            return True
      return False

   def get_selector(self, tag):
      selector = ''

      if (tag.has_attr('id')):
         selector += '#' + tag['id']

      if (tag.has_attr('class')):
         cleanclass = []
         for c in tag['class']:
            if not self.is_stem_of_el(cleanclass, c):
               cleanclass.append(c)
               selector += '.' + c

      if selector is '':
         selector = tag.name
      
      return selector

   # Build selector for user inputted text by order of most stable
   def lookup_selector(self, search_str, scope):

      reverse = scope.find(True, string=re.compile(search_str, re.IGNORECASE))

      if not reverse:
         return self.find_mixed_tags(scope, search_str)

      # First try - use reverse's id / classname
      if reverse.has_attr('id'):
         if len(scope.find_all(id=reverse['id'])) == 1:
            return '#'+reverse['id']

      # Second try - use parent's selector > tagname
      # TODO make sure have unique selector for parent
      parent = reverse.find_parent()

      selector = "{} > {}".format(self.get_selector(parent), self.get_selector(reverse))

      # TODO support returning multiple vs single based on if tag should be multiple or single
      return selector

      # Third try - use parent's selector:nth-child() - check for single elements vs lists like ingred/steps
      for index, el in enumerate(new_els, start=1):
         if search_str in el.get_text():
            break

      selector += ':nth-of-type({})'.format(index)

      return selector

   def child_depth(self, parent, child):
      depth = 1

      while child.parent != parent:
         child = child.parent
         depth += 1

      return depth

   def find_mixed_tags(self, scope, string):
      words = string.split(' ')
      tags = scope.find_all(True, string=re.compile(words[0], re.IGNORECASE))

      #Loop through tags parents until find one with string that matches 'string'
      #This is not necessarily the most shallow tag, so add to depths list for later parsing
      depths = []
      for t in tags:
         d = 0
         for p in t.find_parents(True):
            d += 1
            if p is not None and self.caseless_include(string, p.get_text()):
               depths.append((d, self.get_selector(p)))

      # Loop through array of depths, find most shallow selector
      mindepth = -1
      sel = ""

      for d, s in depths:
         if mindepth == -1 or d < mindepth:
            sel = s
            mindepth = d

      return sel


   def find_scope(self, lookups):
      titles = self.soup.body.find_all(True, string=re.compile(lookups['title'], re.IGNORECASE))
      depth = []

      # compute the depth of titles parent relative to ingredients parent to find closest title to ingredient list
      for title in titles:
         scope = title.parent
         
         if scope is None:
            continue

         el = scope.find(True, string=re.compile(lookups['steps'], re.IGNORECASE))
         while el is None:
            scope = scope.parent

            if scope is None:
               break

            el = scope.find(True, string=re.compile(lookups['steps'], re.IGNORECASE))
         
         if scope != None:
            d = self.child_depth(scope, el)
            depth.append((d, scope))

      mindepth = 0
      scp = self.soup.body

      for d, s in depth:
         if mindepth == 0 or d < mindepth:
            scp = s
            mindepth = d

      return scp

   def grab_selectors(self, lookups):
      #TODO find scope by title/ingredient combo? Title first, then
      # try to find ingredient in parent classes, first success is scope

      scope = self.find_scope(lookups)

      sels = {}
      for key, val in lookups.items():
         sels[key] = self.lookup_selector(val, scope)

      scopesel = self.get_selector(scope)
      #TODO add scope back in
      for k, v in sels.items():
         if v != "" and scopesel not in v.split(' '):
            sels[k] = "{} ".format(scopesel) + v

      print(sels)
      return sels

   def scrape_selector(self, sel):
      els = self.soup.select(sel)
      texts = []

      for e in els:
         texts.append(e.get_text(strip=True))

      return texts
         
   def grab_recipe(self, selectors):
      rec = {}
      for key, val in selectors.items():
         if val != "":
            rec[key] = self.scrape_selector(val)
            print("{} : {}".format(key, rec[key]))

      return rec

selectors = {
   'title': 'h1.recipe-summary__h1',
   'author': 'span.submitter__name',
   'desc': 'div.submitter__description',
   'ingred': 'span[itemprop="recipeIngredient"]',
   'preptime': 'time[itemprop="prepTime"]',
   'cooktime': 'time[itemprop="cookTime"]',
   'totaltime': 'time[itemprop="totalTime"]',
   'steps': 'li.step .recipe-directions__list--item',
   'cals': '.calorie-count span:first-child'}

lookups = {
   'title': 'Zucchini Banana Bread',
   'ingred': 'all-purpose or white whole wheat flour',
   'preptime': '20 Minutes',
   'cooktime': '55 Minutes',
   'totaltime': '1 Hour 15 Minutes',
   'steps': 'Preheat the oven to 350 degrees F. Lightly grease an 8 1/2-inch by 4 1/2-inch loaf pan. Set aside.',
   'yield': '1 Loaf'
}

cookielookups = {
   'title': 'BEST CHOCOLATE CHIP COOKIE RECIPE',
   'desc': 'is easy to make and a great base for',
   'ingred': '1 large egg',
   'preptime': '15',
   'cooktime': '15',
   'totaltime': '30',
   'steps': 'Note: This dough requires chilling.',
   'yield': '24'
}

nyt = {
   'title': 'The Only Ice Cream Recipe You’ll Ever Need',
   'desc': 'This silky, luscious and very classic custard can be used as the base for any ice cream',
   'ingred': 'cups heavy cream',
   'totaltime': '20 minutes plus sev',
   'steps': 'In a small pot, simme',
   'yield': 'About 1 1/2 pints'
}

scraper = AbstractScraper('https://www.melskitchencafe.com/zucchini-banana-bread/')
#scraper = AbstractScraper('https://www.crazyforcrust.com/best-chocolate-chip-cookie-recipe/')
#scraper = AbstractScraper('https://cooking.nytimes.com/recipes/1016605-the-only-ice-cream-recipe-youll-ever-need')
sels = scraper.grab_selectors(lookups)

scraper.grab_recipe(sels)

#otherscraper = AbstractScraper('https://www.nourish-and-fete.com/easy-flour-tortillas-from-scratch/')

#otherscraper.grab_recipe(sels)