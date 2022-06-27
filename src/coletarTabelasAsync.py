from webbrowser import get
from numpy import append
import pandas as pd
import urllib3
import json
import requests
import os
import time
import asyncio
import aiohttp

dataPath = 'data/'

rtabelas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarTabelaDeReferencia')
res = rtabelas.content
df = json.dumps(rtabelas.json())
df = pd.read_json(df)

if os.path.exists(dataPath) == False:
    os.mkdir(dataPath)

tabelas = df.head(2)
df.to_csv(dataPath+'/dadosTabelas.csv', index=False, header=True)


urlMarcas = 'https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas'
urlModelos = 'https://veiculos.fipe.org.br/api/veiculos//ConsultarModelos'

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())





