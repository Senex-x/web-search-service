import os

from crawler import WebCrawler
from tokenizer import Tokenizer


def tokenize():
    print("\n-> Starting tokenizer...")
    input_directory_path = os.path.dirname(__file__) + '/texts'
    output_directory_path = os.path.dirname(__file__) + '/lemmas'

    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)

    all_files = os.listdir(input_directory_path)

    tokenizer = Tokenizer()

    for filename in all_files:
        input_file_path = input_directory_path + '/' + filename
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read().replace('\n', ' ')
            cleaned_text = tokenizer.clean_text(text)
            output_file_path = output_directory_path + '/' + filename

            text_file = open(output_file_path, "w")
            text_file.write(' '.join(cleaned_text))
            text_file.close()

            print('Done %s' % filename)

    print('Done')


if __name__ == '__main__':
    #crawler = WebCrawler()
    #crawler.download_pages()
    Tokenizer.extract_text()
    tokenize()
