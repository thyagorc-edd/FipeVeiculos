#from numpy import append
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

tabelas = df
df.to_csv(dataPath+'/dadosTabelas.csv', index=False, header=True)



# dfComMarcas = pd.DataFrame() #iniciando um dataframe vazio para gravar as marcas
# for row in tabelas.index:
    
#     codigotabela = tabelas['Codigo'][row] #armazena o código da tabela da lista do DF
#     Marcas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas',
#             data = {
#                 'codigoTabelaReferencia':codigotabela, ## esse código será variável por cada tabela da relação de tabelas
#                 'codigoTipoVeiculo':1
#             }
#             )
#     df = json.dumps(Marcas.json())
#     df = pd.read_json(df)
#     df['tabelaReferencia'] = codigotabela
#     dfComMarcas = pd.concat([dfComMarcas,df])
#     print( f'gravando tabela {codigotabela} ' )


# dfComMarcas = dfComMarcas.rename(columns={'Label':'nomeMarca','Value':'codigoMarca'})
# dfComMarcas = dfComMarcas.loc[dfComMarcas['nomeMarca'] == 'Ford'].reset_index(drop=True) ### forçar apenas 10 registros para teste

print(tabelas)


url = 'https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas'
results = []


start = time.time()

def get_tasks(session):
    tasks = []
    for tabela in tabelas.index:
        
        codigo = tabelas['Codigo'][tabela]
        tasks.append(asyncio.create_task(session.post(url, data={ 'codigoTabelaReferencia':codigo, 
                                                                  'codigoTipoVeiculo':1})))
    return tasks

async def get_marcas():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
             results.append(await response.json())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_marcas())


#print(results)
end = time.time()
total_time = end - start
print("It took {} seconds to make {} API calls".format(total_time, tabelas.size))
print('You did it!')