import unittest
import swapp


class TestSwapp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_films = swapp.get_all_films()

    def test_get_all_films(self):
        self.assertEqual(len(TestSwapp.all_films), 7)
        first_film_title = TestSwapp.all_films[0]['title']
        self.assertEqual(first_film_title, 'A New Hope')

    def test_get_lukes_data(self):
        lukes_data = swapp.get_persons_data('luke')
        self.assertEqual(lukes_data['name'], 'Luke Skywalker')
        self.assertEqual(lukes_data['gender'], 'male')
        self.assertEqual(lukes_data['url'], 'https://swapi.co/api/people/1/')

    def test_get_leias_data(self):
        leias_data = swapp.get_persons_data('leia')
        self.assertEqual(leias_data['name'], 'Leia Organa')
        self.assertEqual(leias_data['gender'], 'female')
        self.assertEqual(leias_data['url'], 'https://swapi.co/api/people/5/')

    def test_get_non_existing_person(self):
        self.assertRaises(swapp.PersonNotFoundException,
                          swapp.get_persons_data, "EugeneFama")

    def test_get_biggs_id(self):
        biggs_data = swapp.get_persons_data('biggs')
        self.assertEqual(swapp.get_persons_id(biggs_data), '9')

    def test_get_obiwan_id(self):
        obiwan_data = swapp.get_persons_data('obi')
        self.assertEqual(swapp.get_persons_id(obiwan_data), '10')

    def test_find_shared_films(self):
        ids = {'5', '9'}  # Leia & Biggs
        self.assertEqual(swapp.find_common_films(
            TestSwapp.all_films, ids), ["A New Hope"])

    def test_no_shared_films(self):
        ids = {'11', '9'}  # Anakin & Biggs
        self.assertEqual(swapp.find_common_films(
            TestSwapp.all_films, ids), [])


if __name__ == '__main__':
    unittest.main()
