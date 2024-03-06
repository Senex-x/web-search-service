import re

import spacy
from os import path


class Query:
    def __init__(self, query: str, files: set):
        self.query = query
        self.files = files

    def __and__(self, other):
        return Query(f'({self.query} & {other.query})', self.files & other.files)

    def __or__(self, other):
        return Query(f'({self.query} | {other.query})', self.files | other.files)

    def __sub__(self, other):
        return Query(f'({self.query} ! {other.query})', self.files - other.files)


class BooleanSearch:
    def __init__(self):
        self.inverted_index_file_name = path.dirname(__file__) + '\\inverted_index.txt'
        self.spacy = spacy.load("ru_core_news_sm")
        self.index = dict()
        self.__read_inverted_index()

    def search(self, search_words):
        search_words = re.findall(r'\(|\)|&|\||!|\b\w+\b', search_words)
        query_result = self.__evaluate_query(search_words)
        if query_result:
            query_result = list(query_result.files)
            query_result.sort()
            return query_result
        else:
            return []

    def __read_inverted_index(self):
        file = open(self.inverted_index_file_name, 'r')
        lines = file.readlines()
        for line in lines:
            items = re.split('\\s+', line)
            token = items[0]
            files = set()
            for i in range(2, len(items) - 1):
                files.add(int(items[i]))
            self.index[token] = Query(token, files)
        file.close()

    def __evaluate_query(self, query_tokens):
        stack = []
        i = 0
        while i < len(query_tokens):
            if query_tokens[i] == '(':
                stack.append(query_tokens[i])
            elif query_tokens[i] == ')':
                finish = False
                while stack and stack[-1] != '(' and not finish:
                    stack.append(self.__process_operator(stack.pop(), stack.pop(), stack.pop() if stack else None))
                    finish = True
                if stack:
                    last_appended = stack.pop()
                    stack.pop()
                    stack.append(last_appended)
            elif query_tokens[i] in {'&', '|', '!'}:
                stack.append(query_tokens[i])
            else:
                lemma = self.spacy(query_tokens[i])[0].lemma_
                stack.append(self.index[lemma])

            i += 1

        while len(stack) > 1:
            stack.append(self.__process_operator(stack.pop(), stack.pop(), stack.pop() if stack else None))

        return stack[0]

    @staticmethod
    def __process_operator(operand1, operator, operand2):
        if operand2 is None:
            return operand1
        elif operator == '&':
            return operand1 & operand2
        elif operator == '|':
            return operand1 | operand2
        elif operator == '!':
            return operand1 - operand2


if __name__ == '__main__':
    boolean_search = BooleanSearch()

    queries = ['вебка & модель',
               'намерен | некий',
               'вебка & модель & (намерен | некий)']

    for query in queries:
        result = boolean_search.search(query)
        print(f"Result of the boolean search query: '{query}' is {result}")

