import argparse
import bs4
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
    # If there are capital letters
    if find_caps:
        url = url.lower()
    # If there are spaces in the given argument
    if find_spaces:
        url = re.sub(r"\s*",'',url)
    if not find_http:
        print(url)
        url = 'https://' + url
        print(url)
    
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
    site = requests.get(url)
    status = site.status_code
    if status != 200:
        print('Error reaching ' + url + '...\n Exiting...')
        sys.exit()
    return


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    args = vars(args)
    url = clean_url(args["url"])
    find_site(url)


if __name__ == '__main__':
    main()