import pandas as pd

transacoes = pd.read_excel('base_liga_invest_fo (4).xlsx', sheet_name=0)
historico_precos = pd.read_excel('base_liga_invest_fo (4).xlsx', sheet_name='HistoricoPrecos')
participantes = pd.read_excel('base_liga_invest_fo (4).xlsx', sheet_name='Participante')
ativos = pd.read_excel('base_liga_invest_fo (4).xlsx', sheet_name='Ativo')

def tarefa1(id_participante: int, data: str) -> pd.DataFrame:

    transacoes['data'] = pd.to_datetime(transacoes['data'])

    # Vamos filtrar o histórico de preços até a data desejada

    id_data = transacoes[(transacoes['id_participante'] == id_participante) & (transacoes['data'] <= data)].copy()

    id_data.loc[id_data['operacao'] == 'compra', 'quantidade'] = id_data['quantidade']

    id_data.loc[id_data['operacao'] == 'venda', 'quantidade'] = -id_data['quantidade']

    df_tarefa1 = id_data.groupby('id_ativo')['quantidade'].sum().reset_index()

    return df_tarefa1

#Teste
#print(tarefa1(102,'2024-05-08'))
def tarefa_2_a(data_inicial: str, data_final: str) -> pd.DataFrame:

    # Precisamos calcular o retorno percentual de cada participante em uma determinada data

    data_inicial = pd.to_datetime(data_inicial)
    data_final = pd.to_datetime(data_final)

    # Vamos filtrar o histórico de preços para as datas inicial e final

    precos_iniciais = historico_precos[historico_precos['data'] == data_inicial]
    precos_finais = historico_precos[historico_precos['data'] == data_final]

    retorno_percentual = []

    for id_participante in participantes['id_participante']:

        # Filtrando para as transações até a data inicial

        transacoes_iniciais = transacoes[
            (transacoes['data'] <= data_inicial) & (transacoes['id_participante'] == id_participante)]

        # Filtrando para as transações até a data final

        transacoes_finais = transacoes[
            (transacoes['data'] <= data_final) & (transacoes['id_participante'] == id_participante)]

        # Precisamos calcular a quantidade de ativos na data inicial

        compras_ativos_iniciais = transacoes_iniciais[transacoes_iniciais['operacao'] == 'compra'].groupby('id_ativo')[
            'quantidade'].sum()

        vendas_ativos_iniciais = transacoes_iniciais[transacoes_iniciais['operacao'] == 'venda'].groupby('id_ativo')[
            'quantidade'].sum()

        quantidade_ativos_inicial = compras_ativos_iniciais.sub(vendas_ativos_iniciais, fill_value=0).reset_index()

        quantidade_ativos_inicial.columns = ['id_ativo', 'quantidade']

        # Precisamos calcular a quantidade de ativos na data final

        compras_ativos_finais = transacoes_finais[transacoes_finais['operacao'] == 'compra'].groupby('id_ativo')[
            'quantidade'].sum()

        vendas_ativos_finais = transacoes_finais[transacoes_finais['operacao'] == 'venda'].groupby('id_ativo')[
            'quantidade'].sum()

        quantidade_ativos_final = compras_ativos_finais.sub(vendas_ativos_finais, fill_value=0).reset_index()

        quantidade_ativos_final.columns = ['id_ativo', 'quantidade']

        # Calculando o valor total dos ativos na data inicial

        valor_inicial = quantidade_ativos_inicial.merge(precos_iniciais, on='id_ativo', how='left')

        valor_inicial['valor'] = valor_inicial['quantidade'] * valor_inicial['preco']

        valor_inicial_total = valor_inicial['valor'].sum()

        # Calculando o valor total dos ativos na data final

        valor_final = quantidade_ativos_final.merge(precos_finais, on='id_ativo', how='left')

        valor_final['valor'] = valor_final['quantidade'] * valor_final['preco']

        valor_final_total = valor_final['valor'].sum()

        # Calcula o dinheiro em reserva inicial(considerando que o investimento inicial é de R$ 100,000)

        compras_quantidade_inicial = transacoes_iniciais[transacoes_iniciais['operacao'] == 'compra']['quantidade']

        compras_preco_inicial = transacoes_iniciais[transacoes_iniciais['operacao'] == 'compra']['preco']

        compras_iniciais = (compras_quantidade_inicial * compras_preco_inicial).sum()

        vendas_quantidade_inicial = transacoes_iniciais[transacoes_iniciais['operacao'] == 'venda']['quantidade']

        vendas_preco_inicial = transacoes_iniciais[transacoes_iniciais['operacao'] == 'venda']['preco']

        vendas_iniciais = (vendas_quantidade_inicial * vendas_preco_inicial).sum()

        reserva_inicial = 100000 - compras_iniciais + vendas_iniciais

        # Calcula o dinheiro em reserva final

        compras_quantidade_final = transacoes_finais[transacoes_finais['operacao'] == 'compra']['quantidade']

        compras_preco_final = transacoes_finais[transacoes_finais['operacao'] == 'compra']['preco']

        compras_finais = (compras_quantidade_final * compras_preco_final).sum()

        vendas_quantidade_final = transacoes_finais[transacoes_finais['operacao'] == 'venda']['quantidade']

        vendas_preco_final = transacoes_finais[transacoes_finais['operacao'] == 'venda']['preco']

        vendas_finais = (vendas_quantidade_final * vendas_preco_final).sum()

        reserva_final = 100000 - compras_finais + vendas_finais

        patrimonio_inicial = reserva_inicial + valor_inicial_total

        patrimonio_final = reserva_final + valor_final_total

        # Resta calcular o retorno percentual de cada participante

        retorno = ((patrimonio_final / patrimonio_inicial) - 1) * 100

        retorno_percentual.append({'id_participante': id_participante, 'retorno_percentual': f'{retorno}%'})

    return pd.DataFrame(retorno_percentual)

#Teste
#print(tarefa_2_a('2024-05-06', '2024-05-08'))
def tarefa_2_b(data_inicial: str, data_final: str) -> pd.DataFrame:

    data_inicial = pd.to_datetime(data_inicial)
    data_final = pd.to_datetime(data_final)

    datas = pd.date_range(start=data_inicial, end=data_final)

    tabela_retorno_diario = []

    for i in range(1, len(datas)):
        data_anterior = datas[i - 1]
        data_atual = datas[i]

        retorno_dia = tarefa_2_a(data_anterior, data_atual)
        for _, linha in retorno_dia.iterrows():
            id_participante = linha['id_participante']
            retorno_percentual = linha['retorno_percentual']
            tabela_retorno_diario.append({
                'data': data_atual,
                'id_participante': id_participante,
                'retorno_dia': retorno_percentual
            })

    df_retorno_diario = pd.DataFrame(tabela_retorno_diario)

    df_retorno_diario['retorno_dia'] = df_retorno_diario['retorno_dia'].str.replace('%', '').astype(float)

    # Resta calcular o retorno acumulado e anualizado

    retorno_acumulado_dict = {id_participante: 1 for id_participante in participantes['id_participante']}

    for indice, linha in df_retorno_diario.iterrows():
        id_participante = linha['id_participante']
        retorno_dia = linha['retorno_dia'] / 100
        retorno_acumulado_dict[id_participante] *= (1 + retorno_dia)
        df_retorno_diario.at[indice, 'retorno_acumulado'] = (retorno_acumulado_dict[id_participante] - 1) * 100


    for id_participante in participantes['id_participante']:
        df_participante = df_retorno_diario[df_retorno_diario['id_participante'] == id_participante]
        df_participante = df_participante.sort_values(by='data')

        dias_totais = (df_participante['data'].max() - df_participante['data'].min()).days
        df_retorno_diario.loc[df_participante.index, 'retorno_anualizado'] = ((1 + df_participante[
            'retorno_acumulado'] / 100) ** (365 / dias_totais) - 1) * 100

    df_retorno_diario['retorno_anualizado'] = df_retorno_diario['retorno_anualizado'].round(2)

    df_retorno_diario['data'] = df_retorno_diario['data'].dt.strftime('%Y-%m-%d')

    # Exportando o DataFrame para um arquivo Excel
    df_retorno_diario.to_excel('retorno_diario.xlsx', index=False)

    return df_retorno_diario

#Teste
#data_inicial = '2024-05-06'
#data_final = '2024-05-15'
#df_retorno_diario = tarefa_2_b(data_inicial, data_final)
#print(df_retorno_diario)


def tarefa_2_c(data: str) -> pd.DataFrame:
    data = pd.to_datetime(data).strftime('%Y-%m-%d')

    menor_data = transacoes['data'].min().strftime('%Y-%m-%d')

    df_retorno_diario = tarefa_2_b(menor_data, data)

    df_filtrado = df_retorno_diario[df_retorno_diario['data'] == data]

    df_filtrado = df_filtrado.merge(participantes[['id_participante', 'nome_participante']], on='id_participante')

    df_resultado = df_filtrado[['nome_participante', 'retorno_dia', 'retorno_acumulado', 'retorno_anualizado']]

    df_resultado = df_resultado.sort_values(by='retorno_acumulado', ascending=False)

    return df_resultado

#Teste
#df_resultado = tarefa_2_c('2024-05-15')
#rint(df_resultado)


def tarefa3(id_participante: int, data: str) -> pd.DataFrame:

    data = pd.to_datetime(data)

    # Filtrando  até a data desejada
    transacoes_participante = transacoes[
        (transacoes['id_participante'] == id_participante) & (transacoes['data'] <= data)].copy()

    # Calculando as quantidades de ativos
    compras_ativos = transacoes_participante[transacoes_participante['operacao'] == 'compra'].groupby('id_ativo')[
        'quantidade'].sum()
    vendas_ativos = transacoes_participante[transacoes_participante['operacao'] == 'venda'].groupby('id_ativo')[
        'quantidade'].sum()

    # Calcula a quantidade final de cada ativo
    quantidade_ativos = compras_ativos.sub(vendas_ativos, fill_value=0).reset_index()
    quantidade_ativos.columns = ['id_ativo', 'quantidade']

    # Preço dos ativos na data desejada
    precos_na_data = historico_precos[historico_precos['data'] == data]

    resultado_ativos = quantidade_ativos.merge(precos_na_data, on='id_ativo', how='left')

    transacoes_participante.loc[:, 'valor'] = transacoes_participante['quantidade'] * transacoes_participante['preco']

    # Calculando o custo total
    custo_compras = transacoes_participante[transacoes_participante['operacao'] == 'compra'].groupby('id_ativo')[
        'valor'].sum().reset_index().rename(columns={'valor': 'valor_compra'})
    valor_vendas = transacoes_participante[transacoes_participante['operacao'] == 'venda'].groupby('id_ativo')[
        'valor'].sum().reset_index().rename(columns={'valor': 'valor_venda'})

    # Juntando os dados
    resultado_ativos = resultado_ativos.merge(custo_compras, on='id_ativo', how='left')
    resultado_ativos = resultado_ativos.merge(valor_vendas, on='id_ativo', how='left')

    # Preenchendo valores Nan com 0 para facilitar o manuseio
    resultado_ativos = resultado_ativos.fillna(0)

    # Uma pequena função lambda para calcular o resultado de acordo com a fórmula
    resultado_ativos['resultado'] = resultado_ativos.apply(
        lambda row: (row['preco'] * row['quantidade']) - row['valor_compra'] + row['valor_venda'], axis=1
    )

    resultado_ativos = pd.merge(resultado_ativos, ativos[['id_ativo', 'nome_ativo']], on='id_ativo')

    # Pegando os maiores e menores resultados
    maior_resultado = resultado_ativos.loc[resultado_ativos['resultado'].idxmax()]
    menor_resultado = resultado_ativos.loc[resultado_ativos['resultado'].idxmin()]

    # Criando df
    result_df = pd.DataFrame({
        'nome_ativo': [maior_resultado['nome_ativo'], menor_resultado['nome_ativo']],
        'resultado': [maior_resultado['resultado'], menor_resultado['resultado']]
    })

    return result_df

#Teste
#print(tarefa3(101,'2024-05-08'))
