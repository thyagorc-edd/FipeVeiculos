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

tabelas = df.head(10)
#df.to_csv(dataPath+'/dadosTabelas.csv', index=False, header=True)


#tabelas = pd.read_csv(dataPath+'dadosTabelas.csv', nrows=10) ## nrows define o numero de linhas para leitura. Para testes, utilizaremos 10 linhas enquanto escrevemos o código
## tabelas será um DF com todas as tabelas para recuperar as marcas de todos os anos


dfComMarcas = pd.DataFrame() # iniciando um dataframe vazio para gravar as marcas
for row in tabelas.index:
    
    codigoTabelaMarca = tabelas['Codigo'][row] # armazena o código da tabela da lista do DF
    Marcas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas',
            data = {
                'codigoTabelaReferencia':codigoTabelaMarca, ## esse código será variável por cada tabela da relação de tabelas
                'codigoTipoVeiculo':1
            }
            )
    df = json.dumps(Marcas.json())
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigoTabelaMarca
    dfComMarcas = pd.concat([dfComMarcas,df])
    print( f'gravando tabela {codigoTabelaMarca} ' )


dfComMarcas = dfComMarcas.rename(columns={'Label':'nomeMarca','Value':'codigoMarca'})


dfComModelos = pd.DataFrame() # iniciando um dataframe vazio para gravar os modelos
for row in dfComMarcas.index:

    codigoTabelaModelo = dfComMarcas['tabelaReferencia'][row]
    codigoMarca  = dfComMarcas['codigoMarca'][row]

    modelos = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarModelos',
            data = {
                'codigoTipoVeiculo': 1,
                'codigoTabelaReferencia': codigoTabelaModelo, ## esse código será variável por cada tabela da relação de tabelas
                'codigoMarca':codigoMarca, ## esse código será variável por cada marca na relação de marcas
            }
            )
    
    df = json.dumps(modelos.json()['Modelos'])
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigoTabelaModelo
    df['codigoMarca'] = codigoMarca
    dfComModelos = pd.concat([dfComModelos,df])
    print( f'gravando tabela {codigoTabelaModelo} e marca {codigoMarca}' )


dfComModelos = dfComModelos.rename(columns={'Label':'nomeModelo','Value':'codigoModelo'})   
dfComModelos.to_csv(dataPath+'/DatasetFinal.csv', index=False, header=True)