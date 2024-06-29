# Case de uma Familly Office

## Introdução

Este projeto tem como objetivo monitorar e analisar os dados de uma competição onde investidores talentosos do Leblon competem para alcançar os melhores retornos sobre seus investimentos ao longo de um período específico. 

## Projeto

Este projeto consiste em três tarefas principais, cada uma projetada para lidar com aspectos específicos dos dados de investimento:

1. **Tarefa 1**: Calcular as quantidades de cada ativo que um participante possui em uma data específica.
2. **Tarefa 2**: Calcular o retorno percentual dos participantes em um período especificado e gerar uma tabela de retornos diários.
3. **Tarefa 3**: Calcular o resultado financeiro de um participante em cada ativo em uma data específica e identificar os ativos com melhor e pior desempenho.

## Arquivos de Dados

Os dados são fornecidos em um arquivo Excel com quatro planilhas essenciais:
- **Transacoes**: Contém dados das transações (data, ID do participante, ID do ativo, tipo de operação, quantidade, preço).
- **HistoricoPrecos**: Contém dados históricos de preços dos ativos.
- **Ativo**: Contém detalhes dos ativos (ID do ativo, nome do ativo, CNPJ).
- **Participante**: Contém detalhes dos participantes (ID do participante, nome do participante, CEP).

### Visão Geral das Funções

#### Tarefa 1: Calcular Quantidades de Ativos

```python
def tarefa1(id_participante: int, data: str) -> pd.DataFrame:
    # Função para calcular as quantidades de cada ativo que um participante possui em uma data específica.
    # Parâmetros:
    # - id_participante: O ID do participante.
    # - data: A data no formato 'yyyy-mm-dd'.
    # Retorna um DataFrame com as colunas 'id_ativo' e 'quantidade'.
```

#### Tarefa 2: Calcular Retornos e Gerar Tabela de Retornos Diários

#### Parte (a): Calcular Retorno Percentual

```python
def tarefa_2_a(data_inicial: str, data_final: str) -> pd.DataFrame:
    # Função para calcular o retorno percentual dos participantes entre duas datas.
    # Parâmetros:
    # - data_inicial: A data inicial no formato 'yyyy-mm-dd'.
    # - data_final: A data final no formato 'yyyy-mm-dd'.
    # Retorna um DataFrame com as colunas 'id_participante' e 'retorno_percentual'.
```

#### Parte (b): Gerar Tabela de Retornos Diários

```python
def tarefa_2_b(data_inicial: str, data_final: str) -> pd.DataFrame:
    # Função para gerar uma tabela de retornos diários e salvá-la em um arquivo Excel.
    # Parâmetros:
    # - data_inicial: A data inicial no formato 'yyyy-mm-dd'.
    # - data_final: A data final no formato 'yyyy-mm-dd'.
    # Retorna um DataFrame com as colunas 'data', 'id_participante', 'retorno_dia', 'retorno_acumulado', 'retorno_anualizado'.
```

#### Parte (c): Retornar Ranking dos Participantes em uma Data Específica

```python
def tarefa_2_c(data: str) -> pd.DataFrame:
    # Função para retornar o ranking dos participantes baseado no retorno acumulado em uma data específica.
    # Parâmetros:
    # - data: A data no formato 'yyyy-mm-dd'.
    # Retorna um DataFrame com as colunas 'nome_participante', 'retorno_dia', 'retorno_acumulado', 'retorno_anualizado'.
```

#### Tarefa 3: Calcular Resultado Financeiro de Cada Ativo

```python
def tarefa3(id_participante: int, data: str) -> pd.DataFrame:
    # Função para calcular o resultado financeiro de um participante em cada ativo e identificar os ativos com melhor e pior desempenho.
    # Parâmetros:
    # - id_participante: O ID do participante.
    # - data: A data no formato 'yyyy-mm-dd'.
    # Retorna um DataFrame com as colunas 'nome_ativo' e 'resultado'.
```

### Estrutura do projeto

```plaintext
case-familyoffice/
│
├── base_liga_invest_fo.xlsx  # Arquivo Excel contendo os dados das transações, histórico de preços, ativos e participantes
├── desafio.py                # Script contendo as funções para as tarefas solicitadas
├── retorno_diario.xlsx       # Arquivo Excel gerado pela Tarefa 2(b) com a tabela de retornos diários
├── requirements.txt          # Arquivo de dependências com bibliotecas necessárias
├── README.md                 # Arquivo README com instruções e detalhes do projeto

