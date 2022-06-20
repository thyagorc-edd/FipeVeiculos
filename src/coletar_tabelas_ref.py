from numpy import append
import pandas as pd
import urllib3
import json
import requests
import os

dataPath = 'data/'

rtabelas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarTabelaDeReferencia')
res = rtabelas.content

df = json.dumps(rtabelas.json())
df = pd.read_json(df)

if os.path.exists(dataPath) == False:
    os.mkdir(dataPath)

df.to_csv(dataPath+'/dadosTabelas.csv', index=False, header=True)


tabelas = pd.read_csv(dataPath+'dadosTabelas.csv', nrows=10) ## nrows define o numero de linhas para leitura. Para testes, utilizaremos 10 linhas enquanto escrevemos o código

## tabelas será um DF com todas as tabelas para recuperar as marcas de todos os anos

dfComMarcas = pd.DataFrame()
for row in tabelas.index:
    
    codigoTabela = tabelas['Codigo'][row] # armazena o código da tabela da lista do DF
    Marcas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas',
            data = {
                'codigoTabelaReferencia':codigoTabela, ## esse código será variável por cada tabela da relação de tabelas
                'codigoTipoVeiculo':1
            }
            )
    df = json.dumps(Marcas.json())
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigoTabela
    
    dfComMarcas = pd.concat([dfComMarcas,df])
    print( f'gravando tabela {codigoTabela}' )

dfComMarcas = dfComMarcas.rename(columns={'Label':'nomeMarca','Value':'codigoMarca'})    
dfComMarcas.to_csv(dataPath+'/DatasetFinal.csv', index=False, header=True)

dfComMarcas = pd.DataFrame()