import re
from os.path import dirname, join

import numpy as np
from os import listdir
import spacy
from nltk.tokenize import word_tokenize
from scipy.spatial import distance


class VectorSearch:

    def __init__(self):
        self.index_file_name = join(dirname(__file__), 'index.txt')
        self.tf_idf_folder_name = join(dirname(__file__), 'lemmas_tf_idf')
        self.links = dict()
        self.lemmas = []
        self.matrix = None
        self.nlp = spacy.load("ru_core_news_sm")
        self.__load_article_links()
        self.__load_lemmas()
        self.__load_tf_idf()

    def search(self, query: str) -> list:
        vector = self.__vectorize(query)
        similarities = dict()
        i = 1
        for row in self.matrix:
            dist = 1 - distance.cosine(vector, row)
            if dist > 0:
                similarities[i] = dist
            i += 1
        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        result = [(self.links[str(doc[0])], doc[1]) for doc in sorted_similarities]
        return result

    def __vectorize(self, query: str) -> np.ndarray:
        vector = np.zeros(len(self.lemmas))
        tokens = word_tokenize(query)
        for token in tokens:
            lemma = self.nlp(token)[0].lemma_
            if lemma in self.lemmas:
                vector[self.lemmas.index(lemma)] = 1
        return vector

    def __load_tf_idf(self):
        file_names = listdir(self.tf_idf_folder_name)
        self.matrix = np.zeros((len(file_names), len(self.lemmas)))
        for file_name in file_names:
            file_number = int(re.search('\\d+', file_name)[0])
            with open(self.tf_idf_folder_name + '/' + file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    lemma, idf, tf_idf = lines[i].split(' ')
                    self.matrix[file_number - 1][i] = float(tf_idf)

    def __load_lemmas(self):
        file_names = listdir(self.tf_idf_folder_name)
        for file_name in file_names:
            with open(self.tf_idf_folder_name + '/' + file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    self.lemmas.append(line.split(' ')[0])

    def __load_article_links(self):
        with open(self.index_file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.split(' ')
                self.links[key] = value


if __name__ == '__main__':
    search_engine = VectorSearch()
    results = search_engine.search("продержался почти три дня")
    for result in results:
        print(result)
