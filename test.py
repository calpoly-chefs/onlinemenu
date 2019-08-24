from bs4 import BeautifulSoup
import requests
import re

r = requests.get("https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/")
print(r.status_code)
c = r.content

soup = BeautifulSoup(c, "lxml")


# Build selector for user inputted text by order of most stable
def lookup_selector(search_str):
	reverse = soup.body.find(True, string=re.compile(search_str))

	if not reverse:
		return ""

	# First try - use reverse's id / classname
	if reverse.has_attr('id'):
		if len(soup.find_all(id=reverse['id'])) == 1:
			return '#'+reverse['id'];

	# Second try - use parent's selector > tagname
	# TODO make sure have unique selector for parent
	parents = reverse.find_parent()

	selector = parents.name

	if (parents.has_attr('id')):
		selector += '#' + parents['id']

	if (parents.has_attr('class')):
		for c in parents['class']:
			selector += '.' + c

	selector = selector + ' > ' + reverse.name

	new_els = soup.select(selector);
	if len(new_els) == 1:
		return selector

	# Third try - use parent's selector:nth-child()
	for index, el in enumerate(new_els, start=1):
		if search_str in el.get_text():
			break

	selector += ':nth-of-type({})'.format(index)

	return selector


print(lookup_selector("Crisp edges, chewy middles"))