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

tabelas = df.head(1)
df.to_csv(dataPath+'/dadosTabelas.csv', index=False, header=True)


#tabelas = pd.read_csv(dataPath+'dadosTabelas.csv', nrows=10) ## nrows define o numero de linhas para leitura. Para testes, utilizaremos 10 linhas enquanto escrevemos o código
## tabelas será um DF com todas as tabelas para recuperar as marcas de todos os anos


dfComMarcas = pd.DataFrame() # iniciando um dataframe vazio para gravar as marcas
for row in tabelas.index:
    
    codigotabela = tabelas['Codigo'][row] # armazena o código da tabela da lista do DF
    Marcas = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarMarcas',
            data = {
                'codigoTabelaReferencia':codigotabela, ## esse código será variável por cada tabela da relação de tabelas
                'codigoTipoVeiculo':1
            }
            )
    df = json.dumps(Marcas.json())
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigotabela
    dfComMarcas = pd.concat([dfComMarcas,df])
    print( f'gravando tabela {codigotabela} ' )


dfComMarcas = dfComMarcas.rename(columns={'Label':'nomeMarca','Value':'codigoMarca'})
dfComMarcas = dfComMarcas.loc[dfComMarcas['nomeMarca'] == 'Ford'].reset_index(drop=True) ### forçar apenas 10 registros para teste

print(dfComMarcas)

# ############################################################################################
# ## captura de informações dos modelos ###
# ############################################################################################
dfComModelos = pd.DataFrame() # iniciando um dataframe vazio para gravar os modelos
for row in dfComMarcas.index:

    codigotabela = dfComMarcas.reset_index(drop=True)['tabelaReferencia'][row]
    codigoMarca  = dfComMarcas.reset_index(drop=True)['codigoMarca'][row]
    nomeMarca  = dfComMarcas.reset_index(drop=True)['nomeMarca'][row]


    print(f' tabela {codigotabela} e marca {codigoMarca}')

    modelos = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarModelos',
            data = {
                'codigoTipoVeiculo': 1,
                'codigoTabelaReferencia': codigotabela, ## esse código será variável por cada tabela da relação de tabelas
                'codigoMarca':codigoMarca, ## esse código será variável por cada marca na relação de marcas
            }
            )
    
    df = json.dumps(modelos.json()['Modelos'])
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigotabela
    df['codigoMarca'] = codigoMarca
    df['nomeMarca']   = nomeMarca
    dfComModelos = pd.concat([dfComModelos,df])
    print( f'gravando tabela {codigotabela} e marca {codigoMarca}' )


dfComModelos = dfComModelos.rename(columns={'Label':'nomeModelo','Value':'codigoModelo'})   
#dfComModelos = dfComModelos.head(10) ### forçar apenas 10 registros para teste
############################################################################################
## captura dos anos dos modelos das marcas das tabelas ###
############################################################################################
dfComAnosModelos = pd.DataFrame() # iniciando um dataframe vazio para gravar os modelos
for row in dfComModelos.index:

    codigotabela       = dfComModelos.reset_index(drop=True)['tabelaReferencia'][row]
    codigoMarca        = dfComModelos.reset_index(drop=True)['codigoMarca'][row]
    nomeMarca          = dfComModelos.reset_index(drop=True)['nomeMarca'][row]
    codigoModelo       = dfComModelos.reset_index(drop=True)['codigoModelo'][row]
    nomeModelo         = dfComModelos.reset_index(drop=True)['nomeModelo'][row]

    anomodelos = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarAnoModelo',
          data = {
            'codigoTipoVeiculo': 1,
            'codigoTabelaReferencia': codigotabela, ## esse código será variável por cada tabela da relação de tabelas
            'codigoMarca':codigoMarca, ## esse código será variável por cada marca na relação de marcas
            'codigoModelo':codigoModelo, ## esse código será variável por cada modelo na relação de modelos
          }
          )
    df = json.dumps(anomodelos.json())
    df = pd.read_json(df)
    df['tabelaReferencia'] = codigotabela
    df['codigoMarca'] = codigoMarca
    df['nomeMarca']   = nomeMarca
    df['codigoModelo'] = codigoModelo
    df['nomeModelo']   = nomeModelo

    dfComAnosModelos = pd.concat([dfComAnosModelos,df])
    print( f'gravando tabela {codigotabela},  marca {codigoMarca} e modelo {codigoModelo}' )

dfComAnosModelos = dfComAnosModelos.rename(columns={'Label':'nomeAnoModelo','Value':'codigoAnoModelo'})   

### separação dos tipos de combustíveis da coluna codigoAnoModelo
dfComAnosModelos['tipoCombustivel'] = dfComAnosModelos['codigoAnoModelo'].str.slice(start=-1)
dfComAnosModelos['ano']             = dfComAnosModelos['codigoAnoModelo'].str.slice(stop=4)
###################################

dfComTodosOsParametros = pd.DataFrame() # iniciando um dataframe vazio para gravar os modelos
for row in dfComAnosModelos.index:

    codigotabela       = dfComAnosModelos.reset_index(drop=True)['tabelaReferencia'][row]
    codigoMarca        = dfComAnosModelos.reset_index(drop=True)['codigoMarca'][row]
    nomeMarca          = dfComAnosModelos.reset_index(drop=True)['nomeMarca'][row]
    codigoModelo       = dfComAnosModelos.reset_index(drop=True)['codigoModelo'][row]
    nomeModelo         = dfComAnosModelos.reset_index(drop=True)['nomeModelo'][row]
    ano                = dfComAnosModelos.reset_index(drop=True)['ano'][row]
    tipoCombustivel    = dfComAnosModelos.reset_index(drop=True)['tipoCombustivel'][row]

    rConsultaGeral = requests.post('https://veiculos.fipe.org.br/api/veiculos//ConsultarValorComTodosParametros',
            data = {
                'codigoTipoVeiculo': 1,
                'codigoTabelaReferencia': codigotabela, ## esse código será variável por cada tabela da relação de tabelas
                'codigoMarca':codigoMarca, ## esse código será variável por cada marca na relação de marcas
                'codigoModelo':codigoModelo, ## esse código será variável por cada modelo na relação de modelos
                'anoModelo':ano, ## esse código será variável por ano modelo na relação de ano modelo
                'codigoTipoCombustivel':tipoCombustivel,
                'tipoVeiculo':'carro',
                'tipoConsulta':'tradicional'
            }
    )
    
    d = rConsultaGeral.json()
    df = pd.DataFrame([d])

    df['tabelaReferencia'] = codigotabela
    df['codigoMarca'] = codigoMarca
    df['codigoModelo'] = codigoModelo
    df['anoModelo'] = ano
    df['codigoTipoCombustivel'] = tipoCombustivel
    dfComTodosOsParametros = pd.concat([dfComTodosOsParametros,df])
    print( f'gravando tabela {codigotabela},  marca {codigoMarca} e modelo {codigoModelo} e ano {ano}')

dfComTodosOsParametros.to_csv(dataPath+'/DatasetFinal.csv', index=False, header=True)

