import streamlit as st
import pandas as pd
import numpy as np

def show_dash():
    # Texto
    st.header('Acompanhamento Estrutura NSAP')

    st.sidebar.header('Escolha as opções a baixo.')

    # Dados
    df = pd.DataFrame(
        np.random.randn(100, 3),
        columns=['Preço', 'Taxa de desocupação', 'Taxa inadimplência']
    )

    st.line_chart(df)
