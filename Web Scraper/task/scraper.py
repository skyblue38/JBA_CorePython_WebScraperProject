# JBA CORE PYTHON COURSE
# Web Scraper project - https://hyperskill.org/projects/145
# Submitted by Chris Freeman - Stage 5 of 5 - 11JAN2023
import string
import os
import requests
from bs4 import BeautifulSoup


punct = string.punctuation  # + '—' + '’'  punctuation literals


def fname(title):
    fn = title.strip().split()  # break title into list of words
    nfn = '_'.join(fn).strip()  # reconnect words separated by '_' as new file name
    for i in punct:             # remove punctuation to form final file name
        if i in nfn and not i == '_':   # except for underscore
            nfn = nfn.replace(i, '')
    return nfn + '.txt'         # return new filename with txt suffix


n_pages = int(input())  # get number of pages to search
p_d = {}                # create that many page directories
for p in range(1, n_pages + 1):
    p_d[p] = 'Page_' + str(p)
    os.mkdir(p_d[p])
a_type = input()        # get article class
url_base = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
a_names = []        # list of News article filenames
# Get nature.com/nature pages 1 thru n_pages
for p in range(1, n_pages + 1):
    news_urls = []  # list of article URLs for this page
    request_url = url_base + str(p)
    response = requests.get(request_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    status = response.status_code
    if not status == 200:
        print(f'The URL returned {status}!')    # GET failed
    else:
        main_soup = BeautifulSoup(response.content, 'html.parser')  # parse the html page
        articles = main_soup.find_all('article')            # and find all "Articles"
        for a in articles:
            article_type = a.find('span', 'c-meta__type').text   # find <span class='c-meta__type'...>
            if article_type == a_type:                      # select articles where type = News
                news_urls.append('https://www.nature.com' + a.find('a').get('href'))  # save URL
        # print(news_urls)
        for n in news_urls:             # loop thru the News UTL list and GET each page
            n_r = requests.get(n, headers={'Accept-Language': 'en-US,en;q=0.5'})
            n_s = n_r.status_code
            if not n_s == 200:
                print(f'article URL {n} returns {n_s}')  # http GET failed ??
            else:
                a_soup = BeautifulSoup(n_r.content, 'html.parser')  # parse the News page
                a_t = a_soup.find('title').text  # find the page <title...>
                a_fname = fname(a_t)            # form a filename from the page title
                a_names.append(a_fname)         # and save to the list
                a_body = a_soup.find('div', 'c-article-body').text   # get the body contents
                a_page = a_body.encode(encoding='utf-8')
                # print('Writing:', a_names[-1])
                # print(a_page)
                with open(p_d[p] + '/' + a_fname, 'wb') as f:
                    f.write(a_page)             # and write it to a text file

print('Saved all articles.')       # notify end of web scraping operation
