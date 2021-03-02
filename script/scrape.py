import json
import os
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
from requests import get

from datetime import datetime
import pandas as pd
from settings import token

website = """
#########################################
#           WEBSITE: YELP.com          #
######################################### 
"""
print(website)
start_time = datetime.now()
print('Scraping Yelp for Doctors direct website. starting time : {}'.format(start_time.time()))
print()

links = []
websites = []


def make_request(index):
    url = 'https://api.yelp.com/v3/businesses/search?location=DC&categories=obgyn&term=Doctor&limit=50&offset={i}'.format(
        i=index)
    headers = {
        "Authorization": "Bearer {token}".format(token=token)}
    response = get(url, headers=headers)
    print(response.json())
    d = json.loads(response.text)
    return d


def get_request_data(index):
    while index < 1000:
        request = make_request(index)

        for k in request['businesses']:
            if k['url']:
                links.append(k['url'])

        index += 50

    return links


# def scrape_yelp():
#     urls = get_request_data(index=0)
#     i = 0
#
#     for url in urls:
#         req = urllib.request.Request(
#             "{}".format(url),
#             data=None,
#             headers={
#                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
#             }
#         )
#         html = urlopen(req)
#         content = html.read()
#         soup = BeautifulSoup(content)
#         for a in soup.findAll('p', text="Business website"):
#             if a.nextSibling.text is not None:
#                 print("Now on index: {i} ".format(i=i) + a.nextSibling.text)
#                 i += 1
#                 websites.append(a.nextSibling.text)
#                 break
#
#         else:
#             print("Now on index: {i} No company website detected on Yelp.".format(i=i))
#             i += 1
#             websites.append("n/a")
#
#     print(websites)
#     return websites


# scrape_yelp()
# def create_data_frame():
#     print('Creating dataframe.')
#
#     current_directory = get_project_root()
#     BASE_DIR = os.path.dirname(current_directory)
#     print(BASE_DIR)
#
#     # Dataframe creation
#     df = pd.DataFrame({'company names': company_names,
#                        'addresses': address,
#                        'phone numbers': phone,
#                        'rating': rating,
#                        'company website': company_links,
#                        })
#
#     # Create a Pandas Excel writer using XlsxWriter as the engine.
#     writer = pd.ExcelWriter(
#         '{base_dir}/datasets/yelp_data_{current_date}.xlsx'.format(base_dir=BASE_DIR, current_date=datetime.now()),
#         engine='xlsxwriter')
#
#     # Convert the dataframe to an XlsxWriter Excel object.
#     df.to_excel(writer, sheet_name='Yelp Data')
#
#     # Close the Pandas Excel writer and output the Excel file.
#     writer.save()
#
#     return df
#
#
# def save_to_xlxs():
#     print("Saving dataframe to xlxs file")
#     df = create_data_frame()
#     print(df)


def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))


# get_request_data(index=0)
# make_request(index=0)
