import requests, scrapy, datetime
from bs4 import BeautifulSoup


class TotaljobsSpider(scrapy.Spider):
    name = 'totaljobs'

    today = datetime.date.today()

    start_urls = [
        'https://totaljobs.com/jobs',

        'https://totaljobs.com/jobs/in-london',
        'https://totaljobs.com/jobs/in-bristol',
        'https://totaljobs.com/jobs/in-liverpool',
        'https://totaljobs.com/jobs/in-scotland',
        'https://totaljobs.com/jobs/in-glasgow',
        'https://totaljobs.com/jobs/in-leeds',
        'https://totaljobs.com/jobs/in-manchester',
        'https://totaljobs.com/jobs/in-birmingham',

        'https://totaljobs.com/jobs/r',
        'https://totaljobs.com/jobs/sql',
        'https://totaljobs.com/jobs/php',
        'https://totaljobs.com/jobs/aws',
        'https://totaljobs.com/jobs/java',
        'https://totaljobs.com/jobs/python',
        'https://totaljobs.com/jobs/engineer',
        'https://totaljobs.com/jobs/developer',
        'https://totaljobs.com/jobs/programmer'
    ]


    def parse_full_offer(self, offer_link):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        cookies = {"cookie":"0ceb2907-286a-47fb-8df4-b3ed2d7d6bd4"}
        response = requests.get(offer_link, headers=headers, cookies=cookies)
        html_full_offer = response.text
        full_offer_data = BeautifulSoup(html_full_offer, 'html.parser')
        position = full_offer_data.find('h1', 'brand-font').text.replace('\n', '').replace('\r','').replace('\t','').replace('  ','')

        try:
            location = full_offer_data.find('li', 'location').text.replace('\n','')
        except Exception as e:
            location = full_offer_data.find('div', 'travelTime-locationText').text.replace('\n', '')

        salary = full_offer_data.find('li', 'salary').text.replace('\n','')
        company = full_offer_data.find('li', 'company').text.replace('\n','').replace('\r', '').replace('  ','')
        date_posted = full_offer_data.find('li', 'date-posted').text.replace('\n','')
        
        if str(date_posted) == 'today' or str(date_posted) == 'Today':
            date_posted = str(self.today)

        elif str(date_posted) == 'Recently':
            date_posted = str(self.today)

        elif str(date_posted) == 'Yesterday':
            date_posted = str(self.today - datetime.timedelta(days = 1))

        elif str(date_posted) == 'Posted 2 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 2))

        elif str(date_posted) == 'Posted 3 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 3))

        elif str(date_posted) == 'Posted 4 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 4))

        elif str(date_posted) == 'Posted 5 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 5))

        elif str(date_posted) == 'Posted 6 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 6))

        elif str(date_posted) == 'Posted 7 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 7))

        elif str(date_posted) == 'Posted 8 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 8))

        elif str(date_posted) == 'Posted 9 days ago':
            date_posted = str(self.today - datetime.timedelta(days = 9))

        desc = full_offer_data.find('div', 'job-description').text.replace('\n','').replace('\r', '').replace('  ', '')

        extra_data = full_offer_data.find('ul', 'contact-reference hidden-xs')
        jobID = extra_data.find_all('li')[-1].text.split('ID:')[1].replace(' ','')

        result = {
            "offerID":str(str(jobID)+'_totaljobs').replace('\r','').replace('\t', '').replace('\n',''),
            "jobTitle": position,
            "salary":salary,
            "company":{
                "name":company,
                "location":location
            },
            "offerDescription":desc,
            "postingDate":date_posted,
            "offerLink":offer_link
        }

        return result


    def parse(self, response):

        for offer_html in response.css('div.job').getall():
            soup = BeautifulSoup(offer_html, 'html.parser')
            for offer in soup.find_all('div', 'job new'):
                offer_link = offer.find('div', 'job-title').find('a')['href']
                data = self.parse_full_offer(offer_link)
                yield data

        for page in response.css('.pagination'):
            next_page = page.css('::attr(href)').getall()
            if next_page[-1] is not None:
                next_page = response.urljoin(next_page[-1])
                yield scrapy.Request(next_page, callback=self.parse)

        return
