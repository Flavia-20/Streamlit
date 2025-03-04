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

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]

dados = carregar_dados(acoes)

st.write("""
# Ano Preço de Ações 
""")

lista_acoes = st.multiselect('Escolha o que será visualizado',dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

print("\n")

#grafico
st.area_chart(dados)
st.line_chart(dados)
st.bar_chart(dados)
st.scatter_chart(dados)



window = st.slider("pppppp")

