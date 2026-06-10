# 📊 Sistema de Análise OLAP - Cubo ENADE

Sistema interativo de análise multidimensional do ENADE usando Streamlit, baseado no cubo de dados OLAP.

## 🎯 Objetivo

Substituir o Saiku Analytics por uma interface Streamlit para análises triviais e não triviais do cubo ENADE, seguindo as orientações do material didático MD12.

## 📦 Estrutura do Cubo

### Dimensões
- **👤 Estudante**: Perfil socioeconômico (sexo, cor/raça, renda, escolaridade dos pais, cotas, etc.)
- **🎓 Curso**: Geografia (região, estado, município) e características (modalidade, turno, categoria administrativa)
- **📝 Avaliação**: Percepção da prova (dificuldade, clareza, infraestrutura, tempo)
- **📅 Tempo**: Ciclos avaliativos (década, ano, ciclo)

### Medidas
- **📈 Média Nota Geral**: `AVG(nota_geral)`
- **📘 Média Formação Geral**: `AVG(nota_formacao_geral)`
- **📕 Média Componente Específico**: `AVG(nota_componente_especifico)`

## 🔍 Análises Implementadas

### Análises Triviais (1 dimensão)
1. ✅ **Média de Nota Geral por Ano**
   - Evolução temporal do desempenho nacional
   - Operações: Drill-down (Ano → Ciclo), Roll-up (Ano → Década)

2. ✅ **Média de Nota Geral por Região**
   - Disparidades macrorregionais de ensino
   - Operações: Drill-down (Região → Estado → Município)

3. ✅ **Média de Nota Geral por Sexo**
   - Comparativo de desempenho por gênero
   - Operações: Dice (cruzar com Cor/Raça ou Renda)

4. ✅ **Média de Formação Geral por Tipo de Escola**
   - Público vs Privado: impacto da formação básica
   - Operações: Dice (cruzar com Renda Familiar)

5. ✅ **Média Componente Específico por Turno**
   - Diurno vs Noturno: desempenho técnico
   - Operações: Slice (filtrar por Categoria Administrativa)

### Análises Não Triviais (2+ dimensões)

1. ✅ **Efeito da Primeira Geração Universitária por Estado**
   - Dimensões: Estudante (Primeira Geração) × Curso (Estado)
   - Insight: Onde a inclusão social gera maior impacto

2. ✅ **Evolução do Desempenho de Cotistas por Ciclo**
   - Dimensões: Estudante (Cotas) × Tempo (Ciclo)
   - Insight: Políticas de cotas mantiveram qualidade?

3. ✅ **Resiliência de Alunos Trabalhadores Noturnos**
   - Dimensões: Estudante (Horas Trabalho) × Curso (Turno, Categoria)
   - Insight: Impacto da jornada dupla no desempenho técnico

4. ✅ **Percepção de Dificuldade vs Nota Real por Curso**
   - Dimensões: Avaliação (Dificuldade) × Curso (Curso)
   - Insight: Validação de percepção dos alunos

5. ✅ **Infraestrutura do Curso vs Desempenho por Modalidade**
   - Dimensões: Avaliação (Infraestrutura) × Curso (Modalidade)
   - Insight: EAD depende menos de infraestrutura física?

6. ✅ **Efeito da Renda: Conhecimento Específico vs Geral**
   - Dimensão: Estudante (Renda Familiar)
   - Medida Calculada: Gap = CE - FG
   - Insight: Vulnerabilidade afeta mais o técnico ou humanista?

7. ✅ **Desempenho por Cor/Raça e Categoria Administrativa**
   - Dimensões: Estudante (Cor/Raça) × Curso (Categoria Admin)
   - Insight: Disparidades étnicas por ecossistema institucional

8. ✅ **Clareza dos Enunciados e Idade Avançada**
   - Dimensões: Avaliação (Clareza) × Estudante (Idade)
   - Insight: Legibilidade afeta mais estudantes seniores?

9. ✅ **Disparidade Capital vs Interior por Estado**
   - Dimensão: Curso (Estado → Município)
   - Insight: Concentração de qualidade nas capitais é uniforme?

10. ✅ **Tempo de Prova: Impacto em Mães Solo**
    - Dimensões: Avaliação (Tempo) × Estudante (Sexo + perfil familiar)
    - Insight: Tempo afeta diferentemente mães solo?

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
cd C:\Users\valcann\Downloads\analise-enade-streamlit
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

### 3. Acessar no Navegador

A aplicação abrirá automaticamente em:
```
http://localhost:8501
```

## 📊 Operações OLAP Implementadas

### Operações Básicas
- **Slice**: Filtrar uma dimensão específica (ex: apenas ano 2022)
- **Dice**: Cruzar múltiplas dimensões (ex: Sexo × Região)
- **Roll-up**: Agregar para nível superior (Município → Estado → Região)
- **Drill-down**: Detalhar para nível inferior (Ano → Mês)
- **Pivot**: Rotacionar dimensões (linhas ↔ colunas)

### Operações Avançadas
- **Calculated Members**: Criar medidas derivadas (Gap, Diferenças)
- **Drill-across**: Comparar medidas diferentes na mesma dimensão
- **Drill-through**: Ver registros detalhados por trás de uma célula

## 📐 Equivalência MDX

Cada análise possui sua query MDX equivalente documentada, facilitando:
- Migração para outras ferramentas OLAP (Mondrian, SAP BW, etc.)
- Comparação com resultados do Saiku
- Validação da lógica de agregação

### Exemplo: Análise Trivial

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Tempo].[Calendario_Enade].[Ano].Members} ON ROWS
FROM [Cubo_Enade]
```

### Exemplo: Análise Não Trivial

```mdx
WITH MEMBER [Measures].[Gap CE-FG] AS
  [Measures].[Media Componente Especifico] - [Measures].[Media Formacao Geral]
SELECT
  {[Measures].[Media Formacao Geral], [Measures].[Media Componente Especifico], [Measures].[Gap CE-FG]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Renda Familiar].Members} ON ROWS
FROM [Cubo_Enade]
```

## 🎨 Visualizações

### Gráficos Disponíveis
- 📈 **Linhas**: Evolução temporal
- 📊 **Barras**: Comparações categóricas
- 🥧 **Pizza**: Distribuições percentuais
- 🔥 **Heatmap**: Cruzamentos multidimensionais
- 📍 **Scatter**: Correlações e tendências

### Interatividade
- ✅ Hover para detalhes
- ✅ Zoom e Pan
- ✅ Download de gráficos
- ✅ Filtros dinâmicos
- ✅ Tabelas exportáveis

## 🗂️ Estrutura do Projeto

```
analise-enade-streamlit/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
└── Cubo_Enade.xml        # Schema do cubo (referência)
```

## 💡 Como Usar

### Navegação
1. **Sidebar**: Escolha entre "Análises Triviais" ou "Análises Não Triviais"
2. **Menu Principal**: Selecione a análise específica
3. **Visualização**: Explore gráficos e tabelas interativas

### Interpretação
- Cada análise inclui:
  - **Descrição**: Dimensões e medidas utilizadas
  - **Query MDX**: Equivalência para outras ferramentas
  - **Visualização**: Gráficos interativos
  - **Insights**: Interpretação dos resultados
  - **Operações OLAP**: Próximos passos de análise

## 🔧 Tecnologias

- **Streamlit**: Framework web Python
- **Plotly**: Gráficos interativos
- **Pandas**: Manipulação de dados
- **Python 3.8+**: Linguagem base

## 📚 Referências

- **Material Didático**: MD12 - Cubo de Dados e OLAP
- **Schema Cubo**: Cubo_Enade.xml
- **Especificação**: 15 análises (5 triviais + 10 não triviais)

## 🎓 Conceitos OLAP Aplicados

### Star Schema
```
         dim_estudante
               |
         dim_avaliacao
               |
         fato_enade  ------- dim_curso
               |
          dim_tempo
```

### Granularidade
- **Fato**: 1 registro por aluno por prova
- **Tempo**: Ano, Ciclo, Década
- **Curso**: Região → Estado → Município → Curso
- **Estudante**: Múltiplos atributos sociodemográficos

### Agregações
- **SUM**: Não aplicável (notas individuais)
- **AVG**: Medida principal (média das notas)
- **COUNT**: Quantidade de estudantes
- **MIN/MAX**: Extremos de desempenho

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Porta 8501 em uso
```bash
streamlit run app.py --server.port 8502
```

### Gráficos não aparecem
- Verifique conexão com internet (CDN do Plotly)
- Limpe cache: `streamlit cache clear`

## 📊 Dados Simulados

⚠️ **Nota**: Esta versão usa **dados simulados** para demonstração.

Para conectar dados reais:
1. Configure conexão com banco de dados no `app.py`
2. Substitua DataFrames de exemplo por queries SQL
3. Implemente cache com `@st.cache_data`

### Exemplo de Conexão Real

```python
import sqlalchemy

@st.cache_data
def load_data(query):
    engine = sqlalchemy.create_engine('postgresql://...')
    return pd.read_sql(query, engine)
```

## 🚀 Próximos Passos

### Fase 2: Dados Reais
- [ ] Conectar ao banco de dados ENADE
- [ ] Implementar cache inteligente
- [ ] Adicionar refresh automático

### Fase 3: Filtros Avançados
- [ ] Filtros globais na sidebar
- [ ] Seleção de múltiplas dimensões
- [ ] Comparação entre filtros

### Fase 4: Export e Relatórios
- [ ] Download de gráficos (PNG/SVG)
- [ ] Export de dados (CSV/Excel)
- [ ] Geração de PDF com análises

### Fase 5: Dashboards
- [ ] Dashboard executivo
- [ ] Dashboard por região
- [ ] Dashboard temporal

## 👥 Autores

- **Desenvolvido por**: Claude Code
- **Baseado em**: Material MD12 (Cubo de Dados e OLAP)
- **Data**: Junho 2024

## 📄 Licença

Este projeto é educacional e segue as diretrizes acadêmicas.

---

**📞 Suporte**: Para dúvidas sobre operações OLAP ou análises específicas, consulte o material MD12.
