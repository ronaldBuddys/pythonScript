"""
Save a copy of all BBC recipes as JSON files.

Instructions:

Run this file with Python 3 in an environment with BeautifulSoup4 and requests:

virtualenv -p python3 env
source env/bin/activate
pip install requests beautifulsoup4
python recipes.py
"""

import codecs
import os
import json
import requests
#import string
import re

from bs4 import BeautifulSoup

save_directory = '/Users/ronaldmaceachern/Documents/pWorkspace/bbc/recipes2'

if not os.path.exists(save_directory):
  os.makedirs(save_directory)

def tryget(el):
  try:
    return el.text.strip()
  except:
    return "None"

parser = 'html.parser'
root_url = 'http://www.bbc.co.uk/food'
base_url = 'http://www.bbc.co.uk'


#increment over all the href, look for recipe
food_page = requests.get(root_url)
food_soup = BeautifulSoup(food_page.text, parser)

    
recipe_list = list()
checked_page = list()
investigate = list()

#get check each page for recipes
for food_tag in food_soup.find_all('a', href = re.compile('^/food')):
    food_link = food_tag.get('href')
    investigate.append(food_link)

#wonky
investigate = list(set(investigate))

maxPages = 3
pgCount = 0



for chkpge in investigate:
        
        pgCount = pgCount + 1
        #if in programes   
        #if pgCount > maxPages:
        #    break
        
        #if have not checked page already
        if chkpge not in checked_page:
            #add page to checked_page list
            checked_page.append(chkpge)
            print('checking page', chkpge)
            print('recipes so far:' , len(recipe_list))
            print('pages_checked:' , len(checked_page))
            #new food_page
            fp = requests.get(base_url + chkpge)
            fs = BeautifulSoup(fp.text, parser)
            
            #check new tags
            for ft in fs.find_all('a', href = re.compile('^/food')):
                fl = ft.get('href')
                
                #if haven't looked at page, add it to investigation
                if fl not in investigate:
                    investigate.append(fl)
                #if has a recipe, get it. wonky way of getting regular expression, (require ends in number and has an underscore)
                if re.match(re.compile('^/food/recipes/.*[0-9]+$'), fl) and re.match(re.compile('^/food/recipes/.*[_]'), fl) is not None:
                    if fl not in recipe_list:
                        recipe_list.append(fl)
                        #may want to do the following in a for loop
                        recipe_page = requests.get(base_url + fl)
                        recipe_soup = BeautifulSoup(recipe_page.text, parser)
                        name = recipe_soup.find('h1', class_='content-title__text').text.strip()
                        recipe_data = {
                            'name': name,
                            'prep_time': tryget(recipe_soup.find('p', class_='recipe-metadata__prep-time')),
                            'cook_time': tryget(recipe_soup.find('p', class_='recipe-metadata__cook-time')),
                            'serves': tryget(recipe_soup.find('p', class_='recipe-metadata__serves')),
                            'dietary': tryget(recipe_soup.find('p', class_='recipe-metadata__dietary')),
                            'description': tryget(recipe_soup.find('p', class_='recipe-description__text')),
                            'author': {
                                'name': tryget(recipe_soup.find('div', class_='chef__name')),
                                'programme': tryget(recipe_soup.find('div', class_='chef__programme-name')),
                            },
                            'ingredients': [],
                            'method': []
                        }
                        ingredients = recipe_soup.find_all('li', class_='recipe-ingredients__list-item')
                        for ingredient in ingredients:
                            recipe_data['ingredients'].append(ingredient.text.strip())
                        steps = recipe_soup.find_all('li', class_='recipe-method__list-item')
                        for step in steps:
                            recipe_data['method'].append(step.text.strip())
                        recipe_file = codecs.open(os.path.join(save_directory, name + ".json"), 'w', 'utf-8')
                        recipe_file.write(json.dumps(recipe_data, ensure_ascii=False, indent=2, separators=(',', ': ')))
                        recipe_file.close()
                        print('Wrote recipe file for {}'.format(name))        
      
      
'''
for recipe_link in recipe_list:
    recipe_page = requests.get(base_url + recipe_link)
    recipe_soup = BeautifulSoup(recipe_page.text, parser)
    name = recipe_soup.find('h1', class_='content-title__text').text.strip()
    recipe_data = {
        'name': name,
        'prep_time': tryget(recipe_soup.find('p', class_='recipe-metadata__prep-time')),
        'cook_time': tryget(recipe_soup.find('p', class_='recipe-metadata__cook-time')),
        'serves': tryget(recipe_soup.find('p', class_='recipe-metadata__serving')),
        'author': {
          'name': tryget(recipe_soup.find('div', class_='chef__name')),
          'programme': tryget(recipe_soup.find('div', class_='chef__programme-name')),
        },
        'ingredients': [],
        'method': []
      }
    ingredients = recipe_soup.find_all('li', class_='recipe-ingredients__list-item')
    for ingredient in ingredients:
        recipe_data['ingredients'].append(ingredient.text.strip())
    steps = recipe_soup.find_all('li', class_='recipe-method__list-item')
    for step in steps:
        recipe_data['method'].append(step.text.strip())
    recipe_file = codecs.open(os.path.join(save_directory, name + ".json"), 'w', 'utf-8')
    recipe_file.write(json.dumps(recipe_data, ensure_ascii=False, indent=2, separators=(',', ': ')))
    recipe_file.close()
    print('Wrote recipe file for {}'.format(name))      

'''

    
      

  