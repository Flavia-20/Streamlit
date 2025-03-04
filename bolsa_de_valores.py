import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data #as informações da função vai ficar em cache
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2025-03-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOVDia_05-03-25.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [f"{item}.SA"  for item in tickers]
    #print(tickers)
    return tickers

acoes = carregar_tickers_acoes()
#acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes)

st.write("""
# Ano Preço de Ações 
""")

#prepara a visualização - sidebar
st.sidebar.header("Filtros")

#filtro de ações
lista_acoes = st.sidebar.multiselect('Escolha o que será visualizado',dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

#filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_de_data = st.sidebar.slider("Selecione o periodo", 
                  min_value = data_inicial, 
                  max_value = data_final, 
                  value=(data_inicial, data_final))


#print(intervalo_de_data)
dados = dados.loc[intervalo_de_data[0]: intervalo_de_data[1]]

#graficos
#st.area_chart(dados)
st.line_chart(dados)
#st.bar_chart(dados)
#st.scatter_chart(dados)

#calcilo de performance


texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)    
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close" :acao_unica})

carteira = [ 1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)
    
    carteira[i] = carteira[i] * (1 + performance_ativo)

    if performance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"   \n{acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"   \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"   \n{acao}: {performance_ativo:.1%}"

total_final_careira = sum(carteira)
performace_da_carteira = total_final_careira / total_inicial_carteira - 1
texto_performance_carteira = ""

if performace_da_carteira > 0:
    texto_performance_carteira = texto_performance_carteira + f"   \n{acao}: :green[{performace_da_carteira:.1%}]"
elif performace_da_carteira < 0:
    texto_performance_carteira = texto_performance_carteira + f"   \n{acao}: :red[{performace_da_carteira:.1%}]"
else:
    texto_performance_carteira = texto_performance_carteira + f"   \n{acao}: {performace_da_carteira:.1%}"


st.write(f"""
### Performance dos ativos:
         
{texto_performance_ativos}

{texto_performance_carteira}
""")





