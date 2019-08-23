from bs4 import BeautifulSoup
import requests
import re

r = requests.get("https://wifuchs.github.io/sf-maintenance/form.html")
print(r.status_code)
c = r.content

soup = BeautifulSoup(c, "lxml")



def lookup_selector(search_str):
	reverse = soup.find(True, string=re.compile(search_str))

	if not reverse:
		return ""

	# Build selector for user inputted text by order of most stable
	# First try - use reverse's id / classname

	# Second try - use parent's selector > tagname

	# Third try - use parent's selector:nth-child()

	if reverse.has_attr('id'):
		if len(soup.find_all(id=reverse['id'])) == 1:
			return '#'+reverse['id'];

	parents = reverse.find_parent()

	if (parents.has_attr('id')):
		selector = '#' + parents['id']

	if (parents.has_attr('class')):
		for c in parents['class']:
			selector += '.' + c

	selector = selector + ' > ' + reverse.name

	new_els = soup.select(selector);
	print('Using "%s", %i selected' %(selector, len(new_els)));

	for index, el in enumerate(new_els, start=1):
		if search_str in el.get_text():
			break

	selector += ':nth-of-type({})'.format(index)

	new_els = soup.select(selector);
	print('Using "%s", %i selected' %(selector, len(new_els)));
	print(new_els[0].get_text(strip=True))


print(lookup_selector("Using your mobile phone"))