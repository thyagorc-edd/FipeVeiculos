from email.header import Header
import aiohttp
import asyncio
import pandas as pd
from time import perf_counter

dataPath = 'data/'

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def get_link(session, url, data):
    async with session.post(url, data=data) as r:
        return await r.text()

async def get_data(session, url, ids):
    tasks = []
    for id in ids:
        data = {
                'codigoTabelaReferencia':id, ## esse código será variável por cada tabela da relação de tabelas
                'codigoTipoVeiculo':1
            }
        task = asyncio.create_task( get_link( session, url, data))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def get_final_data(url, ids):
    async with aiohttp.ClientSession() as session:
        totaldata = await get_data(session, url, ids)
        return totaldata, ids

if __name__ == '__main__':
    url = 'https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas'
    df = pd.read_csv(dataPath+'dadosTabelas.csv')
    lista_de_tabelas = df['Codigo'].values.tolist()
    ids = lista_de_tabelas
    
    start = perf_counter()
    results = asyncio.run(get_final_data(url, ids))
    dataList = list(data)

    df = pd.DataFrame(
    dataList, columns=['Name', 'M-cap', 'Internet Companies'])
    print(df)
    df=pd.DataFrame.from_records(results)
    df.to_csv('dadosAsync.csv',index=False, header=True)
    stop = perf_counter()
    print(stop - start)