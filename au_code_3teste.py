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


def get_object_coordinates(name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"https://ned.ipac.caltech.edu/byname?objname={name}"
        print(url)

        driver.get(f"https://ned.ipac.caltech.edu/byname?objname={name}")

        time.sleep(10)

        wait = WebDriverWait(driver, 20)
        ra_element = wait.until(EC.presence_of_element_located((By.ID, "allbyname_5")))
        dec_element = wait.until(EC.presence_of_element_located((By.ID, "allbyname_6")))

        ra = ra_element.text
        dec = dec_element.text
        return ra, dec

    except Exception as e:
        print(f"Erro ao tentar obter as coordenadas: {e}")
        return None, None

    finally:
        driver.quit()


csv = pd.read_csv("AMUSING_PRAM_sample7.csv")

names = list(csv["Name"])

for i, name in enumerate(names):
    print()
    print("Analisando a galaxia", name)
    try:
        ra_ned_column_name = "RA_NED"
        dec_ned_column_name = "DEC_NED"
        v_r_column_name = "V_r [km/s]"
        logd25_column_name = "logd25"
        logr25_column_name = "logr25"
        pa_column_name = "PA [degree]"
        d_column_name = "D [Mpc]"

        encoded_name = quote(name)
        url = f"http://atlas.obs-hp.fr/hyperleda/ledacat.cgi?o={encoded_name}"
            
        print()
        print(url)
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table')
        table = tables[5]

        rows = table.find_all('tr')

        if pd.isna(csv.at[i, v_r_column_name]):
            print("Procurando a velocidade")

            for row in rows:
                columns = row.find_all('td')

                if columns and columns[0].text.strip() == "v":
                    v = columns[1].text.strip().split()[0]
                    break
            
            csv.at[i, v_r_column_name] = v
        else:
            print("Já tem a velocidade")

        if pd.isna(csv.at[i, dec_ned_column_name]) or pd.isna(csv.at[i, ra_ned_column_name]):
            print("Procurando as coordenadas")

            ra, dec = get_object_coordinates(encoded_name)

            csv.at[i, ra_ned_column_name] = ra
            csv.at[i, dec_ned_column_name] = dec
        else:
            print("Já tem as coordenadas")

        if pd.isna(csv.at[i, logd25_column_name]):
            print("Procurando o logd25")
            for row in rows:
                columns = row.find_all('td')

                if columns and columns[0].text.strip() == "logd25":
                    logd25 = columns[1].text.strip().split()[0]
                    break
            csv.at[i, logd25_column_name] = logd25
        else:
            print("Já tem o logd25")

        if pd.isna(csv.at[i, logr25_column_name]):
            print("Procurando o logr25")
            for row in rows:
                columns = row.find_all('td')

                if columns and columns[0].text.strip() == "logr25":
                    logr25 = columns[1].text.strip().split()[0]
                    break
            csv.at[i, logr25_column_name] = logr25
        else:
            print("Já tem o logr25")

        if pd.isna(csv.at[i, pa_column_name]):
            print("Procurando PA [degree]")
            for row in rows:
                columns = row.find_all('td')

                if columns and columns[0].text.strip() == "pa":
                    pa = columns[1].text.strip().split()[0]
                    break
            csv.at[i, pa_column_name] = pa
        else:
            print("Já tem o PA [degree]")

        if pd.isna(csv.at[i, d_column_name]):
            print("Procurando D [Mpc]")
            for row in rows:
                columns = row.find_all('td')

                if columns and columns[0].text.strip() == "modbest":
                    d0 = columns[1].text.strip().split()[0]
                    break
            d1 = float(d0)
            d = 10**((d1-25)/5)
            csv.at[i, d_column_name] = d
        else:
            print("Já tem D [Mpc]")
    
    except Exception as err:
        print("Deu problema nesta galaxia", name)
        print("Erro:", err)

csv.to_csv("AMUSING_PRAM_sample8.csv")
