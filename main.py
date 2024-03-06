from crawler import WebCrawler
from invertedIndex import InvertedIndex


def run_crawler():
    crawler = WebCrawler()
    crawler.download_pages()


def run_inverted_index():
    inverted_index = InvertedIndex()
    inverted_index.create_index_file()


if __name__ == '__main__':
    # run_crawler()
    run_inverted_index()
