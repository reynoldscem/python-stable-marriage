from Matchmaker import Matchmaker
import unittest


class TestMatchmaker(unittest.TestCase):
    def test_cant_have_more_women_than_men(self):
        women = [1, 2, 3]
        men = [1, 2]
        with self.assertRaises(ValueError):
            matchmaker = Matchmaker(men, women, lambda x, y: 0)
            matchmaker.marry()


if __name__ == '__main__':
    unittest.main()
