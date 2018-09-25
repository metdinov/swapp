#!/usr/bin/env python3

import json
import sys
import re
from functools import reduce
from urllib.request import Request, urlopen

# API parameters
ENDPOINT = 'http://swapi.co/api'
FILMS_URL = ENDPOINT + '/films'
PEOPLE_URL = ENDPOINT + '/people'
SEARCH_URL = PEOPLE_URL + '/?search='

# crawler parameters
AGENT = {'User-Agent': 'swapp'}
TIMEOUT = 2


class PersonNotFoundException(Exception):
    """Raised when given person was not found on endpoint"""


def run(names):
    try:
        persons_data = map(get_persons_data, names)
    except PersonNotFoundException as e:
        print(e)
        sys.exit()

    persons_ids = set(map(get_persons_id, persons_data))
    films = get_all_films()
    common_films = find_common_films(films, persons_ids)

    if common_films:
        for movie in common_films:
            print(movie)
    else:
        print("The persons given do not appear together in a film.")


def get_persons_data(name):
    query = fetch_and_parse_data(SEARCH_URL + name)
    person_data = query['results']
    if person_data:
        return person_data[0]
    else:
        raise PersonNotFoundException(name, "was not found")


def get_all_films():
    query = fetch_and_parse_data(FILMS_URL)
    return query['results']


def get_persons_id(person_data):
    person_id = re.findall(r'\d+', person_data['url'])[0]
    return person_id


def find_common_films(films, persons_ids):
    ids_in_film = contains_ids(persons_ids)
    common_films_data = list(filter(ids_in_film, films))
    return [film['title'] for film in common_films_data]


def contains_ids(ids):
    def film_contains_ids(film):
        film_ids = {re.findall(r'\d+', url)[0] for url in film['characters']}
        return all([person_id in film_ids for person_id in ids])
    return film_contains_ids


def fetch_and_parse_data(url, agent=AGENT, timeout=TIMEOUT):
    req = Request(url, headers=AGENT)
    with urlopen(req, timeout=timeout) as response:
        json_str = response.read().decode('utf-8')
        data = json.loads(json_str)
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Finds the films all given Star Wars characters appear together in.')
    parser.add_argument('persons', metavar='person', nargs='+')
    args = parser.parse_args()
    run(args.persons)
