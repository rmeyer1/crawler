
import io
import os
import re
from datetime import datetime

from selenium import webdriver

from time import sleep
import pandas as pd
from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

npxg = []
npxG_Sh = []
np_G_xG = []
prog = []
sca90 = []
gca90 = []
poss = []


def wait_until_element_is_present_by_id(driver, element):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, element)))

    except:
        print('could not locate element %s' % (element))


def get_by_type(locator_type):
    """
        def which generate locator type
        :param locator_type: str set by def which implement on SeleniumDriver class
        :return: tag type or False
        """
    locator_type = locator_type.lower()
    if locator_type == 'id':
        return By.ID
    elif locator_type == 'name':
        return By.NAME
    elif locator_type == 'xpath':
        return By.XPATH
    elif locator_type == 'css':
        return By.CSS_SELECTOR
    elif locator_type == 'class':
        return By.CLASS_NAME
    elif locator_type == 'link':
        return By.LINK_TEXT
    elif locator_type == 'tag':
        return By.TAG_NAME
    else:
        print("Locator type" + locator_type + " not correct/supported")
    return False


def set_firefox_options():
    try:
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

        return opts, profile

    except:
        raise Exception("Could not set firefox options for the browser. ")


def get_web_data():
    try:

        opts, profile = set_firefox_options()
        driver = webdriver.Firefox(profile, executable_path="/usr/local/bin/geckodriver", options=opts)

        driver.get("https://fbref.com/en/comps/11/Serie-A-Stats")

        data_frames = create_data_frame_object(driver)

        write_table_data_to_csv(data_frames)

    except:
        raise Exception("Could not get Web Data")


def get_table_data(driver, table_id, body_tag, row_tag):
    try:

        team_data = []

        wait_until_element_is_present_by_id(driver, table_id)

        table = driver.find_element(get_by_type('id'), table_id)

        sleep(randint(3, 5))

        body = table.find_element(get_by_type('tag'), body_tag)

        sleep(randint(2, 4))

        rows = body.find_elements(get_by_type('tag'), row_tag)

        for row in rows:
            row_class = row.get_attribute("class")

            if "Hellas Verona" in row.text:
                print(row.text)
                res_str = re.sub("Hellas Verona", "HellasVerona", row.text)
                print(res_str)
                team_data.append(res_str)

            # if "vs" in row.text:
            #     print(row.text)
            #     res_str = re.sub("vs ", "vs", row.text)
            #     print(res_str)
            #     team_data.append(res_str)

            elif row.text != "" and body_tag == 'tbody':
                print(row.text)
                team_data.append(row.text)

            elif body_tag == 'thead' and row_class != "over_header":
                res_str = re.sub("# Pl", "#Pl", row.text)
                print(res_str)
                team_data.append(res_str)

        length = len(team_data)
        if length > 1 and body_tag == 'thead':
            team_data.pop(0)
            return team_data

        return team_data

    except:
        raise Exception("Could not get table data from table %s " %(table_id))


def create_data_frame(table1, table2):
    try:
        all_data = pd.np.concatenate((table1, table2))
        df = pd.read_csv(io.StringIO('\n'.join(all_data)), delim_whitespace=True, error_bad_lines=False, engine="python")
        print(df)

        return df
    except:
        raise Exception("Could not create dataframe with table %s. " %(table1))


def create_data_frame_object(driver):
    try:
        tables = ["stats_shooting_squads", "stats_passing_squads", "stats_gca_squads", "stats_possession_squads"]

        button_ids = ['stats_shooting_squads_per_match_toggle', "stats_passing_squads_per_match_toggle", "stats_gca_squads_per_match_toggle", "stats_possession_squads_per_match_toggle"]

        data_frames = []

        for i in range(len(tables)):
            sleep(randint(1, 3))
            is_true = False

            while not is_true:
                driver.refresh()

                toggle_button = driver.find_elements_by_xpath('//*[@id="{}"]'.format(button_ids[i]))

                if toggle_button:
                    is_true = True

            assert toggle_button[0]

            toggle_button[0].click()

            headers = get_table_data(driver, "{}".format(tables[i]), "thead", "tr")

            data = get_table_data(driver, "{}".format(tables[i]), "tbody", "tr")

            df = create_data_frame(headers, data)

            data_frames.append(df)

        return data_frames

    except:
        raise Exception("Could not create dataframe Object. ")


def write_table_data_to_csv(data_frames):
    try:
        current_directory = get_project_root()
        BASE_DIR = os.path.dirname(current_directory)
        print(BASE_DIR)

        col_df = {
            'Squad': data_frames[0]['Squad'],
            'npxg': data_frames[0]['npxG'],
            'npxG/Sh': data_frames[0]['npxG/Sh'],
            'np:G-xG': data_frames[0]['np:G-xG'],
            'Prog': data_frames[1]['Prog'],
            'SCA90': data_frames[2]['SCA90'],
            'GCA90': data_frames[2]['GCA90'],
            'Poss': data_frames[3]['Poss']


        }
        df = pd.DataFrame(col_df)
        df.to_csv('{base_dir}/datasets/fbref_data_{current_date}.csv'.format(base_dir=BASE_DIR, current_date=datetime.now()), index = True)
    except:
        raise Exception("Could not write column df to CSV. ")


def get_project_root():
    print(os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.dirname(__file__))

get_web_data()