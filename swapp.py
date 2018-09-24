#!/usr/bin/env python3

import json
import sys
from functools import reduce
from urllib.request import Request, urlopen

ENDPOINT = 'http://swapi.co/api'
FILMS_URL = ENDPOINT + '/films'
PEOPLE_URL = ENDPOINT + '/people'
SEARCH_URL = PEOPLE_URL + '/?search='


class PersonNotFoundException(Exception):
    """Raised when given person was not found on endpoint"""


def run(persons):
    agent = {'User-Agent': 'swapp'}
    try:
        all_movies = map(get_persons_movies, persons)
    except PersonNotFoundException as e:
        print(e)
        sys.exit()

    common_movies = reduce(set.intersection, all_movies)

    if common_movies:
        print("The persons given appear in the following films:")
        for movie in common_movies:
            print(movie)
    else:
        print("The persons given do not appear together film.")


for query in {'luke', 'leia'}:
    req = Request(SEARCH_URL + query, headers=agent)
    with urlopen(req, timeout=0.5) as response:
        query
