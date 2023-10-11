import scrapy
import pandas as pd

class HelloSpider(scrapy.Spider):
    name = 'Hellospider'
    start_urls = ['https://www.hellowork.com/fr-fr/emploi/recherche.html?l=Dijon+21000&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fcommune%2F21231&c=Alternance&p=1']

    def parse(self, response):
        for element in response.css('div.offer--maininfo'):
            yield {'compagnyName': element.css('span::text').get(),
                   'title': element.css('h3::text').get(),
                   'otherinfo': element.css('otherinfo::text').get(),
                   'publishDate': element.css('span::text').get()}



# les informations ne sont pas complètes dans ce scrapping de hellowork. 'cette entreprise souhaite rester anonyme'; informations qui revient sans cesse
# dans toutes les requêtes.