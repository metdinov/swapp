#!/usr/bin/env python3

import json
import sys
from functools import reduce
from urllib.request import Request, urlopen

# API parameters
ENDPOINT = 'http://swapi.co/api'
FILMS_URL = ENDPOINT + '/films'
PEOPLE_URL = ENDPOINT + '/people'
SEARCH_URL = PEOPLE_URL + '/?search='

# crawler parameters
AGENT = {'User-Agent': 'swapp'}
TIMEOUT = 0.5


class PersonNotFoundException(Exception):
    """Raised when given person was not found on endpoint"""


def run(persons):
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


def get_persons_movies(person):
    req = Request(SEARCH_URL + person, headers=AGENT)
    with urlopen(req, timeout=TIMEOUT) as response:
        data = json.load(response)
    if data['count'] != 1:
        raise PersonNotFoundException(person, "was not found")
    return get_movie_titles(data['films'])


def get_movie_titles(film_urls):
    movie_titles = set()
    for url in film_urls:
        req = Request(url, headers=AGENT)
        with urlopen(req, timeout=TIMEOUT) as response:
            movie = json.load(response)
        movie_titles.add(movie['title'])
    return movie_titles


if __name__ == '__main__':
    run(['luke', 'leia'])
