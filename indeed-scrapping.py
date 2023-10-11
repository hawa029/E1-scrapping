import scrapy

class InddedSpider(scrapy.Spider):
    name = 'IndeedSpider'
    start_urls = ['https://fr.indeed.com/jobs?q=alternance&l=Dijon+%2821%29&from=searchOnHP&vjk=ea7ad82f11da0aed']

    def parse(self, response):
        for element in response.css('div.slider_item'):
            yield {'Company': element.css('span.companyName::text').get(),
                   'Title': element.css('h2.jobTitle-newJob::text').get(),
                   'Description': element.css('div.job-snippet ul li::text').get(),
                   'PublishDate': element.css('span.date::text').get()}


