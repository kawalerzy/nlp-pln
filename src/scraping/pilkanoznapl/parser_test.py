import unittest
from os.path import join

from config import PAGES_PATH
from scraping.pilkanoznapl.parser import parse_article


def load_article() -> str:
    with open(join(PAGES_PATH, 'pilkanoznapl', 'article.html'), 'r') as f:
        return f.read()


class TestArticleParser(unittest.TestCase):

    def test_parse_article(self):
        # given
        article = load_article()

        # when
        result = parse_article(article)

        # then
        print(result)




if __name__ == '__main__':
    unittest.main()
