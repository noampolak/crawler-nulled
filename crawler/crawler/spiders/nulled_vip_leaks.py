import logging
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.python import to_unicode

from .. import settings

import random

user_agent_list = [
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    # 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    # 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

class NulledVipLeaksSpider(CrawlSpider):
    name = "NulledVipLeaksSpider"


    allowed_domains = [settings.DOMAIN]
    start_urls = [settings.BASE_URL]

    def __init__(self, *a, **kw):
        super(NulledVipLeaksSpider, self).__init__(*a, **kw)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                to_unicode(url),
                self.parse_links,
                cookies={
                    "nulledmember_id": 5417320,
                    "nulledpass_hash": "6f3ded8072218af80cf3ec77e4f05cb4",
                    "nulledsession_id": "36b94141227aeed9bc5d6fbeb07fc064",
                    # "User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"

                }
            )

    def parse_topics(self, response):
        url: str = response.url
        title = response.css(".maintitle").css("span::text").get()
        published_date = response.css(".post_date").css(".published::text").get()
        with open(f"output/page-{url.split('/')[-2]}.json", "w") as filee:
            filee.write('[')
            json.dump({
                'link': response.url,
                'title': title,
                'published time': published_date,
            }, filee) 
            filee.write(']')

    def parse_links(self, response, **kwargs):
        print(response.status)
        print(response.url)
        links = []
        topics = response.css(".topic_list").css(".topic_title")
        
        for topic in topics:
            links.append(topic.attrib["href"])

        # links = [link_block.css('a').attrib['href'] for link_block in response.css('.blog-entry-title')]
        logging.info(f"Number of links are {len(links)}")
        next_page_button = response.css('.topic_controls').css(".next a")
        next_page_url = next_page_button.attrib["href"]
        for link in links:
            yield response.follow(url=to_unicode(link), callback=self.parse_topics)
        if next_page_url is not None:
            yield response.follow(url=to_unicode(next_page_url), callback=self.parse_links)
        
    
