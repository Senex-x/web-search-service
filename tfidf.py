import re
from os.path import dirname, join
import spacy
from os import listdir, path
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
from collections import Counter
from math import log10


class FrequencyCounter:
    def __init__(self):
        self.pages_folder_name = join(dirname(__file__), 'pages')
        self.tokens_file_name = join(dirname(__file__), 'tokens.txt')
        self.lemmas_file_name = join(dirname(__file__), 'lemmas.txt')
        self.spacy = spacy.load("ru_core_news_sm")
        self.tokens = set()
        self.lemmas = set()
        self.__read_tokens()
        self.__read_lemmas()
        self.pages = []
        self.counters = []
        self.file_names = []

    def calculate_tf_idf_for_words(self):
        self.__get_words_data()
        self.__calculate_tf_idf(self.tokens, 'words_tf_idf')

    def calculate_tf_idf_for_lemmas(self):
        self.__get_lemmas_data()
        self.__calculate_tf_idf(self.lemmas, 'lemmas_tf_idf')

    def __calculate_tf_idf(self, words, directory_to_save):
        tf = self.__get_tf(words)
        idf = self.__get_idf(len(self.pages), words)
        tf_idf = self.__get_tf_idf(tf, idf, words)
        for page_tf_idf, file_name in zip(tf_idf, self.file_names):
            path_to_save = join(path.dirname(__file__), f'{directory_to_save}/{file_name}.txt')
            with open(path_to_save, 'w+', encoding='utf-8') as file:
                for word in words:
                    file.write(f'{word} {idf[word]} {page_tf_idf[word]}\n')

    def __read_tokens(self):
        file = open(self.tokens_file_name, 'r')
        lines = file.readlines()
        for line in lines:
            self.tokens.add(line.strip())
        file.close()

    def __read_lemmas(self):
        file = open(self.lemmas_file_name, 'r')
        lines = file.readlines()
        for line in lines:
            words = re.split('\\s+', line)
            lemma = words[0][:len(words[0]) - 1]
            self.lemmas.add(lemma)
        file.close()

    def __get_words_data(self):
        self.pages = []
        self.counters = []
        self.file_names = []
        for file_name in listdir(self.pages_folder_name):
            file = open(join(self.pages_folder_name, file_name), 'r', encoding='utf-8')
            self.file_names.append(re.search('\\d+', file_name)[0])
            text = BeautifulSoup(file, features='html.parser').get_text()
            list_of_words = wordpunct_tokenize(text)
            tokens = []
            for word in list_of_words:
                if word in self.tokens:
                    tokens.append(word)
            self.pages.append(tokens)
            self.counters.append(Counter(tokens))
            file.close()

    def __get_lemmas_data(self):
        self.pages = []
        self.counters = []
        self.file_names = []
        for file_name in listdir(self.pages_folder_name):
            file = open(join(self.pages_folder_name, file_name), 'r', encoding='utf-8')
            self.file_names.append(re.search('\\d+', file_name)[0])
            text = BeautifulSoup(file, features='html.parser').get_text()
            doc = self.spacy(text)
            lemmas = []
            for token in doc:
                lemma = token.lemma_
                if lemma in self.lemmas:
                    lemmas.append(lemma)
            self.pages.append(lemmas)
            self.counters.append(Counter(lemmas))
            file.close()

    def __get_tf(self, word_in: set) -> list:
        pages_tf = []
        for page, counter in zip(self.pages, self.counters):
            count = len(page)
            tf = {}
            for word in word_in:
                tf[word] = counter[word] / count
            pages_tf.append(tf)
        return pages_tf

    def __get_idf(self, count_of_pages: int, word_in: set) -> dict:
        counters = dict.fromkeys(word_in, 0)
        for p_counter in self.counters:
            for word in word_in:
                if p_counter[word] != 0:
                    counters[word] += 1
        idf = {}
        for word in word_in:
            idf[word] = log10(count_of_pages / counters[word]) if counters[word] != 0 else 0
        return idf

    @staticmethod
    def __get_tf_idf(tf: list, idf: dict, word_in: set) -> list:
        idf_tf = []
        for tf_count in tf:
            idf_tf_dict = {}
            for word in word_in:
                idf_tf_dict[word] = tf_count[word] * idf[word]
            idf_tf.append(idf_tf_dict)
        return idf_tf


if __name__ == '__main__':
    frequencyCounter = FrequencyCounter()
    frequencyCounter.calculate_tf_idf_for_words()
    frequencyCounter.calculate_tf_idf_for_lemmas()
