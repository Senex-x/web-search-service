import os

import nltk
nltk.download('punkt')
nltk.download('stopwords')
import re

from bs4 import Comment, BeautifulSoup
from nltk.corpus import stopwords
from pymystem3 import Mystem


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

class Tokenizer:

    def clean_text(self, text):
        tokens = self.__tokenize(text)
        tokens = self.__lemmatize(tokens)
        tokens = self.__remove_stop_words(tokens)

        return tokens

    @staticmethod
    def extract_text():
        pages_folder_name = os.path.dirname(__file__) + '/pages'
        texts_folder_name = os.path.dirname(__file__) + '/texts'

        if not os.path.exists(texts_folder_name):
            os.mkdir(texts_folder_name)

        for file_counter in range(1, 101):
            page_name = f'{pages_folder_name}/page_{file_counter}.html'
            text_name = f'{texts_folder_name}/text_{file_counter}.txt'

            with open(page_name, 'r', encoding='utf-8') as page:
                html_text = page.read()

            soup = BeautifulSoup(html_text, 'html.parser')

            words_list = Tokenizer.__get_visible_words_list(soup)
            text = u" ".join(t.strip() for t in words_list)

            with open(text_name, 'w', encoding='utf-8') as page:
                page.write(text)

    @staticmethod
    def __get_visible_words_list(soup):
        """
        Проверяет количество слов на странице
        :return: True, если слов не меньше self.__min_words_count
        """
        texts = soup.findAll(text=True)
        visible_texts = list(filter(tag_visible, texts))
        return visible_texts

    @staticmethod
    def __tokenize(text):
        """ Делит текст на токены """
        tokens = nltk.word_tokenize(text)

        return tokens

    @staticmethod
    def __lemmatize(tokens):
        """ С помощью Mystem лемматизирует токены """
        mystem = Mystem()

        tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]

        return tokens

    @staticmethod
    def __remove_stop_words(tokens):
        """ Удаляет лишние символы """
        tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]

        stop_words = stopwords.words('russian')
        only_cyrillic_letters = re.compile('[а-яА-Я]')

        tokens = [token.lower() for token in tokens if (token not in stop_words)
                  and only_cyrillic_letters.match(token)
                  and not token.isdigit()
                  and token != '']

        return tokens
