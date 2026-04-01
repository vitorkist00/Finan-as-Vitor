# --- NO FINAL DA SEÇÃO DA ABA 2 ---
st.write("---")
st.subheader("⚠️ Zona de Perigo")

with st.expander("Configurações Avançadas"):
    st.warning("Esta ação é irreversível. Ela apagará TODOS os dados da sua planilha para começar do zero.")
    
    # Checkbox de segurança para o botão não ficar ativo por engano
    confirmar_reset = st.checkbox("Eu entendo que isso apagará todo o meu histórico de testes.")
    
    if st.button("Zerar todas as informações", disabled=not confirmar_reset):
        try:
            # Captura todos os dados para manter o cabeçalho
            cabecalho = ["Data", "Descricao", "Categoria", "Valor"]
            
            # Limpa a planilha inteira
            sheet.clear()
            
            # Reinsere apenas a primeira linha de títulos
            sheet.append_row(cabecalho)
            
            st.success("Planilha zerada com sucesso! Agora você pode começar o uso real.")
            # Recarrega a página para limpar os gráficos da tela
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao tentar zerar a planilha: {e}")
