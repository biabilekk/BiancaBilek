import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../bases_tratadas/dadostratadosfarfetch.csv', sep=';')

st.dataframe(df)

st.subheader('Análise de nulos')
aux = df.isnull().sum().reset_index()
aux.columns = ['preco', 'desconto']
st.dataframe(aux)


st.subheader('Análises univariadas')
st.write('Medidas resumo')
st.dataframe(df.describe())

#SELECIONAR COLUNA
lista_de_colunas = df.columns

colunas_numericas = df.select_dtypes(include='number').columns.tolist()


# VERIFICA COLUNAS NUMÉRICAS
if colunas_numericas:

    # SELECIONA
    coluna_escolhida = st.selectbox('Escolha a coluna', colunas_numericas)

    media = round(df[coluna_escolhida].mean(),2)
    desvio = round(df[coluna_escolhida].std(),2)
    mediana = round(df[coluna_escolhida].quantile(0.5),2)
    maximo = round(df[coluna_escolhida].max(),2)
    minimo = round(df[coluna_escolhida].max(),2)

    st.write(f"**Média**: {media}")
    st.write(f"**Desvio padrão**: {desvio}")
    st.write(f"**Mediana**: {mediana}")
    st.write(f"**Máximo**: {maximo}")
else:
    st.warning("Não contém coluna numérica.")

print('Média de valores descontados:', media)
print('Desvio padrão de valores descontados:', desvio)
print('Mediana dos valores descontados:', mediana)
print('Máximo dos valores descontados:' , maximo)
print('Menor valor dos descontados:', minimo)

st.write(f'A coluna escolhida foi {coluna_escolhida}. A sua média é {media}. Seu desvio padrão indica que, quando há desvio, desvia em média {desvio}. E 50% dos dados vão até o valor {mediana}. E seu máximo é de {maximo}.')
st.write(f'O produto com o maior valor, custa {minimo} reais')
st.write('Histograma')
fig = px.histogram(df,x=[coluna_escolhida])
st.plotly_chart(fig)
st.write('Boxplot')
fig2 = px.box(df, x=[coluna_escolhida])
st.plotly_chart(fig2)

st.subheader('Análises multivariadas')
lista_de_escolhas = st.multiselect('Escolha mais de uma coluna para avaliar', lista_de_colunas)
st.markdown('Gráfico de dispersão')
if len(lista_de_escolhas)>2 or len(lista_de_escolhas)<2:
    st.error('Escolha somente 2 colunas')
else:
    fig3 = px.scatter(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig3)
    st.markdown('Gráfico de caixa')
    fig4 = px.box(df, x=lista_de_escolhas[0], y=lista_de_escolhas[1])
    st.plotly_chart(fig4)
    fig5 = px.pie(df, lista_de_escolhas[0], lista_de_escolhas[1])
    st.plotly_chart(fig5)