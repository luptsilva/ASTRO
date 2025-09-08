# 🌌 Novas técnicas de síntese espectral espacialmente resolvida

**Autora:** Luiza Pinheiro da Silva  
**Período de produção:** 01/09/2024 - 30/08/2025  

---

## Descrição

Este projeto realiza a **coleta, organização e unificação de informações astronômicas sobre galáxias** a partir de diferentes fontes públicas:

- **HyperLeda**
  - via *scraping* em HTML  
  - via biblioteca `query`
- **NED (NASA/IPAC Extragalactic Database)**
  - via *scraping* dinâmico com Selenium  
  - via `astroquery`

O resultado é um conjunto de arquivos CSV com as informações de cada fonte e um **arquivo final mesclado** (`galaxy_infos_merged.csv`) consolidando os dados segundo prioridades definidas.

---

## Informações coletadas

As propriedades das galáxias extraídas (quando disponíveis) incluem:

- **Posição em coordenadas galácticas** (`lon`, `lat`)
- **Velocidade radial** (`V_r [Km/s]`)
- **Parâmetros morfológicos**:
  - `logd25` → tamanho do eixo maior (log)
  - `logr25` → razão de eixos (log)
  - `PA [Degree]` → ângulo de posição
- **Distância estimada** em megaparsecs (`d [Mpc]`)

---

## Estrutura do Projeto

```bash
ASTRO/
│── query/ # Biblioteca auxiliar (query HyperLeda)
│── tabelas/ # Tabelas geradas
│ ├── galaxy.csv # Lista inicial de galáxias
│ ├── galaxy_infos_hyperleda.csv
│ ├── galaxy_infos_query_hyperleda.csv
│ ├── galaxy_infos_ned.csv
│ ├── galaxy_infos_query_ned.csv
│ └── galaxy_infos_merged.csv # Arquivo final mesclado
│
│── main.py # Script principal
│── requirements.txt # Dependências do projeto
│── README.md # Este arquivo
```

## Funcionamento

### 1. Entrada
O script lê a lista de nomes de galáxias a partir de:

```bash
tabelas/galaxy.csv
```

## 2. Coleta
Para cada galáxia, o script busca informações em **quatro fontes**:

1. Scraping direto do **HyperLeda**  
2. Biblioteca `query` do **HyperLeda**  
3. Scraping via **Selenium** no **NED**  
4. Consulta via **astroquery** no **NED**

### 3. Unificação
Os arquivos individuais são mesclados no arquivo:

```bash
tabelas/galaxy_infos_merged.csv
```

## Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/luptsilva/ASTRO.git
cd ASTRO
```

### Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Instale as dependências

```bash
pip install -r requirements.txt
```

### Execute o script

```bash
python main.py
```

## Saídas

O script gera automaticamente os seguintes arquivos CSV na pasta tabelas/:

- `galaxy_infos_hyperleda.csv` → informações via scraping HyperLeda
- `galaxy_infos_query_hyperleda.csv` → informações via biblioteca HyperLeda
- `galaxy_infos_ned.csv` → informações via scraping NED
- `galaxy_infos_query_ned.csv` → informações via astroquery NED
- `galaxy_infos_merged.csv` → arquivo final mesclado

## Tecnologias utilizadas

- `Python 3.10+`

- Bibliotecas principais:
    - `requests`, `beautifulsoup4`
    - `selenium`
    - `pandas`
    - `astropy`, `astroquery`
    - `query` (biblioteca auxiliar fornecida)

## Observações

- O scraping do NED depende do Selenium + ChromeDriver configurado.
- O tempo de execução pode ser relativamente longo dependendo da lista de galáxias.
- Algumas informações podem não estar disponíveis em todas as fontes, resultando em valores NaN no CSV final.

