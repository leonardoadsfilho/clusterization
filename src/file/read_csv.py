import pandas as pd
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def ReadCounties(uf):

    counties = pd.read_csv(f'{dir_path}/../../data/municipios.csv', sep=',')

    counties_names = counties['nome']
    counties.drop(['codigo_ibge', 'nome', 'capital', 'siafi_id', 'ddd', 'fuso_horario'], axis=1, inplace = True)
    counties = pd.DataFrame(counties).query(f"codigo_uf == {uf}")
    counties.drop(['codigo_uf'], axis=1, inplace = True)

    return (counties, counties_names)

def ReadUFs():
    
    data = pd.read_csv(f'{dir_path}/../../data/ufs.csv', sep=';')

    data = pd.DataFrame(data)

    uf = data['uf'].to_list()
    estado = data['estado'].to_list()
    sigla = data['sigla'].to_list()

    return (uf, estado, sigla)