# API Key:  a359f7ab18185fe402ef345a0ddf5363cc13ca17
# Model_ID: cl_pi3C7JiL   
import argparse
import matplotlib
from monkeylearn import MonkeyLearn
import os
import re


# custom module calls
import v_scraper as vs

key = 'a359f7ab18185fe402ef345a0ddf5363cc13ca17'
model_id = 'cl_pi3C7JiL'   
ml = MonkeyLearn(key)
def process_words(words, key, model_id):
    if '\t' not in words:
        data = words
        #result = ml.classifiers.classify(model_id, data)
        print (result.body)
    return


def main():
    #this can be cleaned but it escapes me at 1AM
    parser = vs.setup_argparse()
    args = parser.parse_args()
    args = vars(args)
    url = vs.clean_url(args["url"])
    site = vs.find_site(url)
    main_links = vs.find_content(site)
    # reusing the find_site function because there's no reason to fix what
    # isn't broken right now.
    content_list = [vs.find_site(link) for link in main_links]
    articles = [vs.find_paras(article) for article in content_list]
    p_words = [process_words(words, key, model_id) for words in articles]


if __name__ == '__main__':
    main()