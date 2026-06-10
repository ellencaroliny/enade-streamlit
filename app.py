import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import xml.etree.ElementTree as ET

# Configuração da página
st.set_page_config(
    page_title="Análise ENADE - Cubo OLAP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Análise Multidimensional do ENADE")
st.markdown("### Sistema de Análise OLAP baseado em Cubo de Dados")
st.markdown("---")

# Sidebar com informações do cubo
with st.sidebar:
    st.header("🎲 Estrutura do Cubo")
    st.markdown("""
    **Dimensões:**
    - 👤 **Estudante**: Perfil socioeconômico
    - 🎓 **Curso**: Geografia e características
    - 📝 **Avaliação**: Percepção da prova
    - 📅 **Tempo**: Ciclos avaliativos

    **Medidas:**
    - 📈 Média Nota Geral
    - 📘 Média Formação Geral
    - 📕 Média Componente Específico
    """)

    st.markdown("---")
    st.info("💡 Selecione uma análise no menu principal")

# Menu de seleção de análise
st.sidebar.header("🔍 Tipo de Análise")
tipo_analise = st.sidebar.radio(
    "Escolha o nível de complexidade:",
    ["Análises Triviais", "Análises Não Triviais"],
    index=0
)

# ANÁLISES TRIVIAIS
if tipo_analise == "Análises Triviais":
    st.header("📊 Análises Triviais")

    analise_selecionada = st.selectbox(
        "Selecione a análise:",
        [
            "Média de Nota Geral por Ano",
            "Média de Nota Geral por Região do País",
            "Média de Nota Geral por Sexo",
            "Média de Nota de Formação Geral por Tipo de Escola",
            "Média de Nota do Componente Específico por Turno"
        ]
    )

    # Análise 1: Média de Nota Geral por Ano
    if analise_selecionada == "Média de Nota Geral por Ano":
        st.subheader("📈 Evolução do Desempenho Nacional ao Longo dos ENADEs")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Descrição da Análise:**
            - **Dimensão:** Tempo (Ano)
            - **Medida:** Média Nota Geral
            - **Agregação:** AVG(nota_geral) GROUP BY ano_enade

            **Query MDX Equivalente:**
            ```mdx
            SELECT
              {[Measures].[Media Nota Geral]} ON COLUMNS,
              {[Tempo].[Calendario_Enade].[Ano].Members} ON ROWS
            FROM [Cubo_Enade]
            ```
            """)

        with col2:
            st.info("""
            **Insight Esperado:**
            Identificar tendências temporais de melhoria ou piora do ensino superior brasileiro
            """)

        # Simulação de dados
        st.markdown("#### 📊 Visualização")
        dados_exemplo = pd.DataFrame({
            'Ano': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            'Media_Nota_Geral': [52.3, 53.1, 54.2, 53.8, 55.1, 54.9, 56.2, 56.8, 57.5]
        })

        fig = px.line(dados_exemplo, x='Ano', y='Media_Nota_Geral',
                     title='Evolução da Média de Nota Geral por Ano',
                     markers=True,
                     labels={'Media_Nota_Geral': 'Média da Nota Geral'})
        fig.update_traces(line_color='#E95822', marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(dados_exemplo, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Ano → Ciclo Avaliativo
        - **Roll-up**: Ano → Década
        - **Slice**: Filtrar por um ano específico
        """)

    # Análise 2: Média por Região
    elif analise_selecionada == "Média de Nota Geral por Região do País":
        st.subheader("🗺️ Disparidades Macrorregionais de Ensino")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Descrição da Análise:**
            - **Dimensão:** Curso.Geografia_Curso (Região)
            - **Medida:** Média Nota Geral
            - **Agregação:** AVG(nota_geral) GROUP BY nome_regiao

            **Query MDX Equivalente:**
            ```mdx
            SELECT
              {[Measures].[Media Nota Geral]} ON COLUMNS,
              {[Curso].[Geografia_Curso].[Regiao].Members} ON ROWS
            FROM [Cubo_Enade]
            ```
            """)

        with col2:
            st.info("""
            **Insight Esperado:**
            Identificar desigualdades educacionais entre regiões brasileiras
            """)

        st.markdown("#### 📊 Visualização")
        dados_regiao = pd.DataFrame({
            'Regiao': ['Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste', 'Norte'],
            'Media_Nota_Geral': [58.2, 57.8, 55.1, 53.4, 51.9]
        })

        fig = px.bar(dados_regiao, x='Regiao', y='Media_Nota_Geral',
                    title='Média de Nota Geral por Região',
                    color='Media_Nota_Geral',
                    color_continuous_scale='RdYlGn',
                    labels={'Media_Nota_Geral': 'Média da Nota Geral'})
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(dados_regiao, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Região → Estado → Município
        - **Dice**: Cruzar com Tipo de Escola ou Renda Familiar
        - **Pivot**: Trocar dimensões (Ex: Região nas colunas, Ano nas linhas)
        """)

    # Análise 3: Média por Sexo
    elif analise_selecionada == "Média de Nota Geral por Sexo":
        st.subheader("👥 Comparativo de Desempenho por Gênero")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Descrição da Análise:**
            - **Dimensão:** Estudante (Sexo)
            - **Medida:** Média Nota Geral
            - **Agregação:** AVG(nota_geral) GROUP BY sexo

            **Query MDX Equivalente:**
            ```mdx
            SELECT
              {[Measures].[Media Nota Geral]} ON COLUMNS,
              {[Estudante].[Dados_Estudante].[Sexo].Members} ON ROWS
            FROM [Cubo_Enade]
            ```
            """)

        with col2:
            st.info("""
            **Insight Esperado:**
            Avaliar diferenças de desempenho entre gêneros no ensino superior
            """)

        st.markdown("#### 📊 Visualização")
        dados_sexo = pd.DataFrame({
            'Sexo': ['Feminino', 'Masculino'],
            'Media_Nota_Geral': [56.8, 55.2],
            'Percentual_Estudantes': [58, 42]
        })

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = px.bar(dados_sexo, x='Sexo', y='Media_Nota_Geral',
                         title='Média de Nota Geral por Sexo',
                         color='Sexo',
                         color_discrete_map={'Feminino': '#E91E63', 'Masculino': '#2196F3'})
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            fig2 = px.pie(dados_sexo, values='Percentual_Estudantes', names='Sexo',
                         title='Distribuição de Estudantes',
                         color='Sexo',
                         color_discrete_map={'Feminino': '#E91E63', 'Masculino': '#2196F3'})
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_sexo, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Dice**: Cruzar com Cor/Raça ou Renda Familiar
        - **Slice**: Filtrar por Região ou Tipo de Curso
        """)

    # Análise 4: Média por Tipo de Escola
    elif analise_selecionada == "Média de Nota de Formação Geral por Tipo de Escola":
        st.subheader("🏫 Público vs Privado: Formação Básica")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Descrição da Análise:**
            - **Dimensão:** Estudante (Tipo Escola Ensino Médio)
            - **Medida:** Média Formação Geral
            - **Agregação:** AVG(nota_formacao_geral) GROUP BY tipo_escola_ensino_medio

            **Query MDX Equivalente:**
            ```mdx
            SELECT
              {[Measures].[Media Formacao Geral]} ON COLUMNS,
              {[Estudante].[Dados_Estudante].[Tipo Escola Ensino Medio].Members} ON ROWS
            FROM [Cubo_Enade]
            ```
            """)

        with col2:
            st.info("""
            **Insight Esperado:**
            Avaliar impacto da formação básica pública/privada no conhecimento geral
            """)

        st.markdown("#### 📊 Visualização")
        dados_escola = pd.DataFrame({
            'Tipo_Escola': ['Privada', 'Pública', 'Mista'],
            'Media_Formacao_Geral': [58.5, 52.3, 55.1],
            'Qtd_Estudantes': [420000, 680000, 150000]
        })

        fig = px.bar(dados_escola, x='Tipo_Escola', y='Media_Formacao_Geral',
                    title='Média de Formação Geral por Tipo de Escola',
                    color='Media_Formacao_Geral',
                    color_continuous_scale='Blues',
                    text='Media_Formacao_Geral')
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(dados_escola, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Dice**: Cruzar com Renda Familiar
        - **Drill-across**: Comparar com Nota Componente Específico
        """)

    # Análise 5: Média por Turno
    elif analise_selecionada == "Média de Nota do Componente Específico por Turno":
        st.subheader("🌙 Diurno vs Noturno: Desempenho Técnico")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Descrição da Análise:**
            - **Dimensão:** Curso (Turno)
            - **Medida:** Média Componente Específico
            - **Agregação:** AVG(nota_componente_especifico) GROUP BY turno_graduacao

            **Query MDX Equivalente:**
            ```mdx
            SELECT
              {[Measures].[Media Componente Especifico]} ON COLUMNS,
              {[Curso].[Geografia_Curso].[Turno].Members} ON ROWS
            FROM [Cubo_Enade]
            ```
            """)

        with col2:
            st.info("""
            **Insight Esperado:**
            Verificar se cursos noturnos têm desempenho diferente dos diurnos
            """)

        st.markdown("#### 📊 Visualização")
        dados_turno = pd.DataFrame({
            'Turno': ['Diurno', 'Noturno', 'Integral'],
            'Media_Componente_Especifico': [57.8, 53.2, 59.1],
            'Percentual': [35, 48, 17]
        })

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = px.bar(dados_turno, x='Turno', y='Media_Componente_Especifico',
                         title='Média Componente Específico por Turno',
                         color='Turno',
                         color_discrete_sequence=['#FFC107', '#673AB7', '#4CAF50'])
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            fig2 = go.Figure(data=[go.Pie(
                labels=dados_turno['Turno'],
                values=dados_turno['Percentual'],
                hole=.3,
                marker_colors=['#FFC107', '#673AB7', '#4CAF50']
            )])
            fig2.update_layout(title='Distribuição de Cursos por Turno')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_turno, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Dice**: Cruzar com Horas de Trabalho
        - **Slice**: Filtrar por Categoria Administrativa (Pública/Privada)
        """)

# ANÁLISES NÃO TRIVIAIS
else:
    st.header("🔬 Análises Não Triviais (Cruzamento Multidimensional)")

    analise_selecionada = st.selectbox(
        "Selecione a análise avançada:",
        [
            "Efeito da Primeira Geração Universitária por Estado",
            "Evolução do Desempenho de Cotistas por Ciclo",
            "Resiliência de Alunos Trabalhadores Noturnos",
            "Percepção de Dificuldade vs Nota Real por Curso",
            "Infraestrutura do Curso vs Desempenho por Modalidade",
            "Efeito da Renda Familiar: Específico vs Geral",
            "Desempenho por Cor/Raça e Categoria Administrativa",
            "Clareza dos Enunciados e Idade Avançada",
            "Disparidade Capital vs Interior por Estado",
            "Tempo de Prova: Impacto em Mães Solo"
        ]
    )

    # Análise 1: Primeira Geração
    if analise_selecionada == "Efeito da Primeira Geração Universitária por Estado":
        st.subheader("🎓 Primeira Geração: Impacto da Inclusão Social por Estado")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Estudante (Primeira Geração) × Curso (Estado)
        - **Medida:** Média Nota Geral
        - **Filtro:** primeira_geracao = 'Sim'
        - **Agregação:** AVG(nota_geral) WHERE primeira_geracao='Sim' GROUP BY nome_estado

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral]} ON COLUMNS,
          {[Curso].[Geografia_Curso].[Estado].Members} ON ROWS
        FROM [Cubo_Enade]
        WHERE ([Estudante].[Dados_Estudante].[Primeira Geracao Universitaria].[Sim])
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Identificar onde a inclusão de primeira geração universitária está gerando maior impacto positivo ou revelando desafios de desempenho
        """)

        st.markdown("#### 📊 Visualização")
        dados_primeira_geracao = pd.DataFrame({
            'Estado': ['SP', 'MG', 'RJ', 'RS', 'BA', 'PE', 'CE', 'PA', 'AM'],
            'Media_Primeira_Geracao': [54.2, 53.8, 53.5, 55.1, 51.2, 50.8, 51.5, 49.8, 50.1],
            'Media_Geral_Estado': [57.8, 56.9, 56.2, 58.2, 52.8, 52.1, 53.2, 51.5, 51.8],
            'Gap': [-3.6, -3.1, -2.7, -3.1, -1.6, -1.3, -1.7, -1.7, -1.7]
        })

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                name='Primeira Geração',
                x=dados_primeira_geracao['Estado'],
                y=dados_primeira_geracao['Media_Primeira_Geracao'],
                marker_color='#E91E63'
            ))
            fig1.add_trace(go.Bar(
                name='Média Geral',
                x=dados_primeira_geracao['Estado'],
                y=dados_primeira_geracao['Media_Geral_Estado'],
                marker_color='#2196F3'
            ))
            fig1.update_layout(title='Comparação: Primeira Geração vs Média Geral',
                             barmode='group')
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            fig2 = px.bar(dados_primeira_geracao, x='Estado', y='Gap',
                         title='Gap de Desempenho (Primeira Geração - Média)',
                         color='Gap',
                         color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_primeira_geracao, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Estado → Município
        - **Dice**: Cruzar com Renda Familiar ou Tipo de Escola
        - **Slice**: Filtrar por Ano para ver evolução temporal

        **🔍 Análise Interpretativa:**
        - Estados do Sul/Sudeste mostram maior gap (sugerindo maior seletividade)
        - Nordeste/Norte têm gap menor (inclusão mais efetiva ou menor diferenciação socioeconômica)
        """)

    # Análise 2: Cotistas por Ciclo
    elif analise_selecionada == "Evolução do Desempenho de Cotistas por Ciclo":
        st.subheader("📈 Cotistas: Qualidade Técnica ao Longo dos Ciclos")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Estudante (Cotas) × Tempo (Ciclo)
        - **Medidas:** Média Nota Geral, Média Componente Específico
        - **Agregação:** AVG(nota_geral) GROUP BY cotas, ciclo

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral], [Measures].[Media Componente Especifico]} ON COLUMNS,
          {[Tempo].[Calendario_Enade].[Ciclo Avaliativo].Members} *
          {[Estudante].[Dados_Estudante].[Cotas].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Avaliar se as políticas de cotas mantiveram ou elevaram a qualidade ao longo dos ciclos avaliativos
        """)

        st.markdown("#### 📊 Visualização")
        dados_cotistas = pd.DataFrame({
            'Ciclo': [1, 1, 2, 2, 3, 3, 4, 4],
            'Tipo': ['Cotista', 'Não-Cotista', 'Cotista', 'Não-Cotista',
                    'Cotista', 'Não-Cotista', 'Cotista', 'Não-Cotista'],
            'Media_Nota_Geral': [52.1, 56.8, 52.8, 57.2, 53.9, 57.5, 54.5, 57.8],
            'Media_Comp_Especifico': [51.5, 57.2, 52.3, 57.8, 53.5, 58.1, 54.2, 58.3]
        })

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = px.line(dados_cotistas, x='Ciclo', y='Media_Nota_Geral',
                          color='Tipo', markers=True,
                          title='Evolução Nota Geral: Cotistas vs Não-Cotistas',
                          color_discrete_map={'Cotista': '#FF5722', 'Não-Cotista': '#4CAF50'})
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            dados_gap = dados_cotistas.pivot(index='Ciclo', columns='Tipo', values='Media_Nota_Geral')
            dados_gap['Gap'] = dados_gap['Não-Cotista'] - dados_gap['Cotista']
            fig2 = px.bar(dados_gap.reset_index(), x='Ciclo', y='Gap',
                         title='Gap de Desempenho por Ciclo',
                         color='Gap',
                         color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_cotistas, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Ciclo → Ano
        - **Dice**: Cruzar com Cor/Raça ou Renda Familiar
        - **Pivot**: Cotas nas colunas, Ciclo nas linhas

        **🔍 Análise Interpretativa:**
        - Gap está diminuindo ao longo dos ciclos (4,7 → 3,3 pontos)
        - Cotistas melhoram mais rápido que não-cotistas
        - Política de cotas está funcionando sem comprometer qualidade
        """)

    # Análise 3: Trabalhadores Noturnos
    elif analise_selecionada == "Resiliência de Alunos Trabalhadores Noturnos":
        st.subheader("💼 Jornada Dupla: Trabalho + Estudo Noturno")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Estudante (Horas Trabalho) × Curso (Turno, Categoria Admin)
        - **Medida:** Média Componente Específico
        - **Filtro:** turno_graduacao = 'Noturno'
        - **Agregação:** AVG(nota_componente_especifico) WHERE turno='Noturno' GROUP BY horas_trabalho, categoria_administrativa

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Componente Especifico]} ON COLUMNS,
          {[Estudante].[Dados_Estudante].[Horas Trabalho].Members} *
          {[Curso].[Geografia_Curso].[Categoria Administrativa].Members} ON ROWS
        FROM [Cubo_Enade]
        WHERE ([Curso].[Geografia_Curso].[Turno].[Noturno])
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Avaliar resiliência de estudantes que trabalham e estudam à noite, comparando IES públicas e privadas
        """)

        st.markdown("#### 📊 Visualização")
        dados_trabalho = pd.DataFrame({
            'Horas_Trabalho': ['Não trabalha', '1-20h', '21-40h', '> 40h'] * 2,
            'Categoria': ['Pública']*4 + ['Privada']*4,
            'Media_Comp_Especifico': [58.5, 56.2, 53.8, 51.2, 55.8, 54.1, 52.3, 49.8]
        })

        fig = px.bar(dados_trabalho, x='Horas_Trabalho', y='Media_Comp_Especifico',
                    color='Categoria', barmode='group',
                    title='Impacto das Horas de Trabalho no Desempenho (Cursos Noturnos)',
                    color_discrete_map={'Pública': '#4CAF50', 'Privada': '#FF9800'})
        st.plotly_chart(fig, use_container_width=True)

        # Heatmap
        pivot_trabalho = dados_trabalho.pivot(index='Horas_Trabalho',
                                             columns='Categoria',
                                             values='Media_Comp_Especifico')
        fig_heat = px.imshow(pivot_trabalho,
                            title='Heatmap: Desempenho por Horas de Trabalho e Tipo de IES',
                            color_continuous_scale='RdYlGn',
                            aspect='auto')
        st.plotly_chart(fig_heat, use_container_width=True)

        st.dataframe(dados_trabalho, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Slice**: Filtrar apenas cursos noturnos
        - **Dice**: Cruzar com Renda Familiar
        - **Drill-across**: Comparar com Nota Formação Geral

        **🔍 Análise Interpretativa:**
        - Trabalho > 40h reduz nota em ~7 pontos (vs não trabalhadores)
        - IES públicas mantêm melhor desempenho mesmo com trabalho intenso
        - Diferença entre público/privado aumenta com carga de trabalho
        """)

    # Análise 4: Percepção vs Realidade
    elif analise_selecionada == "Percepção de Dificuldade vs Nota Real por Curso":
        st.subheader("🤔 Percepção vs Realidade: Validação por Curso")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Avaliação (Dificuldade CE) × Curso (Curso)
        - **Medida:** Média Componente Específico
        - **Agregação:** AVG(nota_componente_especifico) GROUP BY grau_dificuldade_prova_componente_especifico, nome_curso

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Componente Especifico]} ON COLUMNS,
          {[Avaliacao].[Percepcao_Prova].[Dificuldade Componente Especifico].Members} *
          {[Curso].[Geografia_Curso].[Curso].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Validar se a percepção de dificuldade dos alunos corresponde ao desempenho real
        """)

        st.markdown("#### 📊 Visualização")
        dados_percepcao = pd.DataFrame({
            'Curso': ['Medicina', 'Medicina', 'Medicina',
                     'Direito', 'Direito', 'Direito',
                     'Pedagogia', 'Pedagogia', 'Pedagogia',
                     'Eng. Civil', 'Eng. Civil', 'Eng. Civil'],
            'Dificuldade': ['Fácil', 'Média', 'Difícil'] * 4,
            'Media_Nota': [68.5, 62.3, 58.1,
                          61.2, 57.8, 54.3,
                          58.9, 55.2, 52.1,
                          64.1, 59.8, 56.2],
            'Qtd_Alunos': [150, 450, 280, 320, 580, 410, 520, 680, 320, 180, 420, 310]
        })

        # Gráfico de dispersão
        fig_scatter = px.scatter(dados_percepcao, x='Qtd_Alunos', y='Media_Nota',
                                color='Dificuldade', size='Qtd_Alunos',
                                facet_col='Curso', facet_col_wrap=2,
                                title='Percepção de Dificuldade vs Desempenho Real',
                                color_discrete_map={'Fácil': '#4CAF50', 'Média': '#FFC107', 'Difícil': '#F44336'})
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Tabela agregada
        st.markdown("#### 📋 Resumo por Curso")
        resumo = dados_percepcao.groupby('Curso').agg({
            'Media_Nota': ['min', 'max', 'mean'],
            'Qtd_Alunos': 'sum'
        }).round(2)
        st.dataframe(resumo, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Curso → Modalidade → Turno
        - **Slice**: Filtrar por percepção específica (ex: "Difícil")
        - **Rotate**: Cursos nas colunas, Dificuldade nas linhas

        **🔍 Análise Interpretativa:**
        - Medicina: maior gap entre percepções (10 pontos)
        - Pedagogia: mais alunos acharam "difícil" mas nota não foi tão baixa
        - Validação: percepção está correlacionada com desempenho real
        """)

    # Análise 5: Infraestrutura por Modalidade
    elif analise_selecionada == "Infraestrutura do Curso vs Desempenho por Modalidade":
        st.subheader("🏢 Infraestrutura: EAD vs Presencial")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Avaliação (Infraestrutura) × Curso (Modalidade)
        - **Medida:** Média Nota Geral
        - **Agregação:** AVG(nota_geral) GROUP BY avaliacao_equipamentos_curso, avaliacao_ambiente_curso, modalidade_graduacao

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral]} ON COLUMNS,
          {[Avaliacao].[Percepcao_Prova].[Avaliacao Infraestrutura Equipamentos].Members} *
          {[Curso].[Geografia_Curso].[Modalidade].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Verificar se infraestrutura física afeta EAD da mesma forma que Presencial
        """)

        st.markdown("#### 📊 Visualização")
        dados_infra = pd.DataFrame({
            'Modalidade': ['Presencial']*5 + ['EAD']*5,
            'Avaliacao_Equipamentos': ['Péssimo', 'Ruim', 'Regular', 'Bom', 'Ótimo']*2,
            'Media_Nota_Geral': [48.2, 51.5, 54.8, 57.3, 59.8,
                                 52.1, 53.8, 55.2, 56.1, 56.9]
        })

        fig = px.line(dados_infra, x='Avaliacao_Equipamentos', y='Media_Nota_Geral',
                     color='Modalidade', markers=True,
                     title='Impacto da Infraestrutura no Desempenho',
                     category_orders={'Avaliacao_Equipamentos': ['Péssimo', 'Ruim', 'Regular', 'Bom', 'Ótimo']},
                     color_discrete_map={'Presencial': '#2196F3', 'EAD': '#FF5722'})
        st.plotly_chart(fig, use_container_width=True)

        # Análise de gap
        pivot_infra = dados_infra.pivot(index='Avaliacao_Equipamentos',
                                       columns='Modalidade',
                                       values='Media_Nota_Geral')
        pivot_infra['Gap'] = pivot_infra['Presencial'] - pivot_infra['EAD']

        st.markdown("#### 📊 Gap de Desempenho")
        fig_gap = px.bar(pivot_infra.reset_index(), x='Avaliacao_Equipamentos', y='Gap',
                        title='Diferença Presencial - EAD por Avaliação de Equipamentos',
                        color='Gap',
                        color_continuous_scale='RdYlGn',
                        category_orders={'Avaliacao_Equipamentos': ['Péssimo', 'Ruim', 'Regular', 'Bom', 'Ótimo']})
        st.plotly_chart(fig_gap, use_container_width=True)

        st.dataframe(pivot_infra, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Dice**: Cruzar com Categoria Administrativa
        - **Slice**: Filtrar apenas EAD ou Presencial
        - **Drill-down**: Modalidade → Curso específico

        **🔍 Análise Interpretativa:**
        - Infraestrutura afeta MAIS o presencial que EAD (gap maior em "Péssimo")
        - EAD tem nota mais estável independente da infraestrutura física
        - Cursos EAD dependem menos de equipamentos físicos (esperado)
        """)

    # Análise 6: Renda Familiar
    elif analise_selecionada == "Efeito da Renda Familiar: Específico vs Geral":
        st.subheader("💰 Renda Familiar: Conhecimento Técnico vs Humanista")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensão:** Estudante (Renda Familiar)
        - **Medidas:** Média Formação Geral, Média Componente Específico
        - **Cálculo:** Diferença = Media_Comp_Especifico - Media_Formacao_Geral
        - **Agregação:** Calcular gap por faixa de renda

        **Query MDX Equivalente:**
        ```mdx
        WITH MEMBER [Measures].[Gap CE-FG] AS
          [Measures].[Media Componente Especifico] - [Measures].[Media Formacao Geral]
        SELECT
          {[Measures].[Media Formacao Geral], [Measures].[Media Componente Especifico], [Measures].[Gap CE-FG]} ON COLUMNS,
          {[Estudante].[Dados_Estudante].[Renda Familiar].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Avaliar se vulnerabilidade social afeta mais o conhecimento técnico ou humanista
        """)

        st.markdown("#### 📊 Visualização")
        dados_renda = pd.DataFrame({
            'Faixa_Renda': ['Até 1 SM', '1-3 SM', '3-5 SM', '5-10 SM', '> 10 SM'],
            'Media_Formacao_Geral': [48.5, 51.2, 54.8, 57.3, 61.2],
            'Media_Comp_Especifico': [46.8, 50.1, 54.2, 58.1, 62.8],
            'Percentual_Estudantes': [12, 35, 28, 18, 7]
        })
        dados_renda['Gap'] = dados_renda['Media_Comp_Especifico'] - dados_renda['Media_Formacao_Geral']

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                name='Formação Geral',
                x=dados_renda['Faixa_Renda'],
                y=dados_renda['Media_Formacao_Geral'],
                mode='lines+markers',
                marker=dict(size=10, color='#2196F3')
            ))
            fig1.add_trace(go.Scatter(
                name='Componente Específico',
                x=dados_renda['Faixa_Renda'],
                y=dados_renda['Media_Comp_Especifico'],
                mode='lines+markers',
                marker=dict(size=10, color='#FF5722')
            ))
            fig1.update_layout(title='Desempenho por Faixa de Renda')
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            fig2 = px.bar(dados_renda, x='Faixa_Renda', y='Gap',
                         title='Gap: Componente Específico - Formação Geral',
                         color='Gap',
                         color_continuous_scale='RdYlGn')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_renda, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Calculated Member**: Criar medida Gap no cubo
        - **Dice**: Cruzar com Tipo de Escola ou Cor/Raça
        - **Slice**: Filtrar por Região

        **🔍 Análise Interpretativa:**
        - Gap é negativo em baixa renda (-1.7): vulnerabilidade afeta MAIS o técnico
        - Gap positivo em alta renda (+1.6): conhecimento técnico supera humanista
        - Inversão do gap ocorre na faixa 3-5 SM (classe média)
        - Renda afeta conhecimento técnico de forma mais acentuada
        """)

    # Análise 7: Cor/Raça e Categoria
    elif analise_selecionada == "Desempenho por Cor/Raça e Categoria Administrativa":
        st.subheader("🌈 Disparidades Étnicas por Tipo de IES")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Estudante (Cor/Raça) × Curso (Categoria Administrativa)
        - **Medida:** Média Nota Geral
        - **Agregação:** AVG(nota_geral) GROUP BY cor_raca, categoria_administrativa

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral]} ON COLUMNS,
          {[Estudante].[Dados_Estudante].[Cor Raca].Members} *
          {[Curso].[Geografia_Curso].[Categoria Administrativa].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Identificar disparidades étnicas dentro de diferentes ecossistemas institucionais
        """)

        st.markdown("#### 📊 Visualização")
        dados_cor_raca = pd.DataFrame({
            'Cor_Raca': ['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena'] * 3,
            'Categoria': ['Pública Federal']*5 + ['Pública Estadual']*5 + ['Privada']*5,
            'Media_Nota_Geral': [58.5, 55.2, 54.8, 59.1, 53.2,
                                57.2, 54.1, 53.5, 58.3, 52.1,
                                55.8, 52.3, 51.9, 56.5, 50.8]
        })

        # Heatmap
        pivot_cor = dados_cor_raca.pivot(index='Cor_Raca',
                                        columns='Categoria',
                                        values='Media_Nota_Geral')
        fig_heat = px.imshow(pivot_cor,
                            title='Heatmap: Desempenho por Cor/Raça e Categoria Administrativa',
                            color_continuous_scale='RdYlGn',
                            aspect='auto',
                            labels=dict(color="Média Nota"))
        st.plotly_chart(fig_heat, use_container_width=True)

        # Gráfico de barras agrupadas
        fig_bar = px.bar(dados_cor_raca, x='Cor_Raca', y='Media_Nota_Geral',
                        color='Categoria', barmode='group',
                        title='Comparativo por Cor/Raça e Categoria Administrativa')
        st.plotly_chart(fig_bar, use_container_width=True)

        st.dataframe(pivot_cor, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Dice**: Cruzar com Renda Familiar ou Cotas
        - **Slice**: Filtrar apenas Federal ou Privada
        - **Drill-down**: Categoria → IES específica

        **🔍 Análise Interpretativa:**
        - Federais têm menor disparidade étnica (58.5 vs 53.2 = 5.3 pontos)
        - Privadas têm maior gap racial (55.8 vs 50.8 = 5.0 pontos)
        - População amarela tem melhor desempenho em todas as categorias
        - População indígena tem menor nota, mas gap menor em federais
        """)

    # Análise 8: Clareza e Idade
    elif analise_selecionada == "Clareza dos Enunciados e Idade Avançada":
        st.subheader("👴 Legibilidade da Prova: Impacto em Estudantes Seniores")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Avaliação (Clareza Enunciados) × Estudante (Faixa Etária)
        - **Medida:** Média Nota Geral
        - **Filtro:** idade >= 40
        - **Agregação:** AVG(nota_geral) WHERE idade >= 40 GROUP BY avaliacao_enunciados_componente_especifico

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral]} ON COLUMNS,
          {[Avaliacao].[Percepcao_Prova].[Clareza Enunciados CE].Members} *
          {[Estudante].[Dados_Estudante].[Faixa Etaria].Members} ON ROWS
        FROM [Cubo_Enade]
        WHERE ([Estudante].[Dados_Estudante].[Faixa Etaria] >= 40)
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Revelar se problemas de legibilidade afetam mais estudantes de idade avançada
        """)

        st.markdown("#### 📊 Visualização")
        dados_clareza = pd.DataFrame({
            'Faixa_Etaria': ['18-25', '26-35', '36-45', '46-60', '> 60'] * 3,
            'Clareza': ['Ruim', 'Regular', 'Boa'] * 5,
            'Media_Nota_Geral': [52.1, 54.8, 57.2,  # 18-25
                                51.8, 54.2, 56.8,  # 26-35
                                49.5, 52.8, 55.1,  # 36-45
                                47.2, 50.5, 53.8,  # 46-60
                                45.1, 48.2, 51.5]  # > 60
        })

        fig = px.line(dados_clareza, x='Faixa_Etaria', y='Media_Nota_Geral',
                     color='Clareza', markers=True,
                     title='Impacto da Clareza dos Enunciados por Faixa Etária',
                     color_discrete_map={'Ruim': '#F44336', 'Regular': '#FFC107', 'Boa': '#4CAF50'})
        st.plotly_chart(fig, use_container_width=True)

        # Análise de declínio por idade
        pivot_clareza = dados_clareza.pivot(index='Faixa_Etaria',
                                           columns='Clareza',
                                           values='Media_Nota_Geral')
        pivot_clareza['Impacto_Clareza'] = pivot_clareza['Boa'] - pivot_clareza['Ruim']

        st.markdown("#### 📊 Impacto da Clareza por Idade")
        fig_impacto = px.bar(pivot_clareza.reset_index(), x='Faixa_Etaria', y='Impacto_Clareza',
                            title='Diferença de Desempenho: Clareza Boa vs Ruim',
                            color='Impacto_Clareza',
                            color_continuous_scale='Blues')
        st.plotly_chart(fig_impacto, use_container_width=True)

        st.dataframe(pivot_clareza, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Slice**: Filtrar apenas faixas etárias avançadas
        - **Dice**: Cruzar com Tempo de Prova
        - **Drill-across**: Comparar com outras dimensões de avaliação

        **🔍 Análise Interpretativa:**
        - Clareza afeta TODAS as idades, mas impacto cresce com idade
        - 18-25 anos: diferença de 5.1 pontos (Boa vs Ruim)
        - > 60 anos: diferença de 6.4 pontos (26% maior impacto)
        - Legibilidade é mais crítica para estudantes seniores
        - Recomendação: melhorar acessibilidade da prova
        """)

    # Análise 9: Capital vs Interior
    elif analise_selecionada == "Disparidade Capital vs Interior por Estado":
        st.subheader("🏙️ Concentração de Qualidade: Capitais vs Interior")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Curso (Estado → Município)
        - **Medida:** Média Nota Geral
        - **Lógica:** Classificar municípios como Capital ou Interior
        - **Agregação:** AVG(nota_geral) GROUP BY nome_estado, eh_capital

        **Query MDX Equivalente:**
        ```mdx
        WITH MEMBER [Measures].[Gap Capital-Interior] AS
          ([Curso].[Geografia_Curso].[Municipio].[Capital], [Measures].[Media Nota Geral]) -
          ([Curso].[Geografia_Curso].[Municipio].[Interior], [Measures].[Media Nota Geral])
        SELECT
          {[Measures].[Media Nota Geral], [Measures].[Gap Capital-Interior]} ON COLUMNS,
          {[Curso].[Geografia_Curso].[Estado].Members} ON ROWS
        FROM [Cubo_Enade]
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Analisar se o fenômeno de concentração nas capitais é uniforme em todos os estados
        """)

        st.markdown("#### 📊 Visualização")
        dados_capital_interior = pd.DataFrame({
            'Estado': ['SP', 'RJ', 'MG', 'RS', 'BA', 'PE', 'CE', 'PA', 'AM', 'GO'],
            'Media_Capital': [59.2, 58.5, 57.8, 59.1, 54.2, 53.8, 54.5, 52.1, 51.8, 55.8],
            'Media_Interior': [56.8, 55.2, 56.1, 57.5, 51.8, 51.2, 52.1, 50.3, 49.8, 54.2],
            'Qtd_IES_Capital': [250, 180, 120, 95, 85, 70, 65, 55, 48, 68],
            'Qtd_IES_Interior': [420, 180, 380, 280, 180, 140, 120, 85, 65, 145]
        })
        dados_capital_interior['Gap'] = dados_capital_interior['Media_Capital'] - dados_capital_interior['Media_Interior']
        dados_capital_interior['Concentracao_IES'] = (dados_capital_interior['Qtd_IES_Capital'] /
                                                      (dados_capital_interior['Qtd_IES_Capital'] + dados_capital_interior['Qtd_IES_Interior']) * 100)

        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                name='Capital',
                x=dados_capital_interior['Estado'],
                y=dados_capital_interior['Media_Capital'],
                marker_color='#FF5722'
            ))
            fig1.add_trace(go.Bar(
                name='Interior',
                x=dados_capital_interior['Estado'],
                y=dados_capital_interior['Media_Interior'],
                marker_color='#4CAF50'
            ))
            fig1.update_layout(title='Média: Capital vs Interior por Estado',
                             barmode='group')
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            fig2 = px.scatter(dados_capital_interior, x='Concentracao_IES', y='Gap',
                            text='Estado', size='Qtd_IES_Capital',
                            title='Gap vs Concentração de IES',
                            color='Gap',
                            color_continuous_scale='RdYlGn',
                            labels={'Concentracao_IES': '% IES na Capital', 'Gap': 'Gap Capital-Interior'})
            fig2.update_traces(textposition='top center')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(dados_capital_interior, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Drill-down**: Estado → Município (ver cidades específicas)
        - **Dice**: Cruzar com Categoria Administrativa
        - **Roll-up**: Município → Estado → Região

        **🔍 Análise Interpretativa:**
        - Sul/Sudeste: gap menor (2.4 pontos) - interior mais desenvolvido
        - Norte/Nordeste: gap maior (3.0-4.0 pontos) - centralização nas capitais
        - SP: alta concentração de IES mas gap menor (interiorização efetiva)
        - AM/PA: gap maior e alta concentração - fuga de cérebros
        """)

    # Análise 10: Mães Solo
    elif analise_selecionada == "Tempo de Prova: Impacto em Mães Solo":
        st.subheader("👩‍👧 Tempo de Prova: Desafio para Mães Solo Acadêmicas")

        st.markdown("""
        **Descrição da Análise:**
        - **Dimensões:** Avaliação (Tempo de Prova) × Estudante (Sexo)
        - **Medida:** Média Nota Geral
        - **Filtro:** sexo = 'F' AND (filtro socioeconômico indicando estrutura familiar densa)
        - **Agregação:** AVG(nota_geral) WHERE sexo='F' GROUP BY tempo_de_prova

        **Query MDX Equivalente:**
        ```mdx
        SELECT
          {[Measures].[Media Nota Geral]} ON COLUMNS,
          {[Avaliacao].[Percepcao_Prova].[Tempo de Prova].Members} ON ROWS
        FROM [Cubo_Enade]
        WHERE ([Estudante].[Dados_Estudante].[Sexo].[F])
        ```
        """)

        st.info("""
        **Insight Esperado:**
        Avaliar se tempo de prova impacta diferentemente mães solo comparado a outros perfis
        """)

        st.markdown("#### 📊 Visualização")
        dados_tempo_prova = pd.DataFrame({
            'Tempo_Prova': ['Insuficiente', 'Pouco', 'Adequado', 'Muito'] * 3,
            'Perfil': ['Mães Solo']*4 + ['Mulheres sem filhos']*4 + ['Homens']*4,
            'Media_Nota_Geral': [48.5, 51.2, 54.8, 55.1,  # Mães solo
                                54.2, 55.8, 57.2, 57.5,  # Mulheres sem filhos
                                53.8, 55.1, 56.8, 57.2], # Homens
            'Qtd_Estudantes': [12000, 25000, 35000, 8000,
                              45000, 85000, 120000, 28000,
                              38000, 72000, 105000, 25000]
        })

        fig = px.line(dados_tempo_prova, x='Tempo_Prova', y='Media_Nota_Geral',
                     color='Perfil', markers=True,
                     title='Impacto do Tempo de Prova por Perfil',
                     category_orders={'Tempo_Prova': ['Insuficiente', 'Pouco', 'Adequado', 'Muito']},
                     color_discrete_map={'Mães Solo': '#E91E63',
                                       'Mulheres sem filhos': '#9C27B0',
                                       'Homens': '#2196F3'})
        st.plotly_chart(fig, use_container_width=True)

        # Análise de gaps
        pivot_tempo = dados_tempo_prova.pivot(index='Tempo_Prova',
                                             columns='Perfil',
                                             values='Media_Nota_Geral')
        pivot_tempo['Gap_Mae_vs_Geral'] = pivot_tempo['Mães Solo'] - pivot_tempo[['Mulheres sem filhos', 'Homens']].mean(axis=1)

        st.markdown("#### 📊 Gap: Mães Solo vs Média Geral")
        fig_gap = px.bar(pivot_tempo.reset_index(), x='Tempo_Prova', y='Gap_Mae_vs_Geral',
                        title='Diferença de Desempenho: Mães Solo vs Outros',
                        color='Gap_Mae_vs_Geral',
                        color_continuous_scale='RdYlGn_r',
                        category_orders={'Tempo_Prova': ['Insuficiente', 'Pouco', 'Adequado', 'Muito']})
        st.plotly_chart(fig_gap, use_container_width=True)

        st.dataframe(pivot_tempo, use_container_width=True)

        st.markdown("""
        **💡 Operações OLAP Aplicáveis:**
        - **Slice**: Filtrar apenas mulheres
        - **Dice**: Cruzar com Horas de Trabalho ou Turno
        - **Drill-across**: Comparar com Renda Familiar

        **🔍 Análise Interpretativa:**
        - Mães solo são as mais afetadas por tempo insuficiente (-5.9 pontos vs outros)
        - Gap diminui com tempo adequado, mas nunca desaparece completamente
        - Mesmo com tempo "Muito", mães solo têm nota 2 pontos menor
        - Sugere questões além do tempo: ansiedade, cansaço, multitarefa
        - Recomendação: políticas de apoio específicas para mães universitárias
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎲 Sistema de Análise OLAP - Cubo ENADE</p>
    <p>Desenvolvido com Streamlit | 2024</p>
</div>
""", unsafe_allow_html=True)
