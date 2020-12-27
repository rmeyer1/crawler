import os

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
print('Generating Yelp Data: starting time : {}'.format(start_time.time()))
print()

company_links = []
company_names = []
locations = []
phone = []
rating = []
address = []
index = 0


# We don't need this function right now because the yelp api can only handle 1000 results at a time.
# Will re-evalute in the future.
def get_total():
    url = 'https://api.yelp.com/v3/businesses/search?location=PHX&categories=Contractors&term=contractors&limit=50'
    headers = {
        "Authorization": "Bearer {token}".format(token=token)}
    response = get(url, headers=headers).json()
    print(response['total'])
    return response['total']


def make_request(index):
    url = 'https://api.yelp.com/v3/businesses/search?location=PHX&categories=Contractors&term=contractors&limit=50&offset={i}'.format(
        i=index)
    headers = {
        "Authorization": "Bearer {token}".format(token=token)}
    response = get(url, headers=headers)
    print(response.json())
    return response.json()


def get_request_data(index):
    while index < 1000:
        request = make_request(index)

        for business in request['businesses']:
            company_names.append(business['name'])
            address.append(business['location']['display_address'])
            phone.append(business['display_phone'])
            rating.append(business['rating'])
            company_links.append(business['url'])

        index += 50

    save_to_csv()


def create_data_frame():
    print('Creating dataframe.')

    # Dataframe creation
    df = pd.DataFrame({'company names': company_names,
                       'addresses': address,
                       'phone numbers': phone,
                       'rating': rating,
                       'company website': company_links,
                       })

    return df


def save_to_csv():
    print("Saving dataframe to csv file")
    current_directory = get_project_root()
    BASE_DIR = os.path.dirname(current_directory)
    print(BASE_DIR)
    csv_file = 'yelp_data_{}.csv'.format(datetime.now())
    df = create_data_frame()
    df.to_csv(r"{base_dir}/datasets/".format(base_dir=BASE_DIR) + csv_file)


def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))


get_request_data(index)
