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
TIMEOUT = 1


class PersonNotFoundException(Exception):
    """Raised when given person was not found on endpoint"""


def run(persons):
    try:
        all_movies = map(get_persons_movies, persons)
    except PersonNotFoundException as e:
        print(e)
        sys.exit()

    common_movies = find_common_movies(all_movies)

    if common_movies:
        for movie in common_movies:
            print(movie)
    else:
        print("The persons given do not appear together in a film.")


def find_common_movies(all_movies):
    return reduce(set.intersection, all_movies)


def get_persons_movies(person):
    req = Request(SEARCH_URL + person, headers=AGENT)
    with urlopen(req, timeout=TIMEOUT) as response:
        json_str = response.read().decode('utf-8')
        data = json.loads(json_str)
    if data['count'] != 1:
        raise PersonNotFoundException(person, "was not found")
    results = data['results'][0]
    return get_movie_titles(results['films'])


def get_movie_titles(film_urls):
    movie_titles = set()
    for url in film_urls:
        req = Request(url, headers=AGENT)
        with urlopen(req, timeout=TIMEOUT) as response:
            json_str = response.read().decode('utf-8')
            movie = json.loads(json_str)
        movie_titles.add(movie['title'])
    return movie_titles


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Finds the films all given Star Wars characters appear together in.')
    parser.add_argument('persons', metavar='person', nargs='+')
    args = parser.parse_args()
    run(args.persons)
