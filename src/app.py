import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados

def grafico_comparativo_versao_karol(dados_2019,dados_2020,causa="todas",uf="Brasil"):
    if(uf=="Brasil"):
        total_2019 = dados_2019.groupby('tipo_doenca').sum()
        total_2020 = dados_2020.groupby('tipo_doenca').sum()
        if(causa=='todas'):
            lista = [total_2019['total'].sum(),total_2020['total'].sum()]
        else:
            lista = [int(total_2019.loc[causa]),int(total_2020.loc[causa])]
    else:
        total_2019 = dados_2019.groupby(['uf','tipo_doenca']).sum()
        total_2020 = dados_2020.groupby(['uf','tipo_doenca']).sum()
        if(causa=='todas'):
            lista = [int(total_2019.loc[uf].sum()),int(total_2020.loc[uf].sum())]
        else:
            lista = [int(total_2019.loc[uf,causa]),int(total_2020.loc[uf,causa])]

    dados = pd.DataFrame({'Total':lista,'Ano':[2019,2020]})
    #plt.figure(figsize=(8,6))
    #plt.title(f"Número de Óbitos por {causa} - {uf}")
    fig, ax = plt.subplots()
    ax = sns.barplot(x="Ano",y="Total",data=dados)
    
    return fig
    #plt.show()

def main():
    obitos_2019=carrega_dados('dados/obitos-2019.csv')
    obitos_2020=carrega_dados('dados/obitos-2020.csv')
    tipo_doenca = np.append(obitos_2020['tipo_doenca'].unique(),'todas')
    estado = np.append(obitos_2020['uf'].unique(),'Brasil')

    

    st.title('Comparativo do número de óbitos por doença/UF 2019-2020')
    st.markdown("#### Este trabalho analisa os dados dos óbitos no Brasil nos anos de 2019 e 2020.")
    opcao_0 = st.radio('Deseja visualizar o Dataframe',('Não desejo visualizar','Óbitos 2019','Óbitos 2020'))
    if opcao_0=='Óbitos 2019':
        st.dataframe(obitos_2019)
    elif opcao_0=='Óbitos 2020':
        st.dataframe(obitos_2020)
    else:
        pass

    opcao_1 = st.selectbox('Selecione o tipo de doença',tipo_doenca)
    opcao_2 = st.selectbox('Selecione o Estado',estado)

    figura = grafico_comparativo_versao_karol(obitos_2019,obitos_2020,opcao_1,uf=opcao_2)

    st.pyplot(figura)
   
    

if __name__ == "__main__":
    main()