from asyncAction import get_final_data
import asyncio
import json
import pandas as pd
from time import perf_counter

dataPath = 'data/'

url = 'https://veiculos.fipe.org.br/api/veiculos//ConsultarTabelaDeReferencia'
data = {}

start = perf_counter()
results = asyncio.run(get_final_data(url, data))
parsed = json.loads(results.pop(-1))
# print(type(parsed))
tabelas = pd.DataFrame(parsed)
tabelas = tabelas
print(tabelas)

stop = perf_counter()
total = stop - start

print('It tooks {} seconds'.format(total))

