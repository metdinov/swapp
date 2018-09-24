import unittest
import swapp


class TestSwapp(unittest.TestCase):

    def test_get_single_movie_title(self):
        film_url = ["https://swapi.co/api/films/5/"]
        title = {"Attack of the Clones"}
        self.assertEqual(swapp.get_movie_titles(film_url), title)

    def test_get_many_movie_titles(self):
        film_urls = [
            "https://swapi.co/api/films/2/",
            "https://swapi.co/api/films/6/",
            "https://swapi.co/api/films/3/",
            "https://swapi.co/api/films/1/",
            "https://swapi.co/api/films/7/"
        ]
        titles = {
            "The Empire Strikes Back",
            "Revenge of the Sith",
            "Return of the Jedi",
            "A New Hope",
            "The Force Awakens"
        }
        self.assertEqual(swapp.get_movie_titles(film_urls), titles)

    def test_get_lukes_movies(self):
        titles = {
            "The Empire Strikes Back",
            "Revenge of the Sith",
            "Return of the Jedi",
            "A New Hope",
            "The Force Awakens"
        }
        self.assertEqual(swapp.get_persons_movies("luke"), titles)

    def test_get_biggs_movies(self):
        titles = {
            "A New Hope"
        }
        self.assertEqual(swapp.get_persons_movies("biggs"), titles)

    def test_non_existing_person(self):
        self.assertRaises(swapp.PersonNotFoundException,
                          swapp.get_persons_movies, "EugeneFama")

    def test_some_shared_movies(self):
        some_movies = iter([{"The Empire Strikes Back", "A New Hope"},
                            {"The Force Awakens", "The Empire Strikes Back"},
                            {"The Empire Strikes Back", "The Force Awakens"}])
        self.assertEqual(swapp.find_common_movies(
            some_movies), {"The Empire Strikes Back"})

    def test_no_shared_movies(self):
        some_movies = iter([{"Revenge of the Sith", "A New Hope"},
                            {"The Force Awakens", "Return of the Jedi"}])
        self.assertEqual(swapp.find_common_movies(some_movies), set())


if __name__ == '__main__':
    unittest.main()
