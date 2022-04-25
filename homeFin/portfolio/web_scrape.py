import requests, bs4, re 

class WebScrape:

    objects = []
    def __init__(self, url, header):
        self.url = url
        self.response = requests.get(self.url, headers = header)
        self.objects.append(self)
        self.scraper = bs4.BeautifulSoup(self.response.text, features="html.parser")



