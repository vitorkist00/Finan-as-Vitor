import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. Configuração de Acesso (Dizendo ao Python para usar os 'Secrets')
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
try:
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # Coloque o nome EXATO da sua planilha do Google aqui embaixo:
    sheet = client.open("Finanças").sheet1 
except Exception as e:
    st.error(f"Erro de Conexão: Verifique se as Secrets foram coladas corretamente. {e}")

# 2. Interface do App
st.title("💰 Meu Controle Financeiro")

tab1, tab2 = st.tabs(["Registrar", "Relatório"])

with tab1:
    with st.form("add_gasto", clear_on_submit=True):
        data = st.date_input("Data", datetime.now())
        desc = st.text_input("Descrição")
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Lazer", "Trabalho", "Outros"])
        valor = st.number_input("Valor (R$)", step=0.01)
        enviar = st.form_submit_button("Salvar")
        
        if enviar:
            sheet.append_row([str(data), desc, cat, valor])
            st.success("Salvo na planilha!")

with tab2:
    if st.button("Atualizar Dados"):
        dados = pd.DataFrame(sheet.get_all_records())
        st.dataframe(dados)
