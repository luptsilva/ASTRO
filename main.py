"""
Projeto: Novas técnicas de síntese espectral espacialmente resolvida
Data de produção: 01/09/2024 - 30/08/2025
Autora: Luiza Pinheiro da Silva

Este script realiza a coleta e unificação de informações sobre 
galáxias a partir de diferentes fontes astronômicas:

-> HyperLeda (via scraping HTML e biblioteca query)
-> NED - NASA/IPAC Extragalactic Database (via scraping com Selenium e astroquery)


Os dados extraídos incluem:
- Posição em coordenadas galácticas (longitude lon e latitude lat)
- Velocidade radial (V_r [Km/s])
- Parâmetros morfológicos (logd25, logr25, PA [Degree])
- Distância estimada em megaparsecs (d [Mpc], quando disponível)

Após coletar as informações, o script gera arquivos CSV (Comma-Separeted Values) com os resultados
de cada método e um arquivo final mesclado (galaxy_infos_merged.csv) 
seguindo uma ordem de prioridade.
"""

import requests
import time

import pandas as pd

from bs4 import BeautifulSoup

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from query import hyperleda
from astroquery.ipac.ned import Ned
from astropy.coordinates import SkyCoord
import astropy.units as u


def get_infos_hyperleda(names):
    """
    Obtém informações de galáxias direto do site HyperLeda via scraping.

    Para cada galáxia, busca:
        - Velocidade radial (V_r [Km/s])
        - logd25 (tamanho do eixo maior)
        - logr25 (razão de eixos)
        - PA (ângulo de posição)
        - Coordenadas galácticas (lon, lat)

    Args:
        names (list[str]): Lista de nomes de galáxias.

    Output:
        Cria o arquivo CSV `tabelas/galaxy_infos_hyperleda.csv`.
    """
    # (column text)
    lat_lon_deg = "Galactic (IAU1958)"
    v_r_column_name = "v"
    logd25_column_name = "logd25"
    logr25_column_name = "logr25"
    pa_column_name = "pa"
    # type = "type"  # Mesma coisa que Morphology
    rows_names = [v_r_column_name, logd25_column_name, logr25_column_name, pa_column_name]

    all_infos = []

    for name in names:
        print("Buscando informações da galaxia " + name)

        encoded_name = quote(name)
        url = f"http://atlas.obs-hp.fr/hyperleda/ledacat.cgi?o={encoded_name}"

        response = requests.get(url, timeout=10)
        html = BeautifulSoup(response.text, 'html.parser')

        tables = html.find_all('table')
        table = tables[5]
        rows = table.find_all('tr')

        infos = {"Name": name}
        for row in rows:
            columns = row.find_all('td')

            for row_name in rows_names:
                if columns and columns[0].text.strip() == row_name:
                    # Ignorando as variações (+-) 
                    infos[row_name] = columns[1].text.strip().split()[0]
                    break
        
        # Agora vamos pegar a lat e a lon da tabela que está acima desta
        table = tables[3]
        rows = table.find_all('tr')

        for row in rows:
            columns = row.find_all('td')

            if columns and columns[0].text.strip() == lat_lon_deg:
                # O 1 ignora o G na frente
                infos["lon"] = columns[1].text.strip()[1:].replace("+", " ").replace("-", " -").split()[0]
                infos["lat"] = columns[1].text.strip()[1:].replace("+", " ").replace("-", " -").split()[1]
                break
        
        all_infos.append(infos)

    columns = ["Name"] + rows_names + ["lon", "lat"]
    df = pd.DataFrame(all_infos, columns=columns)
    df.to_csv("tabelas/galaxy_infos_hyperleda.csv", index=False)


def get_infos_ned(names):
    """
    Obtém informações de galáxias no site NED usando Selenium (scraping dinâmico).

    Para cada galáxia, busca:
        - Coordenadas galácticas (lon, lat)
        - Velocidade radial (V_r [Km/s])
        - Distância em Mpc (d [Mpc])

    Args:
        names (list[str]): Lista de nomes de galáxias.

    Output:
        Cria o arquivo CSV `tabelas/galaxy_infos_ned.csv`.
    """

    def get_info(driver, id):
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, id)))
            return element.text
        except Exception as e:
            print(f"Erro ao tentar obter informações: {e}")
            return None

    # NASA ID da tag
    lon_deg = "allbyname_11"
    lat_deg = "allbyname_12"
    cz = "allbyname_19"
    # cz_var = "allbyname_20"
    mpc = "allbyname_26"
    # mpc_sem = "allbyname_27"
    # morphology = "allbyname_29"
    id_to_name = {
        "allbyname_11": "lon",
        "allbyname_12": "lat",
        "allbyname_19": "v",
        # "allbyname_20": "cz_var",
        "allbyname_26": "mpc",
        # "allbyname_27": "mpc_sem",
    }
    ids = [lon_deg, lat_deg, cz, mpc]
    all_infos = []

    for name in names:
        print("Buscando informações da galaxia " + name)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://ned.ipac.caltech.edu/byname?objname={name}")
        time.sleep(10) # Necessário para dar tempo da tabela atualizar

        infos = {"Name": name}
        for id in ids:
            infos[id_to_name[id]] = get_info(driver, id)

        all_infos.append(infos)
    
    columns = ["Name"] + list(id_to_name.values())
    df = pd.DataFrame(all_infos, columns=columns)
    df.to_csv("tabelas/galaxy_infos_ned.csv", index=False)

def get_infos_query_hyperleda(names):
    """
    Obtém informações de galáxias do HyperLeda via biblioteca `query`.

    Para cada galáxia, busca:
        - Coordenadas galácticas (lon, lat)
        - Velocidade radial (V_r [Km/s])
        - logd25, logr25, PA [Degree]

    Args:
        names (list[str]): Lista de nomes de galáxias.

    Output:
        Cria o arquivo CSV `tabelas/galaxy_infos_query_hyperleda.csv`.
    """

    all_infos = []
    for name in names:
        print("Buscando informações da galaxia " + name)
        result_table = hyperleda.query_object(name , properties='l2, b2, v, logd25, logr25, pa')[0]
        infos = {
            "Name": name,
            "lon": result_table["l2"],
            "lat": result_table["b2"],
            "v": result_table["v"],
            "logd25": result_table["logd25"],
            "logr25": result_table["logr25"],
            "pa": result_table["pa"]
        }
        all_infos.append(infos)
    
    columns = ["Name", "lon", "lat", "v", "logd25", "logr25", "pa"]
    df = pd.DataFrame(all_infos, columns=columns)
    df.to_csv("tabelas/galaxy_infos_query_hyperleda.csv", index=False)


def get_infos_query_ned(names):
    """
    Obtém informações de galáxias do NED via `astroquery`.

    Para cada galáxia:
        - Consulta RA/DEC no NED
        - Converte RA/DEC para coordenadas galácticas (lon, lat)
        - Obtém velocidade radial (v)

    Args:
        names (list[str]): Lista de nomes de galáxias.

    Output:
        Cria o arquivo CSV `tabelas/galaxy_infos_query_ned.csv`.
    """
    all_infos = []

    for name in names:
        print("Buscando informações da galaxia " + name)
        result_table = Ned.query_object(name)

        ra = result_table["RA"][0]
        dec = result_table["DEC"][0]

        # Converte RA/DEC -> coordenadas galácticas
        coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs")
        lon = coord.galactic.l.deg
        lat = coord.galactic.b.deg

        infos = {
            "Name": name,
            "lon": lon,
            "lat": lat,
            "v": result_table["Velocity"][0],
        }
        all_infos.append(infos)

    # exporta pra CSV
    columns = ["Name", "lon", "lat", "v"]
    df = pd.DataFrame(all_infos, columns=columns)
    df.to_csv("tabelas/galaxy_infos_query_ned.csv", index=False)


def merge_tables_with_priority(file_paths, final_columns, output_path="galaxy_infos_merged.csv"):
    """
    Mescla várias tabelas de informações de galáxias com base em prioridade.

    As tabelas são processadas na ordem fornecida em `file_paths`. 
    Para galáxias duplicadas, mantém-se a primeira ocorrência (maior prioridade).

    Args:
        file_paths (list[str]): Lista de caminhos para arquivos CSV em ordem de prioridade.
        final_columns (list[str]): Lista de colunas desejadas no resultado final.
        output_path (str, optional): Caminho do arquivo CSV de saída. Default: "galaxy_infos_merged.csv".

    Returns:
        pd.DataFrame: DataFrame resultante com as informações mescladas.
    """
    dfs = []
    for path in file_paths:
        df = pd.read_csv(path)
        # Garante que todas as colunas existam
        for col in final_columns:
            if col not in df.columns:
                df[col] = None
        dfs.append(df[final_columns])
    
    # Concatena na ordem de prioridade
    merged = pd.concat(dfs)
    
    # Resolve duplicatas mantendo a primeira ocorrência (maior prioridade)
    merged = merged.groupby("Name", as_index=False).first()
    
    # Salva o csv
    merged.to_csv(output_path, index=False)
    
    return merged


def main():
    """
    Função principal do script:

        1. Lê lista de galáxias de `tabelas/galaxy.csv`.
        2. Obtém informações via:
            - Scraping do HyperLeda
            - Biblioteca `query` do HyperLeda
            - Scraping do NED
            - Biblioteca `astroquery` do NED
        3. Mescla os resultados em `tabelas/galaxy_infos_merged.csv`,
           respeitando a ordem de prioridade.

    Output:
        Imprime as primeiras linhas do DataFrame final.
    """
    # Site NASA -> https://ned.ipac.caltech.edu/
    # Site OSU Institut Pytheas -> http://atlas.obs-hp.fr/hyperleda/
    # Lib professor -> query
    # tem a astroquery.ned mas está em desuso
    # Lib minha -> astroquey.ipac.ned

    galaxy_names = pd.read_csv("tabelas/galaxy.csv")
    names = list(galaxy_names["Name"])

    get_infos_hyperleda(names)
    get_infos_query_hyperleda(names)

    get_infos_ned(names)
    get_infos_query_ned(names)

    file_paths = [
        # Lista de prioridade
        "tabelas/galaxy_infos_query_hyperleda.csv",  # 1
        "tabelas/galaxy_infos_hyperleda.csv",        # 2
        "tabelas/galaxy_infos_ned.csv",              # 3
        "tabelas/galaxy_infos_query_ned.csv"         # 4
    ]
    
    final_columns = ["Name", "lon", "lat", "v", "logd25", "logr25", "pa", "mpc"]
    merge_tables_with_priority(file_paths, final_columns, "tabelas/galaxy_infos_merged.csv")


if __name__ == "__main__":
    main()
