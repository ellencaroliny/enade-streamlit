# 📐 Queries MDX - Referência Completa

Todas as queries MDX equivalentes às análises implementadas no Streamlit.

---

## 🎯 Análises Triviais

### 1. Média de Nota Geral por Ano

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Tempo].[Calendario_Enade].[Ano].Members} ON ROWS
FROM [Cubo_Enade]
```

**Ordem**: Crescente por Ano  
**Filtro**: Nenhum

---

### 2. Média de Nota Geral por Região

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Regiao].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY [Measures].[Media Nota Geral] DESC
```

**Ordem**: Decrescente por Média  
**Filtro**: Nenhum

---

### 3. Média de Nota Geral por Sexo

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Sexo].Members} ON ROWS
FROM [Cubo_Enade]
```

**Ordem**: Alfabética  
**Filtro**: Nenhum

---

### 4. Média de Formação Geral por Tipo de Escola

```mdx
SELECT
  {[Measures].[Media Formacao Geral]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Tipo Escola Ensino Medio].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY [Measures].[Media Formacao Geral] DESC
```

**Ordem**: Decrescente por Média  
**Filtro**: Nenhum

---

### 5. Média Componente Específico por Turno

```mdx
SELECT
  {[Measures].[Media Componente Especifico]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Turno].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY [Measures].[Media Componente Especifico] DESC
```

**Ordem**: Decrescente por Média  
**Filtro**: Nenhum

---

## 🔬 Análises Não Triviais

### 1. Efeito da Primeira Geração Universitária por Estado

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Estado].Members} ON ROWS
FROM [Cubo_Enade]
WHERE ([Estudante].[Dados_Estudante].[Primeira Geracao Universitaria].[Sim])
ORDER BY [Measures].[Media Nota Geral] DESC
```

**Filtro**: Apenas primeira geração = 'Sim'  
**Ordem**: Decrescente por Média

---

### 2. Evolução do Desempenho de Cotistas por Ciclo

```mdx
SELECT
  {[Measures].[Media Nota Geral], [Measures].[Media Componente Especifico]} ON COLUMNS,
  {[Tempo].[Calendario_Enade].[Ciclo Avaliativo].Members} *
  {[Estudante].[Dados_Estudante].[Cotas].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY [Tempo].[Calendario_Enade].[Ciclo Avaliativo]
```

**Cruzamento**: Ciclo × Cotas  
**Ordem**: Temporal (Ciclo)

---

### 3. Resiliência de Alunos Trabalhadores Noturnos

```mdx
SELECT
  {[Measures].[Media Componente Especifico]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Horas Trabalho].Members} *
  {[Curso].[Geografia_Curso].[Categoria Administrativa].Members} ON ROWS
FROM [Cubo_Enade]
WHERE ([Curso].[Geografia_Curso].[Turno].[Noturno])
ORDER BY [Estudante].[Dados_Estudante].[Horas Trabalho]
```

**Filtro**: Apenas turno = 'Noturno'  
**Cruzamento**: Horas Trabalho × Categoria Admin

---

### 4. Percepção de Dificuldade vs Nota Real por Curso

```mdx
SELECT
  {[Measures].[Media Componente Especifico]} ON COLUMNS,
  {[Avaliacao].[Percepcao_Prova].[Dificuldade Componente Especifico].Members} *
  {[Curso].[Geografia_Curso].[Curso].Members} ON ROWS
FROM [Cubo_Enade]
WHERE (
  [Curso].[Geografia_Curso].[Curso].[Medicina],
  [Curso].[Geografia_Curso].[Curso].[Direito],
  [Curso].[Geografia_Curso].[Curso].[Pedagogia],
  [Curso].[Geografia_Curso].[Curso].[Eng. Civil]
)
ORDER BY [Curso].[Geografia_Curso].[Curso]
```

**Filtro**: Cursos específicos (exemplo)  
**Cruzamento**: Dificuldade × Curso

---

### 5. Infraestrutura do Curso vs Desempenho por Modalidade

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Avaliacao].[Percepcao_Prova].[Avaliacao Infraestrutura Equipamentos].Members} *
  {[Curso].[Geografia_Curso].[Modalidade].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY 
  [Curso].[Geografia_Curso].[Modalidade],
  [Avaliacao].[Percepcao_Prova].[Avaliacao Infraestrutura Equipamentos]
```

**Cruzamento**: Infraestrutura × Modalidade  
**Ordem**: Modalidade, depois Infraestrutura

---

### 6. Efeito da Renda Familiar: Específico vs Geral

```mdx
WITH MEMBER [Measures].[Gap CE-FG] AS
  [Measures].[Media Componente Especifico] - [Measures].[Media Formacao Geral]
SELECT
  {
    [Measures].[Media Formacao Geral],
    [Measures].[Media Componente Especifico],
    [Measures].[Gap CE-FG]
  } ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Renda Familiar].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY [Estudante].[Dados_Estudante].[Renda Familiar]
```

**Calculated Member**: Gap = CE - FG  
**Medidas**: 3 (FG, CE, Gap)

---

### 7. Desempenho por Cor/Raça e Categoria Administrativa

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Cor Raca].Members} *
  {[Curso].[Geografia_Curso].[Categoria Administrativa].Members} ON ROWS
FROM [Cubo_Enade]
ORDER BY 
  [Curso].[Geografia_Curso].[Categoria Administrativa],
  [Measures].[Media Nota Geral] DESC
```

**Cruzamento**: Cor/Raça × Categoria Admin  
**Ordem**: Por Categoria, depois por Média

---

### 8. Clareza dos Enunciados e Idade Avançada

```mdx
WITH SET [Idade_Avancada] AS
  FILTER(
    [Estudante].[Dados_Estudante].[Faixa Etaria].Members,
    [Estudante].[Dados_Estudante].[Faixa Etaria].CurrentMember.Name >= "40"
  )
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Avaliacao].[Percepcao_Prova].[Clareza Enunciados CE].Members} *
  [Idade_Avancada] ON ROWS
FROM [Cubo_Enade]
ORDER BY [Estudante].[Dados_Estudante].[Faixa Etaria]
```

**Filtro Dinâmico**: Idade >= 40  
**Cruzamento**: Clareza × Faixa Etária

---

### 9. Disparidade Capital vs Interior por Estado

```mdx
WITH 
  MEMBER [Curso].[Geografia_Curso].[Capital] AS
    AGGREGATE(
      FILTER(
        [Curso].[Geografia_Curso].[Municipio].Members,
        [Curso].[Geografia_Curso].[Municipio].CurrentMember.Name IN {...} // Lista de capitais
      )
    )
  MEMBER [Curso].[Geografia_Curso].[Interior] AS
    AGGREGATE(
      FILTER(
        [Curso].[Geografia_Curso].[Municipio].Members,
        NOT ([Curso].[Geografia_Curso].[Municipio].CurrentMember.Name IN {...})
      )
    )
  MEMBER [Measures].[Gap Capital-Interior] AS
    ([Curso].[Geografia_Curso].[Capital], [Measures].[Media Nota Geral]) -
    ([Curso].[Geografia_Curso].[Interior], [Measures].[Media Nota Geral])
SELECT
  {
    [Measures].[Media Nota Geral],
    [Measures].[Gap Capital-Interior]
  } ON COLUMNS,
  {[Curso].[Geografia_Curso].[Estado].Members} *
  {[Curso].[Geografia_Curso].[Capital], [Curso].[Geografia_Curso].[Interior]} ON ROWS
FROM [Cubo_Enade]
```

**Calculated Members**: Capital, Interior, Gap  
**Lógica Customizada**: Classificação de municípios

---

### 10. Tempo de Prova: Impacto em Mães Solo

```mdx
WITH 
  SET [Maes_Solo] AS
    FILTER(
      [Estudante].[Dados_Estudante].[Sexo].Members,
      [Estudante].[Dados_Estudante].[Sexo].CurrentMember.Name = "F"
      // + filtros adicionais de estrutura familiar
    )
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Avaliacao].[Percepcao_Prova].[Tempo de Prova].Members} ON ROWS
FROM [Cubo_Enade]
WHERE [Maes_Solo]
ORDER BY [Avaliacao].[Percepcao_Prova].[Tempo de Prova]
```

**Filtro Customizado**: Sexo = F + perfil familiar  
**Dimensão**: Tempo de Prova

---

## 🎯 Operações OLAP em MDX

### Drill-down (Detalhar)

```mdx
-- De Região para Estado
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Regiao].[Sudeste].Children} ON ROWS
FROM [Cubo_Enade]
```

---

### Roll-up (Agregar)

```mdx
-- De Município para Estado
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Municipio].[Sao Paulo].Parent} ON ROWS
FROM [Cubo_Enade]
```

---

### Slice (Fatiar)

```mdx
-- Apenas ano 2022
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Regiao].Members} ON ROWS
FROM [Cubo_Enade]
WHERE ([Tempo].[Calendario_Enade].[Ano].[2022])
```

---

### Dice (Cubo)

```mdx
-- Cruzamento 3D: Sexo × Região × Renda
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Estudante].[Dados_Estudante].[Sexo].Members} *
  {[Curso].[Geografia_Curso].[Regiao].Members} *
  {[Estudante].[Dados_Estudante].[Renda Familiar].Members} ON ROWS
FROM [Cubo_Enade]
```

---

### Pivot (Rotacionar)

```mdx
-- Inverter eixos: Anos nas colunas
SELECT
  {[Tempo].[Calendario_Enade].[Ano].Members} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Regiao].Members} ON ROWS
FROM [Cubo_Enade]
WHERE ([Measures].[Media Nota Geral])
```

---

## 🔧 Funções MDX Úteis

### FILTER (Filtrar)

```mdx
FILTER(
  [Estudante].[Dados_Estudante].[Idade].Members,
  [Estudante].[Dados_Estudante].[Idade].CurrentMember.Name > "30"
)
```

---

### TOPCOUNT (Top N)

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  TOPCOUNT(
    [Curso].[Geografia_Curso].[Curso].Members,
    10,
    [Measures].[Media Nota Geral]
  ) ON ROWS
FROM [Cubo_Enade]
```

---

### BOTTOMCOUNT (Bottom N)

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  BOTTOMCOUNT(
    [Curso].[Geografia_Curso].[Estado].Members,
    5,
    [Measures].[Media Nota Geral]
  ) ON ROWS
FROM [Cubo_Enade]
```

---

### AGGREGATE (Agregar)

```mdx
WITH MEMBER [Curso].[Geografia_Curso].[Sul_Sudeste] AS
  AGGREGATE({
    [Curso].[Geografia_Curso].[Regiao].[Sul],
    [Curso].[Geografia_Curso].[Regiao].[Sudeste]
  })
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  {[Curso].[Geografia_Curso].[Sul_Sudeste]} ON ROWS
FROM [Cubo_Enade]
```

---

### CROSSJOIN (Produto Cartesiano)

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  CROSSJOIN(
    [Estudante].[Dados_Estudante].[Sexo].Members,
    [Curso].[Geografia_Curso].[Regiao].Members
  ) ON ROWS
FROM [Cubo_Enade]
```

---

### HIERARCHIZE (Hierarquizar)

```mdx
SELECT
  {[Measures].[Media Nota Geral]} ON COLUMNS,
  HIERARCHIZE(
    {
      [Curso].[Geografia_Curso].[Regiao].Members,
      [Curso].[Geografia_Curso].[Estado].Members
    }
  ) ON ROWS
FROM [Cubo_Enade]
```

---

## 📊 Calculated Members Avançados

### Percentual de Variação

```mdx
WITH MEMBER [Measures].[Variacao_Percentual] AS
  (
    [Measures].[Media Nota Geral] -
    ([Measures].[Media Nota Geral], [Tempo].[Calendario_Enade].[Ano].PrevMember)
  ) /
  ([Measures].[Media Nota Geral], [Tempo].[Calendario_Enade].[Ano].PrevMember) * 100
```

---

### Média Móvel (3 períodos)

```mdx
WITH MEMBER [Measures].[Media_Movel_3] AS
  AVG(
    {
      [Tempo].[Calendario_Enade].[Ano].CurrentMember.Lag(1),
      [Tempo].[Calendario_Enade].[Ano].CurrentMember,
      [Tempo].[Calendario_Enade].[Ano].CurrentMember.Lead(1)
    },
    [Measures].[Media Nota Geral]
  )
```

---

### Ranking

```mdx
WITH MEMBER [Measures].[Ranking] AS
  RANK(
    [Curso].[Geografia_Curso].CurrentMember,
    [Curso].[Geografia_Curso].[Estado].Members,
    [Measures].[Media Nota Geral]
  )
```

---

### IIF (Condicional)

```mdx
WITH MEMBER [Measures].[Classificacao] AS
  IIF(
    [Measures].[Media Nota Geral] >= 60,
    "Alta",
    IIF(
      [Measures].[Media Nota Geral] >= 50,
      "Media",
      "Baixa"
    )
  )
```

---

## 🎓 Boas Práticas MDX

### 1. Use WITH para Clareza

```mdx
WITH 
  MEMBER [Measures].[Gap] AS ...
  SET [TopEstados] AS ...
SELECT ...
```

---

### 2. Evite Cruzamentos Muito Grandes

❌ **Ruim**:
```mdx
-- 1000 × 1000 = 1 milhão de células!
{[Dim1].Members} * {[Dim2].Members}
```

✅ **Bom**:
```mdx
-- Use TOPCOUNT ou FILTER
TOPCOUNT([Dim1].Members, 20, [Measures].[Value])
```

---

### 3. Ordene Resultados

```mdx
SELECT ... ON ROWS
FROM ...
ORDER BY [Measures].[Value] DESC
```

---

### 4. Nomeie Calculated Members Claramente

✅ **Bom**: `[Measures].[Gap_CE_Menos_FG]`  
❌ **Ruim**: `[Measures].[Calc1]`

---

### 5. Documente Queries Complexas

```mdx
-- Análise: Efeito da renda no gap entre CE e FG
-- Criado: 2024-06-10
-- Autor: Equipe Analytics
WITH MEMBER [Measures].[Gap] AS ...
SELECT ...
```

---

## 📚 Referências

- **MDX Language Reference**: [Microsoft Docs](https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-language-reference-mdx)
- **Schema Cubo ENADE**: `Cubo_Enade.xml`
- **Material Didático**: MD12 - Cubo de Dados e OLAP

---

**💡 Todas estas queries podem ser executadas no Saiku ou em qualquer ferramenta OLAP compatível com MDX**
