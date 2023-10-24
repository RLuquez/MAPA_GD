import streamlit as st
import pandas as pd
import folium
import gdown

# Define o ID do arquivo no Google Drive
file_id = "1vO4UBl06tJd8afuGlI-LNM9M3nPZhhSt"

# URL do arquivo no Google Drive
url = f"https://drive.google.com/uc?id={file_id}"

# Baixa o arquivo do Google Drive
output = 'DADOS_GD_RESUMO.csv'
gdown.download(url, output, quiet=False)

# Lê o arquivo CSV
df = pd.read_csv(output)

# Defina a opção padrão
opcao = "Geração Distribuída"

# Estilos dos botões
button_style = "font-weight: bold; width: 100%; padding: 10px 0; background-color: #0074bf; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 18px;"

# Adicione uma imagem no canto superior direito da barra lateral
st.sidebar.image("logo2.jpg", width=200, caption="")

# Crie os botões na barra lateral
if st.sidebar.button("Geração Distribuída", key="GD_button", help="Clique para Geração Distribuída"):
    opcao = "Geração Distribuída    "

if st.sidebar.button("Geração Centralizada", key="GC_button", help="Clique para Geração Centralizada"):
    opcao = "Geração Centralizada"

if st.sidebar.button("Metodologia", key="Metodologia_button", help="Clique para Metodologia"):
    opcao = "Metodologia"

# Conteúdo principal do aplicativo
if opcao == "Geração Distribuída":
    # Conteúdo relacionado à Geração Distribuída
    st.title("Potencial de Reciclagem de Painéis Fotovoltaicos")

    # Adiciona uma linha horizontal
    st.write("---")

    # df = pd.read_csv("DADOS_GD_RESUMO.csv")

    # Informações Gerais - Geração Distribuída
    st.subheader("Informações Gerais - Geração Distribuída no Brasil")

    # Estilizando as caixas
    box_style = """
        background-color: #f4f4f4;
        padding: 1px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px #888888;
        text-align: center;
        width: 200px;
    """

    # Define as cores para os valores calculados
    value_styles = [
        'color: green; font-size: 26px;',  # Tamanho menor para o texto
        'color: blue; font-size: 26px;',  # Tamanho menor para o texto
        'color: orange; font-size: 26px;'  # Tamanho menor para o texto
    ]

    # Divide a tela em 3 colunas
    col1, col2, col3 = st.columns(3)

    # Valor numérico
    valor = df["N_MOD"].count()
    valor_col2 = df["N_MOD"].sum()
    valor_col3 = df["PESO_TOTAL"].sum() / 1000000

    # Formate o valor com separadores de milhares (vírgula) e 2 casas decimais
    valor_formatado = '{:,.0f}'.format(valor)
    valor_formatado_col2 = '{:,.0f}'.format(valor_col2)
    valor_formatado_col3 = '{:,.2f}'.format(valor_col3)

    with col1:
        st.markdown(
            f'<div style="{box_style}"><h4>Qtd de Sistemas de Geração Distribuida</h4><p style="{value_styles[0]}">{valor_formatado}</p></div>',
            unsafe_allow_html=True)

    with col2:
        st.markdown(
            f'<div style="{box_style}"><h4>Quantidade de Módulos Instalados</h4><p style="{value_styles[1]}">{valor_formatado_col2}</p></div>',
            unsafe_allow_html=True)

    with col3:
        st.markdown(
            f'<div style="{box_style}"><h4>Milhões de Toneladas de Módulos</h4><p style="{value_styles[2]}">{valor_formatado_col3}</p></div>',
            unsafe_allow_html=True)

    # Exibe a linha horizontal
    st.write("---")

    # Leitura dos DataFrames
    AGRUPAMENTO_MUNICIPIO = pd.read_csv("AGRUPAMENTO_MUNICIPIO.csv")
    AGRUPAMENTO_ESTADO = pd.read_csv("AGRUPAMENTO_ESTADO.csv")
    AGRUPAMENTO_REGIAO = pd.read_csv("AGRUPAMENTO_REGIAO.csv")

    # Título
    st.title("Mapa de Geração Distribuída")

    # Adicionar uma selectbox para escolher entre Estado, Região ou Município
    opcao = st.selectbox("Escolha a visualização:", ["Estado", "Região", "Município"])

    if opcao == "Município":
        # Barra de busca
        busca = st.text_input("Buscar município:")

    # Função para encontrar o local na base de dados
    def encontrar_local(data, nome_coluna, nome_local):
        local_encontrado = data[data[nome_coluna].str.contains(nome_local, case=False, na=False)]
        if not local_encontrado.empty:
            latitude = local_encontrado.iloc[0]['LATITUDE']
            longitude = local_encontrado.iloc[0]['LONGITUDE']
            return latitude, longitude, local_encontrado.iloc[0]
        return None, None, None

    # Escolha do DataFrame baseado na seleção do usuário
    if opcao == "Estado":
        data = AGRUPAMENTO_ESTADO
        mapa_title = "Mapa de Geração Distribuída por Estado"
        nome_column = "ESTADO"
    elif opcao == "Região":
        data = AGRUPAMENTO_REGIAO
        mapa_title = "Mapa de Geração Distribuída por Região"
        nome_column = "REGIÃO"
    else:
        data = AGRUPAMENTO_MUNICIPIO
        mapa_title = "Mapa de Geração Distribuída por Município"
        nome_column = "MUNICIPIO"

    # Criar um mapa centrado no Brasil
    m = folium.Map(location=[-15.77972, -47.92972], zoom_start=5)

    if opcao == "Município" and busca:
        # Tentar encontrar o local na base de dados
        latitude, longitude, info_municipio = encontrar_local(data, nome_column, busca)
        if latitude and longitude:
            # Ajustar o zoom do mapa com base na localização encontrada
            m.location = [latitude, longitude]
            m.zoom_start = 2  # Ajuste o valor do zoom para um zoom mais próximo

            # Exibir informações do município encontrado
            st.subheader(f"Informações do Município: {info_municipio[nome_column]}")
            st.write(info_municipio)
            st.write("OBS: Valores de peso em toneladas")

    # Adicionar marcadores para cada local (Estado, Região ou Município) com informações
    for _, row in data.iterrows():
        local = row[nome_column]
        latitude = row['LATITUDE']
        longitude = row['LONGITUDE']

        # Formatar as informações a serem exibidas no marcador
        popup_text = f"""<b>{nome_column}:</b> {local}<br>
                        <b>Comentário:</b> Valores de Potência em KW, Valores de Peso em toneladas para visualização de Municípios e Estado. Para a opção Região, os valores estão representados como milhões de toneladas.<br>
                        <b>Sistemas de GD :</b> {row['SISTEMAS']}<br>
                        <b>Potência (KW):</b> {row['POTÊNCIA']}<br>
                        <b>Número de Módulos:</b> {row['N_MOD']}<br>
                        <b>Peso Total:</b> {row['PESO_TOTAL']}<br>
                        <b>Vidro:</b> {row['VIDRO']}<br>
                        <b>Alumínio:</b> {row['ALUMÍNIO']}<br>
                        <b>Silício:</b> {row['SILÍCIO']}<br>
                        <b>Polímero:</b> {row['POLÍMERO']}<br>
                        <b>Cabos (Cu e Polimeros):</b> {row['CABOS (Cu e Polimeros)']}<br>
                        <b>Condutor Al (Interno):</b> {row['CONDUTOR AL (Interno)']}<br>
                        <b>Condutor Cu (Interno):</b> {row['CONDUTOR CU (Interno)']}<br>
                        <b>Chumbo e Estanho:</b> {row['CHUMBO E ESTANHO']}<br>
                        <b>Prata (t):</b> {row['PRATA']}<br>"""

        # Adicionar um marcador ao mapa com informações e um ícone pequeno
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=3,  # Tamanho da bolinha
            color='blue',  # Cor da bolinha
            fill=True,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(m)

    # Exibir o mapa
    st.subheader(mapa_title)
    st.components.v1.html(m._repr_html_(), height=600)

    # Gráfico de Barras
    st.subheader("Quantidade Total de Materiais")
    material_type = st.selectbox("Escolha o material:",
                                 ["PESO_TOTAL", "VIDRO", "ALUMÍNIO", 'EVA',	'SILÍCIO	POLÍMERO',	'CABOS (Cu e Polimeros)', 'CONDUTOR AL (Interno)', 'CONDUTOR CU (Interno)', 'CHUMBO E ESTANHO', 'PRATA'])
    chart_type = st.selectbox("Escolha o tipo de gráfico:", ["Por Região", "Por Estado", "Por Município"])

    if chart_type == "Por Região":
        data = df.groupby("REGIÃO")[material_type].sum()
    elif chart_type == "Por Estado":
        data = df.groupby("ESTADO")[material_type].sum()
    else:
        data = df.groupby("MUNICIPIO")[material_type].sum()

    st.bar_chart(data)

elif opcao == "Geração Centralizada":
    # Conteúdo relacionado à Geração Centralizada
    st.title("Geração Centralizada")
    st.write("Aqui você encontraria informações sobre Geração Centralizada.")

elif opcao == "Metodologia":
    # Conteúdo relacionado à Metodologia
    st.title("Metodologia")
    st.write("Página em Construção...")

# Conteúdo comum a todas as opções
st.write("Este é um texto comum a todas as opções da barra lateral.")
