import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class Crawler:
    def __init__(self):
        self.base_url = 'https://4pda.to'
        self.request_urls = [
            'https://4pda.to/tag/smartphones/',
            'https://4pda.to/tag/laptops/',
            'https://4pda.to/tag/pc/',
            'https://4pda.to/tag/audio/',
            'https://4pda.to/tag/monitors/'
        ]
        self.rel_attribute = 'bookmark'
        self.pages_folder_name = os.path.dirname(__file__) + '/pages'
        self.index_file_name = os.path.dirname(__file__) + '/index.txt'
        self.session = requests.Session()

        if not os.path.exists(self.pages_folder_name):
            os.mkdir(self.pages_folder_name)

    def download_pages(self, count: int = 100):
        all_links = list(self.find_pages())
        index_file = open(self.index_file_name, 'w', encoding='utf-8')
        file_counter = 1
        for link in all_links:
            if file_counter <= count:
                text = self.get_text_from_page(link)
                if text is None:
                    continue
                else:
                    page_name = f'{self.pages_folder_name}/page_{file_counter}.html'
                    with open(page_name, 'w', encoding='utf-8') as page:
                        page.write(text)
                    index_file.write(f'{file_counter} {link}\n')
                    file_counter += 1
            else:
                break
        index_file.close()

    def find_pages(self):
        all_links = []
        for request_url in self.request_urls:
            page = urllib.request.urlopen(request_url)
            soup = BeautifulSoup(page, 'html.parser')
            links = []
            for link in soup.findAll('a', {'rel': self.rel_attribute}, href=True):
                if link.get('href')[0] == 'h':
                    link = urllib.parse.urljoin(self.base_url, link.get('href'))
                    links.append(link)
            all_links.extend(links)

        return all_links

    def get_text_from_page(self, url):
        request = self.session.get(url)
        request.encoding = request.apparent_encoding
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            bad_tags = ['style', 'link', 'script']
            for tag in soup.find_all(bad_tags):
                tag.extract()
            return str(soup)
        return None


if __name__ == '__main__':
    crawler = Crawler()
    crawler.download_pages()