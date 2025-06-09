#IMPORTAR BIBLIOTECAS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import missingno as msno
import plotly.express as px
from unidecode import unidecode
import streamlit as st

#ABRIR O SITE
navegador = webdriver.Chrome()
navegador.get('https://www.farfetch.com/br/shopping/women/sale/all/items.aspx')
navegador.maximize_window()

#ROLAR A PÁGINA
import time
altura_total = navegador.execute_script("return document.body.scrollHeight")
altura_atual = 0
while altura_atual < altura_total:
    navegador.execute_script("window.scrollBy(0, 1000);")
    altura_atual += 1000
    time.sleep(0.5)

#LISTA DOS PRODUTOS
lista_produtos = [] # lista vazia
for produto in range(1,97):
    try:
        navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{produto}]/div/a/div[2]/div[1]/p[2]').text
        dado_produto = navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{produto}]/div/a/div[2]/div[1]/p[2]').text
        lista_produtos.append(dado_produto)
    except:
        pass

#LISTA DOS PREÇOS
lista_precos = [] # lista vazia
for preco in range(1,97):
    try:
        navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{preco}]/div/a/div[2]/div[2]/div/p[1]').text
        dado_preco = navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{preco}]/div/a/div[2]/div[2]/div/p[1]').text
        lista_precos.append(dado_preco)
    except:
        pass

#LISTA DOS DESCONTOS
lista_descontos = [] # lista vazia
for desconto in range(1,97):
    try:
        navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{desconto}]/div/a/div[2]/div[2]/span').text
        dado_desconto = navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{desconto}]/div/a/div[2]/div[2]/span').text
        
    except:
        dado_desconto = (f'0%')
    lista_descontos.append(dado_desconto)

#LISTA DOS PREÇOS COM DESCONTOS
lista_precos_desconto = [] # lista vazia
for preco_desconto in range(1,97):
    try:
        navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{preco_desconto}]/div/a/div[2]/div[2]/div/p[2]').text
        dado_preco_desconto = navegador.find_element(By.XPATH, f'//*[@id="catalog-grid"]/li[{preco_desconto}]/div/a/div[2]/div[2]/div/p[2]').text
        lista_precos_desconto.append(dado_preco_desconto)
    except:
        pass

#DATAFRAME PRODUTO
tabela1 = pd.DataFrame(lista_produtos, columns=['produto'])

#DATAFRAME PREÇO
tabela2 = pd.DataFrame(lista_precos, columns=['preco'])

#DATAFRAME DESCONTO
tabela3 = pd.DataFrame(lista_descontos, columns=['desconto'])

#DATAFRAME PREÇO COM DESCONTO
tabela4 = pd.DataFrame(lista_precos_desconto, columns=['preco_desconto'])

#CONCATENAR DATAFRAMES
df = pd.concat([tabela1, tabela2, tabela3, tabela4], axis=1)

#EXPORTANDO BASE BRUTA CSV
df.to_csv('../bases_originais/dadosbrutosfarfetch.csv', sep=';', index=False)

#LIMPEZA DE PREÇOS
df['preco']=df.preco.str.replace('\n', ' ').str.replace(' ,', ',').str.replace(', ', ',').str.replace('R$ ', '').str.split(' ').str.get(0).str.replace(',',';').str.replace('.','').str.replace(';', '.').str.replace('R$', ' ')

#LIMPEZA DE PREÇOS
df['desconto']=df.desconto.str.replace('\n', ' ').str.replace('%', ',').str.replace(', ', ',').str.replace(',', '').str.replace('-', '')

#LIMPEZA DE PREÇOS
df['preco_desconto']=df.preco_desconto.str.replace('\n', ' ').str.replace(' ,', ',').str.replace(', ', ',').str.replace('R$ ', '').str.split(' ').str.get(0).str.replace(',',';').str.replace('.','').str.replace(';', '.').str.replace('R$', ' ')

#CONVERTER PARA NÚMERICO
for numer in ['preco', 'desconto', 'preco_desconto']:
    df[numer] = pd.to_numeric(df[numer], errors='coerce')
    
#TRATAMENTO DE NULOS
df.fillna({'preco':0, 'desconto':0, 'preco_desconto':0}, inplace=True)

#TRATAMENTO DE DUPLICADOS
df = df.drop_duplicates()

#TRATAMENTO DE CARACTERES DO PRODUTO
df['produto']=df['produto'].apply(unidecode)

#OUTLIERS PREÇOS
df.loc[df['preco'] >= 15000, 'preco'] = 15000
df.loc[df['preco'] <= 0, 'preco'] = 100

#OUTLIERS PREÇOS COM DESCONTO
df.loc[df['preco_desconto'] >= 12000, 'preco_desconto'] = 12000
df.loc[df['preco_desconto'] <= 0, 'preco_desconto'] = 100

#EXPORTANDO BASE TRATADA CSV
df.to_csv('../bases_tratadas/dadostratadosfarfetch.csv', sep=';', index=False)
