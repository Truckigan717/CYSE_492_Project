import argparse
from bs4 import BeautifulSoup
import os
import requests
import re
import sys

def setup_argparse():
    '''
    sets up our method of parsing arguments recieved from the command line
    '''
    parser = argparse.ArgumentParser(
            prog='v_scraper', 
            description=(
            "this is Veritaz's scraper so we don't have to rely on "
            "wacky plugins that may not be available in an operational "
            "environement"
            )
    )
    parser.add_argument("url",
                        type=str,
                        help=("this is the name of the site "
                              "that we wish to scrape")
    )
    return parser


def clean_url(url):
    '''
    This cleans up our urls if they have any 'dirt' on them
    
    This will remove unnecessary capital letters, spaces or other unsightly
    characters that will limit our ability to make a request for the site.

    Args:
        url(str): the user-supplied url, such as news.google.com, etc
    Returns
        str: the cleaned url
    '''
    find_caps = re.search((r"[A-Z]+"), url)
    find_spaces = re.search((r"\s*"), url)
    find_http = re.search((r"^[http|https]://.*"), url)
    find_dot_com = re.search((r".*\.com"), url)
    # If there are capital letters
    if find_caps:
        url = url.lower()
    # If there are spaces in the given argument
    if find_spaces:
        url = re.sub(r"\s*",'',url)
    if not find_http:
        url = 'https://' + url
    if not find_dot_com:
        url = url + '.com'
    return url
    


def find_site(url):
    '''
    here we're gonna try to find the site that the user specified
    after we've cleaned it

    Args:
        url(str): url that we cleaned and can now use with requests

    Return:
        list
    '''
    if re.search('(http://|https://)\w+', url):
        site = requests.get(url)
        status = site.status_code
        print(status)
        if status != 200:
            print('Error reaching ' + url + '...\n Exiting...')
            return
        else:
            return site.content

def find_content(site):
    '''
    Finds content from the target site to get links and titles
    Args"
        site:
            this is the 'content', or bytes object that we used requests to get in
            find_site().
    Returns:
        list
    '''
    soup = BeautifulSoup(site, 'html.parser')
    links = soup.find_all('ul', href=True)
    # BeautifulSoup has some weird quirks that I don't fully understand as of
    # right now, but it gets the job done and is still the best tool for the
    # job.
    links = [
        'http:' + link['href'] for link in links if 'http' not in link['href']
    ]
    links = [link for link in links if link.endswith('.html')]
    # Okay, now we have all the links from the home site and maybe some more...
    # now to go to the sites and grab all that we can, a real smash and grab 
    # if you will
    return links


def find_paras(article):
    '''
    grab these articles' paragraphs so we can use monkey learn on them.
    Args:
        article(str):
            a piece of reporting that we can grab the text from and determine
            the articles purpose and feelings towards a subject using 
            monkeylearn, a basic sentiment analyzer.
    '''
    soup = BeautifulSoup(article, 'html.parser')
    paras = soup.find_all('p')
    # have to remove newlines and tabs and other white space so it's easier to 
    # parse moving forward.
    paras = [re.sub('\n*|\t*','', p.text) for p in paras]
    if re.search(r'LLC', paras[0]):
        return
    print(p[1:][1:-2])
    return paras

# this is for testing the program. currently works very well on Fox news.
def main():
    parser = setup_argparse()
    args = parser.parse_args()
    args = vars(args)
    url = clean_url(args["url"])
    site = find_site(url)
    main_links = find_content(site)
    # reusing the find_site function because there's no reason to fix what
    # isn't broken right now.
    content_list = [find_site(link) for link in main_links]
    words = [find_paras(article) for article in content_list]



if __name__ == '__main__':
    main()