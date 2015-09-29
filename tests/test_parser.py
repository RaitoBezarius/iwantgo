from src import parser
import unittest

class TestStream(unittest.TestCase):

    def test_list(self):
        stream = parser.Stream("Hello")
        self.assertEqual(list(stream), ['H', 'e', 'l', 'l', 'o'])

    def test_saves(self):
        stream = parser.Stream("Hello")
        stream.save()
        self.assertEqual(next(stream), 'H')
        stream.apply()
        self.assertEqual(next(stream), 'H')
        self.assertEqual(next(stream), 'e')
        stream.drop()
        self.assertEqual(next(stream), 'l')
        self.assertEqual(next(stream), 'l')
        stream.save()
        self.assertEqual(next(stream), 'o')
        stream.pop()
        self.assertEqual(next(stream), 'o')

    def test_stack(self):
        stream = parser.Stream([1, 2, 3, 4])
        stream.save()
        next(stream)
        stream.save()
        self.assertEqual(next(stream), 2)
        next(stream)
        stream.save()
        self.assertEqual(next(stream), 4)
        stream.drop()
        stream.apply()
        self.assertEqual(next(stream), 2)
        stream.pop()
        self.assertEqual(next(stream), 2)
        stream.save()
        next(stream)
        stream.pop()
        stream.pop()
        self.assertEqual(next(stream), 1)


class TestWordRule(unittest.TestCase):

    def test_keyword(self):
        from_parser = parser.keyword("from")
        self.assertEqual(from_parser("lol"), None)
        self.assertEqual(from_parser("from"), dict())

    def test_argument(self):
        argument = parser.argument("destination")
        self.assertEqual(argument("Paris"), {'destination': 'Paris'})
        self.assertEqual(argument(""), None)
        self.assertEqual(argument("Amsterdam"), {'destination': 'Amsterdam'})

    def test_custom(self):
        matcher = lambda word: len(word) == 4
        parser_four = parser.WordRule(matcher, 'arg')
        self.assertEqual(parser_four("Cool"), {'arg': 'Cool'})
        self.assertEqual(parser_four("Coool"), None)
