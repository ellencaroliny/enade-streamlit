# 🎯 Guia Rápido de Uso

## 🚀 Iniciar Aplicação

### Passo 1: Abrir Terminal
```bash
cd C:\Users\valcann\Downloads\analise-enade-streamlit
```

### Passo 2: Instalar Dependências (apenas primeira vez)
```bash
pip install -r requirements.txt
```

### Passo 3: Executar
```bash
streamlit run app.py
```

✅ A aplicação abrirá automaticamente em: `http://localhost:8501`

---

## 📊 Navegação

### 1️⃣ **Sidebar (Esquerda)**

**Escolha o tipo de análise:**
- 📊 **Análises Triviais**: 1 dimensão, simples de interpretar
- 🔬 **Análises Não Triviais**: 2+ dimensões, cruzamentos complexos

### 2️⃣ **Menu Principal (Centro)**

**Selecione a análise específica** no dropdown

### 3️⃣ **Conteúdo (Centro/Direita)**

Para cada análise você verá:

#### 📝 Descrição
- Dimensões utilizadas
- Medidas agregadas
- Tipo de agregação (AVG, SUM, etc.)

#### 💻 Query MDX
- Equivalência em linguagem MDX
- Útil para migrar para outras ferramentas OLAP

#### 📊 Visualizações Interativas
- Gráficos de linha, barra, pizza, heatmap
- **Hover**: Passe o mouse para ver valores
- **Zoom**: Clique e arraste
- **Download**: Ícone de câmera no canto

#### 📋 Tabelas de Dados
- Dados brutos usados nos gráficos
- Ordenação por coluna (clique no header)

#### 💡 Operações OLAP Sugeridas
- Próximos passos de análise
- Drill-down, Roll-up, Dice, Slice

#### 🔍 Análise Interpretativa
- Insights principais
- Conclusões baseadas nos dados

---

## 🎓 Análises Disponíveis

### 📊 TRIVIAIS (5)

#### 1. Média de Nota Geral por Ano
**O que mostra**: Evolução do desempenho ao longo do tempo

**Como usar**:
- Identifique tendências (subindo/caindo)
- Veja impacto de políticas educacionais
- Compare períodos específicos

**Operações OLAP**:
- Drill-down: Ano → Ciclo Avaliativo
- Roll-up: Ano → Década

---

#### 2. Média de Nota Geral por Região
**O que mostra**: Diferenças entre Sul, Sudeste, Centro-Oeste, Nordeste, Norte

**Como usar**:
- Identifique desigualdades regionais
- Compare sua região com outras
- Veja onde investir em educação

**Operações OLAP**:
- Drill-down: Região → Estado → Município
- Dice: Cruzar com Tipo de Escola

---

#### 3. Média de Nota Geral por Sexo
**O que mostra**: Comparação Feminino vs Masculino

**Como usar**:
- Veja se há diferença de gênero
- Analise distribuição de estudantes
- Compare com outros fatores

**Operações OLAP**:
- Dice: Cruzar com Cor/Raça ou Renda

---

#### 4. Média de Formação Geral por Tipo de Escola
**O que mostra**: Pública vs Privada vs Mista (ensino médio)

**Como usar**:
- Avalie impacto da formação básica
- Veja preparação para conhecimento geral
- Compare com desempenho técnico

**Operações OLAP**:
- Dice: Cruzar com Renda Familiar
- Drill-across: Comparar com Componente Específico

---

#### 5. Média Componente Específico por Turno
**O que mostra**: Diurno vs Noturno vs Integral

**Como usar**:
- Veja se turno afeta desempenho técnico
- Analise perfil de cada turno
- Identifique desafios noturnos

**Operações OLAP**:
- Dice: Cruzar com Horas de Trabalho
- Slice: Filtrar por Categoria Administrativa

---

### 🔬 NÃO TRIVIAIS (10)

#### 1. Efeito da Primeira Geração Universitária
**O que mostra**: Impacto de ser primeiro da família na universidade, por estado

**Insight**: Onde a inclusão social funciona melhor?

**Gráficos**:
- Comparação: Primeira Geração vs Média Geral (barras agrupadas)
- Gap de Desempenho por Estado (barras coloridas)

---

#### 2. Evolução de Cotistas por Ciclo
**O que mostra**: Desempenho de cotistas ao longo do tempo

**Insight**: Política de cotas manteve qualidade?

**Gráficos**:
- Linhas temporais: Cotistas vs Não-Cotistas
- Gap diminuindo ao longo dos ciclos (barras)

---

#### 3. Resiliência de Alunos Trabalhadores
**O que mostra**: Impacto de trabalhar + estudar à noite

**Insight**: Público vs Privado conseguem apoiar melhor?

**Gráficos**:
- Barras agrupadas: Horas de Trabalho × Tipo IES
- Heatmap: Intensidade do impacto

---

#### 4. Percepção vs Nota Real
**O que mostra**: Alunos que acham prova difícil realmente tiram notas baixas?

**Insight**: Validação da percepção por curso

**Gráficos**:
- Scatter plot: Quantidade × Nota (por dificuldade)
- Facet por Curso (4 gráficos)

---

#### 5. Infraestrutura × Modalidade
**O que mostra**: EAD depende de infraestrutura física?

**Insight**: Presencial é mais afetado por equipamentos

**Gráficos**:
- Linhas: Evolução da nota por avaliação de equipamentos
- Barras: Gap Presencial - EAD

---

#### 6. Renda: Específico vs Geral
**O que mostra**: Vulnerabilidade afeta mais conhecimento técnico ou humanista?

**Insight**: Baixa renda prejudica mais o componente específico

**Gráficos**:
- Linhas duplas: FG e CE por renda
- Barras: Gap entre componentes

---

#### 7. Cor/Raça × Categoria Administrativa
**O que mostra**: Disparidades étnicas em Federal vs Estadual vs Privada

**Insight**: Federais têm menor desigualdade racial

**Gráficos**:
- Heatmap: Intensidade de desempenho
- Barras agrupadas: Comparação direta

---

#### 8. Clareza × Idade Avançada
**O que mostra**: Legibilidade da prova afeta mais idosos?

**Insight**: Impacto aumenta com idade (26% maior em +60 anos)

**Gráficos**:
- Linhas: Nota por idade (separado por clareza)
- Barras: Diferença Boa - Ruim por idade

---

#### 9. Capital vs Interior
**O que mostra**: Qualidade concentrada nas capitais? Varia por estado?

**Insight**: Sul/Sudeste têm interior forte, Norte concentrado

**Gráficos**:
- Barras agrupadas: Capital vs Interior por estado
- Scatter: Concentração de IES × Gap de desempenho

---

#### 10. Tempo de Prova × Mães Solo
**O que mostra**: Tempo afeta diferentemente mães universitárias?

**Insight**: Maior impacto em mães, mesmo com tempo adequado

**Gráficos**:
- Linhas: Três perfis (mães solo, mulheres sem filhos, homens)
- Barras: Gap de mães vs média geral

---

## 💡 Dicas de Uso

### 🔍 Exploração Guiada

1. **Comece pelas Triviais**: Entenda dimensões e medidas
2. **Vá para Não Triviais**: Veja cruzamentos complexos
3. **Compare Análises**: Veja padrões recorrentes

### 📊 Interpretação de Gráficos

**Linhas**:
- Tendência subindo = melhoria
- Tendência caindo = piora
- Linhas paralelas = comportamento similar

**Barras**:
- Maior = melhor desempenho
- Verde = positivo
- Vermelho = negativo

**Heatmap**:
- Verde escuro = alto desempenho
- Vermelho escuro = baixo desempenho
- Amarelo = médio

**Scatter**:
- Pontos agrupados = correlação
- Pontos dispersos = sem correlação
- Tamanho = quantidade

### 🎯 Focar em Insights

Cada análise tem seção **"Análise Interpretativa"** com:
- ✅ Principais achados
- ✅ Números concretos
- ✅ Comparações relevantes
- ✅ Recomendações

---

## 🔧 Operações OLAP Explicadas

### Drill-down (Detalhar)
**Exemplo**: Região → Estado → Município

"Quero ver São Paulo especificamente dentro do Sudeste"

### Roll-up (Agregar)
**Exemplo**: Município → Estado → Região

"Quero visão macro, agregando cidades"

### Slice (Fatiar)
**Exemplo**: Filtrar apenas ano 2022

"Quero ver só o último ENADE"

### Dice (Cubo)
**Exemplo**: Sexo × Região × Renda

"Quero cruzar múltiplos fatores"

### Pivot (Rotacionar)
**Exemplo**: Trocar linhas ↔ colunas

"Quero anos nas colunas em vez de linhas"

---

## ❓ FAQ

**P: Dados são reais?**
R: Versão atual usa dados simulados. Para dados reais, conecte ao banco.

**P: Posso exportar gráficos?**
R: Sim! Clique no ícone de câmera em cada gráfico.

**P: Como comparar duas análises?**
R: Abra a aplicação em duas abas do navegador.

**P: Posso adicionar análises?**
R: Sim! Edite `app.py` seguindo o padrão existente.

**P: E se quiser filtros dinâmicos?**
R: Veja seção "Próximos Passos" no README.

---

## 🎨 Atalhos de Teclado

- `R`: Recarregar aplicação
- `Ctrl + Scroll`: Zoom na página
- `Ctrl + F`: Buscar texto

---

## 📞 Precisa de Ajuda?

1. Leia a seção **"Análise Interpretativa"** de cada análise
2. Consulte o **README.md** para detalhes técnicos
3. Veja **"Operações OLAP Aplicáveis"** para próximos passos

---

**🎓 Desenvolvido para demonstrar conceitos OLAP de forma interativa e educacional**
