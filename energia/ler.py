import pandas as pd
import numpy as np
import numpy_quaddtype as npq

def parse_coordenadas(x, N):
    """
    Dado um vetor x de dimensao 6N, retorna os vetores q e p
    contidos em x
    """
    # print([a for a in x[0:N]][0])
    # print([float(a) for a in x[0:N]][0])
    # exit()
    R = [
        [float(a) for a in x[0:N]],
        [float(a) for a in x[N:2*N]],
        [float(a) for a in x[2*N:3*N]]
    ]
    P = [
        [float(a) for a in x[3*N:4*N]],
        [float(a) for a in x[4*N:5*N]],
        [float(a) for a in x[5*N:6*N]]
    ]
    R = np.array(list(zip(*R)))
    P = np.array(list(zip(*P)))
    return R, P

def ler_simulacao_csv (arquivo, chunksize, saltos=1):
    """
    Le um arquivo de dados de simulacao (trajetorias) em .csv
    """
    valores_R, valores_P = [], []
    for chunk in pd.read_csv(arquivo, chunksize=chunksize, skiprows=3, float_precision='round_trip'):
        # Aplica a funcao
        def func_res (x):
            [R, P] = [*parse_coordenadas(x, int(len(x)/6))]
            valores_R.append(R)
            valores_P.append(P)
        chunk.apply(func_res, axis=1)
    return valores_R[::saltos], valores_P[::saltos]

def ler_simulacao_bin (arquivo):
    """
    Le um arquivo de dados de simulacao (trajetorias) em .bin
    """
    arq = open(arquivo)
    float_tipo = np.float64

    # A primeira linha tem o formato: h, G, N
    tipo_1a_linha = np.dtype([
        ('col1', float_tipo), ('col2', float_tipo), ('col3', 'i')
    ])
    primeira_linha = np.fromfile(file=arq, count=1, dtype=tipo_1a_linha)[0]
    print(primeira_linha)
    
    # Agora captura as massas (2a linha)
    N = primeira_linha[2]
    tipo_2a_linha = np.dtype([(f'col{i}', float_tipo) for i in range(N)])
    massas = np.fromfile(file=arq, count=1, dtype=tipo_2a_linha)[0]
    
    # Agora le o arquivo inteiro
    tipo_dado = np.dtype([(f'col{i}', float_tipo) for i in range(6*N)])
    dados = np.fromfile(file=arq, dtype=tipo_dado)

    dados = [list(x) for x in dados]
    valores_R, valores_P = [], []
    for linha in dados:
        [R, P] = [*parse_coordenadas(linha, N)]
        valores_R.append(R)
        valores_P.append(P)    
    return valores_R, valores_P