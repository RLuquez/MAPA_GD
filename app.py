#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap

# Título e informações
st.title("Potencial de Reciclagem de Painéis Fotovoltaicos")
st.write("Esse site tem como objetivo apresentar o potencial de reciclagem de painéis fotovoltaicos de cada município do Brasil.")
st.write("Abaixo é apresentado o mapa do Brasil, onde cada ponto faz referência a um município, ao clicar no ponto é possível observar informações como número de sistemas de geração distribuída, potência instalada, número de painéis, quantidade de cada material contido nos painéis como vidro, alumínio, silício, cobre, prata chumbo e outro.")
st.write("* Os dados de potência estão na unidade de (w).")
st.write("* Os dados de peso estão na unidade de (kg).")

# Exibe os serviços de dados
st.title("Serviços de Dados")
st.write("Todos os dados utilizados são públicos e podem ser consultados nos seguintes endereços:")
st.write("ANEEL – API: https://dadosabertos.aneel.gov.br/api/3/action/datastore_search")
st.write("IBGE – API:  https://servicodados.ibge.gov.br/docs/localidades")

# Exibe a imagem "logo2" no canto superior esquerdo
st.image("logo2.jpg", width=100)

# Adiciona uma linha horizontal
st.write("---")

# Carrega os dados do arquivo CSV
COORDENADAS_MUNICIPIOS_GD = pd.read_csv("COORDENADAS_MUNICIPIOS_GD.csv")

# Renomeia as colunas para "lat" e "lon"
COORDENADAS_MUNICIPIOS_GD = COORDENADAS_MUNICIPIOS_GD.rename(columns={
    "latitude": "lat",
    "longitude": "lon",
    "SISTEMAS_GD": "Sistemas GD",
    "POTÊNCIA (w)": "Potência",
    "N_MOD": "Número de Módulos",
    "TOTAL PESO (kg)": "Peso Total",
    "TOTAL VIDRO (kg)": "Vidro",
    "TOTAL ALUMÍNIO (kg)": "Alumínio",
    "TOTAL SILÍCIO (kg)": "Silício",
    "TOTAL POLÍMERO (kg)": "Polímero",
    "TOTAL ZINCO (kg)": "Zinco",
    "TOTAL CHUMBO (kg)": "Chumbo",
    "TOTAL COBRE (kg)": "Cobre",
    "TOTAL PRATA (kg)": "Prata"
})

# Mapa de marcadores
st.title("Mapa de Marcadores")
# Cria um mapa com os pontos
m = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)

# Adiciona marcadores para cada município com informações
for _, row in COORDENADAS_MUNICIPIOS_GD.iterrows():
    municipio = row['MUNICIPIOS']
    latitude = row['lat']
    longitude = row['lon']

    # Formata as informações a serem exibidas no marcador
    popup_text = f"""<b>Município:</b> {municipio}<br>
                    <b>Sistemas GD:</b> {row['Sistemas GD']}<br>
                    <b>Potência:</b> {row['Potência']}<br>
                    <b>Número de Módulos:</b> {row['Número de Módulos']}<br>
                    <b>Peso Total:</b> {row['Peso Total']}<br>
                    <b>Vidro:</b> {row['Vidro']}<br>
                    <b>Alumínio:</b> {row['Alumínio']}<br>
                    <b>Silício:</b> {row['Silício']}<br>
                    <b>Polímero:</b> {row['Polímero']}<br>
                    <b>Zinco:</b> {row['Zinco']}<br>
                    <b>Chumbo:</b> {row['Chumbo']}<br>
                    <b>Cobre:</b> {row['Cobre']}<br>
                    <b>Prata:</b> {row['Prata']}<br>"""

    # Adiciona um marcador ao mapa com informações e um ícone pequeno
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=3,  # Tamanho da bolinha
        color='blue',  # Cor da bolinha
        fill=True,
        popup=folium.Popup(popup_text, max_width=300),
    ).add_to(m)

# Exibe o mapa de marcadores no Streamlit
st.components.v1.html(m._repr_html_(), height=600)

# Exibe a linha horizontal
st.write("---")

# Mapa de calor
st.title("Mapa de Calor")
# Lista de colunas para o mapa de calor
columns_for_heatmap = ["Sistemas GD", "Potência", "Número de Módulos", "Peso Total", "Vidro",
                       "Alumínio", "Silício", "Polímero", "Zinco", "Chumbo", "Cobre", "Prata"]
selected_column = st.selectbox("Escolha a coluna para o mapa de calor", columns_for_heatmap)

# Cria um mapa com base na coluna selecionada
heat_map = folium.Map(location=[-15.77972, -47.92972], zoom_start=5)

# Cria uma lista de coordenadas para o mapa de calor
heat_data = [[row['lat'], row['lon'], row[selected_column]] for _, row in COORDENADAS_MUNICIPIOS_GD.iterrows()]

# Adiciona o mapa de calor
HeatMap(heat_data).add_to(heat_map)

# Exibe o mapa de calor no Streamlit
st.components.v1.html(heat_map._repr_html_(), height=600)

# Exibe a linha horizontal
st.write("---")

# Exibe a linha horizontal
st.line_chart([(0, 0), (1000, 1)], color="blue", width=10)


# In[ ]:




