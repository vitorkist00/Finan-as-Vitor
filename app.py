import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURAÇÃO E CONEXÃO ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Finanças").sheet1 

st.set_page_config(page_title="Gestão Financeira VIP", layout="wide")

# --- INTERFACE ---
st.title("💰 Controle Financeiro Inteligente")

aba1, aba2 = st.tabs(["📥 Entradas e Saídas", "📊 Relatório Detalhado"])

with aba1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Registrar Gasto")
        with st.form("form_gasto", clear_on_submit=True):
            data_g = st.date_input("Data do Gasto", datetime.now())
            desc_g = st.text_input("Descrição (Ex: Aluguel, Posto)")
            cat_g = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Lazer", "Trabalho", "Moradia", "Outros"])
            valor_g = st.number_input("Valor do Gasto (R$)", min_value=0.0, step=0.01)
            if st.form_submit_button("Salvar Despesa"):
                # Salvamos como valor negativo na planilha para os cálculos baterem
                sheet.append_row([str(data_g), desc_g, cat_g, -valor_g])
                st.success("Despesa registrada!")

    with col_b:
        st.subheader("Registrar Receita (Salário)")
        with st.form("form_receita", clear_on_submit=True):
            data_r = st.date_input("Data do Recebimento", datetime.now())
            desc_r = st.text_input("Origem", value="Salário Líquido")
            valor_r = st.number_input("Valor Recebido (R$)", min_value=0.0, step=0.01)
            if st.form_submit_button("Salvar Entrada"):
                sheet.append_row([str(data_r), desc_r, "Receita", valor_r])
                st.success("Entrada registrada!")

with aba2:
    st.subheader("Resumo do Mês")
    
    # Puxa os dados da planilha
    df = pd.DataFrame(sheet.get_all_records())
    
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        df['Mês/Ano'] = df['Data'].dt.strftime('%m/%Y')
        
        # Filtro de Mês
        lista_meses = df['Mês/Ano'].unique()
        mes_ref = st.selectbox("Selecione o Mês", lista_meses)
        df_mes = df[df['Mês/Ano'] == mes_ref]

        # --- CÁLCULOS ---
        total_receita = df_mes[df_mes['Valor'] > 0]['Valor'].sum()
        total_gastos = df_mes[df_mes['Valor'] < 0]['Valor'].sum()
        saldo_final = total_receita + total_gastos

        # --- MÉTRICAS ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Salário/Entradas", f"R$ {total_receita:.2f}")
        m2.metric("Gastos Totais", f"R$ {abs(total_gastos):.2f}", delta_color="inverse")
        m3.metric("Saldo Sobrando", f"R$ {saldo_final:.2f}")

        # --- SOMA POR CATEGORIA ---
        st.write("---")
        st.subheader("Gastos por Categoria")
        # Filtra apenas o que é gasto (negativo) e agrupa
        gastos_cat = df_mes[df_mes['Valor'] < 0].groupby('Categoria')['Valor'].sum().abs().reset_index()
        gastos_cat.columns = ['Categoria', 'Total Gasto']
        
        col_graf, col_tab = st.columns([2, 1])
        col_graf.bar_chart(gastos_cat.set_index('Categoria'))
        col_tab.dataframe(gastos_cat, hide_index=True)

    else:
        st.info("Ainda não há dados na planilha.")
