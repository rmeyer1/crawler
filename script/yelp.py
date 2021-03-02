import json
import os

from requests import get

from datetime import datetime
import pandas as pd

from script.proxy import main
from settings import token
website = """
#########################################
#           WEBSITE: YELP.com          #
######################################### 
"""
print(website)
start_time = datetime.now()
print('Generating Yelp Data: starting time : {}'.format(start_time.time()))
print()

company_names = []
address = []
phone = []
rating = []
yelp_links = []
zip = []
company_site = main()


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

        for business in request['businesses']:
            company_names.append(business['name'])
            address.append(business['location']['display_address'])
            zip.append(business['location']['zip_code'])
            phone.append(business['display_phone'])
            rating.append(business['rating'])
            yelp_links.append(business['url'])

        index += 50

    save_to_xlxs()


def create_data_frame():
    print('Creating dataframe.')

    current_directory = get_project_root()
    BASE_DIR = os.path.dirname(current_directory)
    print(BASE_DIR)

    # Dataframe creation
    a = {'Name or Business Name': company_names, 'Display Address': address, 'Zipcode': zip, 'Phone Numbers': phone, 'Company Website': company_site, 'Yelp Rating': rating, 'Yelp Link': yelp_links,}
    df = pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    # df = pd.DataFrame({'Name or Business Name': company_names,
    #                    'Display Address': address,
    #                    'Zipcode': zip,
    #                    'Phone Numbers': phone,
    #                    'Company Website': company_site,
    #                    'Yelp Rating': rating,
    #                    'Yelp Link': yelp_links,
    #                    })

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('{base_dir}/datasets/yelp_data_{current_date}.xlsx'.format(base_dir=BASE_DIR, current_date=datetime.now()), engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Yelp Data')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    return df


def save_to_xlxs():
    print("Saving dataframe to xlxs file")
    df = create_data_frame()
    print(df)

def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))


get_request_data(index=0)
# make_request(index=0)