from Matchmaker import Matchmaker
import unittest


def absolute_length_difference(first, second):
    return abs(len(first) - len(second))


class TestMatchmaker(unittest.TestCase):
    def test_can_have_more_women_than_men(self):
        women = [1, 2, 3]
        men = [1, 2]
        try:
            matchmaker = Matchmaker(men, women, lambda x, y: 0)
            matchmaker.marry()
        except ValueError:
            self.fail()

    def test_can_have_equal_women_and_men(self):
        women = [1, 2, 3]
        men = [1, 2, 3]
        try:
            matchmaker = Matchmaker(men, women, lambda x, y: 0)
            matchmaker.marry()
        except ValueError:
            self.fail()

    def test_cant_have_fewer_women_than_men(self):
        women = [1, 2]
        men = [1, 2, 3]
        with self.assertRaises(ValueError):
            matchmaker = Matchmaker(men, women, lambda x, y: 0)
            matchmaker.marry()

    # Multiple cases checked here... Should probably be split up.
    def test_strings_match_on_length_difference(self):
        women = ['1', '22', '333']
        men = ['22', '1']
        expected = [('22', '22', 0), ('1', '1', 0)]

        def compute_and_check(msg=None):
            matchmaker = Matchmaker(
                men, women, absolute_length_difference,
            )
            results = matchmaker.marry()

            self.assertCountEqual(results, expected, msg=msg)

        compute_and_check("Fewer man case")

        men.append('333')
        expected.append(('333', '333', 0))

        compute_and_check("Equal count case")

        women.append('4444')

        compute_and_check("Extra woman case")

        men.append('abcd')
        expected.append(('abcd', '4444', 0))

        compute_and_check("Same women and men, strings not identical.")

        men.append('abcdefg')
        women.append('abcdef')
        expected.append(('abcdefg', 'abcdef', 1))

        compute_and_check("Same women and men, one pair differ in length")

        women.append('abcde')
        compute_and_check("Extra woman, not a closest match, ignored")

    def test_match_on_number_difference(self):
        women = [1, 100, 1000]
        men = [5, 90, 10000]

        expected = [
            (5, 1, 4),
            (90, 100, 10),
            (10000, 1000, 9000)
        ]

        matchmaker = Matchmaker(men, women, lambda x, y: abs(x - y))
        results = matchmaker.marry()

        self.assertCountEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
