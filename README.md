# crawler-nulled
The following crawler goes over **nulled.to/forum/15-other-leaks/** and download all the topics pages
It uses AutoThrottling to fool the website as much as it can so it won't be blocked

## setup:
Clone the repo \
`git clone git@github.com:noampolak/crawler-nulled.git` \
Install dependencies \
`poetry install` 

## usage:
Go to crawler folder \
`cd crawler` \
Run the crawler. \
`scrapy crawl NulledVipLeaksSpider` \
Or you can run in debug mode with vscode

## Settings:
You can change the settings in the settings.py file or change some of them via env variables.