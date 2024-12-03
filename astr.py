# Editando arquivo

from astroquery.ipac.ned import Ned
import pandas as pd
from query import hyperleda
from astropy.coordinates import SkyCoord
from dustmaps.sfd import SFDQuery
import numpy as np

csv = pd.read_csv("Tabelas/AMUSING_PRAM_sample.csv")
fits = pd.read_csv('Tabelas/fits_to_csv_certo.csv') #arquivo só com a Reff
g = csv['Name']
c = pd.read_csv("Tabelas/AMUSING_PRAM_cubes.csv", index_col="Name")
c["Has_cube"] = True
m = pd.merge(c, csv, on="Name" ,how = "left")

#merge fits
fits.rename(columns={'Gal':'Name'}, inplace=True)
fits['Name'] = fits['Name'].str.strip()
t = pd.merge(m, fits, on="Name" ,how = "left")

#tirando colunas vazias
t.replace(-999.0, np.nan, inplace=True)

for name in g:
    g_hyperleda = hyperleda.query_object(name , properties='all')
    g_ned = Ned.query_object(name)
    print(g_ned)
    print(g_hyperleda)

#calcula e(b-V)
coords = SkyCoord(t["RA_NED"], t["DEC_NED"], unit = "deg", frame='icrs')
sfd = SFDQuery()
ebv = sfd(coords)
t["E(B-V)"] = ebv

t.to_csv("Tabelas/AMUSING_PRAM_sampleTESTEAGORAVAI.csv", index=False)
#Name,has_cube,No,Bulge,Outskirts,RA_NED,DEC_NED,Morphology,deVac Morphology,V_r [km/s],D [Mpc],E(B-V),PA [degree],logd25,logr25,inc,PA,Reff