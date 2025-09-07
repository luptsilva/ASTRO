import requests
import time

import pandas as pd

from bs4 import BeautifulSoup

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_ned():
    pass

def get_hyperleda():
    pass


def main():
    # Site NASA -> https://ned.ipac.caltech.edu/
    # Site OSU Institut Pytheas -> http://atlas.obs-hp.fr/hyperleda/
    # Lib professor -> query

    # NASA (maxpath, ID)
    lon_deg = "allbyname.gal_lon"  # allbyname_11
    lat_deg = "allbyname.gal_lat"  # allbyname_12
    cz = "allbyname.v_Sun"  # allbyname_19
    cz_var = "allbyname.unc_v_Sun"  # allbyname_20
    mpc = "allbyname.mean_distance"  # allbyname_26
    mpc_sem = "allbyname.SEM_distance"  # allbyname_27
    # morphology = "allbyname.o_class_morph"  # allbyname_29

    # OSU (column text)
    lat_lon_deg = "Galactic (IAU1958)"
    v_r_column_name = "v"
    logd25_column_name = "logd25"
    logr25_column_name = "logr25"
    pa_column_name = "pa"
    rows_names = [v_r_column_name, logd25_column_name, logr25_column_name, pa_column_name]
    # type = "type"  # Mesma coisa que Morphology

    name = "2MASXJ01372378-0018422"

    encoded_name = quote(name)
    url = f"http://atlas.obs-hp.fr/hyperleda/ledacat.cgi?o={encoded_name}"

    response = requests.get(url, timeout=10)
    html = BeautifulSoup(response.text, 'html.parser')

    tables = html.find_all('table')
    table = tables[5]
    rows = table.find_all('tr')

    infos = {}
    for row in rows:
        columns = row.find_all('td')

        for row_name in rows_names:
            if columns and columns[0].text.strip() == row_name:
                infos[row_name] = columns[1].text.strip()
                break

    print(infos)

    # df = pd.read_csv("tabelas/antigas/AMUSING_PRAM_sample7.csv")
    # df_names = df[["Name"]]
    # df_names.to_csv("galaxy_names.csv", index=False)
    pass



if __name__ == "__main__":
    main()