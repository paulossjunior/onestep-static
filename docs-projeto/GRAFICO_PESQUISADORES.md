# 📊 Gráfico de Participação de Pesquisadores

## ✅ Nova Funcionalidade Adicionada

Adicionado gráfico de barras mostrando a distribuição de participação de pesquisadores (coordenadores + pesquisadores) nos projetos de cada grupo de pesquisa.

---

## 🎯 O que Foi Adicionado

### 1. Gráfico de Distribuição

**Localização:** Após a tabela de estudantes em cada grupo de pesquisa

**Mostra:**
- Quantos pesquisadores participaram de 1 projeto
- Quantos pesquisadores participaram de 2 projetos
- Quantos pesquisadores participaram de 3+ projetos
- E assim por diante...

### 2. Lista de Pesquisadores Altamente Engajados

**Critério:** Pesquisadores que participaram de 3 ou mais projetos

**Mostra:**
- Nome do pesquisador
- Número de projetos
- Ordenado por número de projetos (decrescente)

---

## 📊 Exemplo Visual

### Gráfico de Barras

```
Distribuição de Participação de Pesquisadores
(Total: 25 pesquisadores únicos)

Número de Pesquisadores
    ↑
 15 │     ██
    │     ██
 10 │     ██  ██
    │     ██  ██
  5 │     ██  ██  ██
    │     ██  ██  ██  ██
  0 └─────────────────────→
         1   2   3   4
    Número de Projetos por Pesquisador
```

**Interpretação:**
- 15 pesquisadores participaram de 1 projeto
- 6 pesquisadores participaram de 2 projetos
- 3 pesquisadores participaram de 3 projetos
- 1 pesquisador participou de 4 projetos

### Tabela de Altamente Engajados

```
┌─────────────────────────────────────────┐
│ Pesquisadores Altamente Engajados       │
│ (3+ Projetos)                           │
├─────────────────────────┬───────────────┤
│ Nome do Pesquisador     │ Nº Projetos   │
├─────────────────────────┼───────────────┤
│ Dr. João Silva          │      5        │
│ Dra. Maria Santos       │      4        │
│ Dr. Pedro Oliveira      │      3        │
│ Dra. Ana Costa          │      3        │
└─────────────────────────┴───────────────┘
Total: 4 pesquisador(es) com envolvimento sustentado
```

---

## 🔍 Como Funciona

### 1. Coleta de Dados

```python
# Para cada projeto do grupo:
# 1. Adiciona o coordenador
# 2. Adiciona todos os pesquisadores
# 3. Conta quantos projetos cada pessoa participou
```

### 2. Contagem de Participação

```python
researcher_projects = {
    "Dr. João Silva": ["Projeto A", "Projeto B", "Projeto C", "Projeto D", "Projeto E"],
    "Dra. Maria Santos": ["Projeto A", "Projeto C", "Projeto F", "Projeto G"],
    "Dr. Pedro Oliveira": ["Projeto B", "Projeto D", "Projeto H"],
    # ...
}
```

### 3. Distribuição

```python
participation_distribution = {
    1: 15,  # 15 pesquisadores com 1 projeto
    2: 6,   # 6 pesquisadores com 2 projetos
    3: 3,   # 3 pesquisadores com 3 projetos
    4: 1,   # 1 pesquisador com 4 projetos
}
```

---

## 📍 Localização nos Arquivos

### Inglês
**Arquivo:** `onestep-static/docs/research_groups.md`

**Seção:** Após "Students and Their Projects"

**Título:** "Researcher Participation Distribution"

### Português
**Arquivo:** `onestep-static/docs/research_groups.pt.md`

**Seção:** Após "Estudantes e Seus Projetos"

**Título:** "Distribuição de Participação de Pesquisadores"

---

## 🎨 Características do Gráfico

### Visual
- ✅ **Cor:** Verde (#2ca02c) - diferente dos estudantes (azul)
- ✅ **Tipo:** Gráfico de barras
- ✅ **Interativo:** Hover mostra detalhes
- ✅ **Labels:** Números em cima de cada barra
- ✅ **Responsivo:** Adapta ao tamanho da tela

### Dados
- ✅ **Pesquisadores únicos:** Conta cada pessoa uma vez
- ✅ **Inclui coordenadores:** Coordenadores são contados como pesquisadores
- ✅ **Inclui pesquisadores:** Todos os pesquisadores listados
- ✅ **Por grupo:** Cada grupo tem seu próprio gráfico

---

## 📊 Diferenças: Estudantes vs Pesquisadores

| Aspecto | Estudantes | Pesquisadores |
|---------|-----------|---------------|
| Cor | Azul (#1f77b4) | Verde (#2ca02c) |
| Critério "Altamente Engajado" | 5+ projetos | 3+ projetos |
| Posição | Antes da rede | Antes da rede |
| Título (EN) | Student Participation | Researcher Participation |
| Título (PT) | Participação de Estudantes | Participação de Pesquisadores |

---

## 🧪 Como Testar

### 1. Iniciar Servidor

```bash
cd onestep-static
mkdocs serve
```

### 2. Acessar Grupos de Pesquisa

```
http://127.0.0.1:8001/research_groups/
```

### 3. Verificar Gráficos

Para cada grupo de pesquisa que tem projetos:

1. **Rolar até "Visualizations"**
2. **Ver gráfico de projetos ao longo do tempo**
3. **Ver gráfico de estudantes ao longo do tempo**
4. **Ver tabela de estudantes**
5. **Ver gráfico de participação de pesquisadores** ← NOVO!
6. **Ver tabela de pesquisadores altamente engajados** ← NOVO!
7. **Ver rede de colaboração**

### 4. Testar em Português

```
http://127.0.0.1:8001/pt/research_groups/
```

Verificar que:
- ✅ Título em português
- ✅ Labels em português
- ✅ Tabela em português

---

## 📈 Insights que o Gráfico Revela

### 1. Engajamento de Pesquisadores

```
Muitos pesquisadores com 1 projeto:
→ Grupo com muitos colaboradores pontuais

Poucos pesquisadores com muitos projetos:
→ Grupo com núcleo estável de pesquisadores
```

### 2. Estabilidade do Grupo

```
Distribuição uniforme:
→ Grupo equilibrado

Concentração em poucos pesquisadores:
→ Grupo dependente de poucos membros
```

### 3. Colaboração

```
Muitos pesquisadores com 2-3 projetos:
→ Boa colaboração entre membros

Maioria com 1 projeto:
→ Colaborações pontuais
```

---

## 🔄 Comparação com Estudantes

### Padrões Típicos

**Estudantes:**
```
Maioria: 1-2 projetos (iniciação científica)
Alguns: 3-5 projetos (bolsistas dedicados)
Raros: 5+ projetos (estudantes excepcionais)
```

**Pesquisadores:**
```
Maioria: 1-2 projetos (colaboradores)
Alguns: 3-5 projetos (membros ativos)
Raros: 5+ projetos (líderes do grupo)
```

---

## 📝 Código Adicionado

### Estrutura

```jinja2
{# 1. Coletar dados de pesquisadores #}
{% set researcher_projects = {} %}

{# 2. Contar participação #}
{% set researcher_participation_distribution = {} %}

{# 3. Criar gráfico de barras #}
<div id="chart-researcher-participation-{{ group_index }}">
<script>
  // Plotly bar chart
</script>

{# 4. Listar altamente engajados #}
{% if highly_engaged_researchers|length > 0 %}
  <table>
    <!-- Lista de pesquisadores -->
  </table>
{% endif %}
```

---

## ✅ Checklist de Verificação

### Funcionalidade
- [x] Gráfico aparece em cada grupo
- [x] Dados corretos (coordenadores + pesquisadores)
- [x] Barras com cores corretas (verde)
- [x] Labels visíveis
- [x] Hover funciona
- [x] Tabela de altamente engajados aparece
- [x] Ordenação correta (decrescente)

### Bilíngue
- [x] Versão em inglês
- [x] Versão em português
- [x] Títulos traduzidos
- [x] Labels traduzidos
- [x] Descrições traduzidas

### Visual
- [x] Gráfico responsivo
- [x] Cores consistentes
- [x] Espaçamento adequado
- [x] Tabela estilizada

---

## 🎉 Resultado

Agora cada grupo de pesquisa tem:

1. ✅ **Gráfico de projetos** ao longo do tempo
2. ✅ **Gráfico de estudantes** ao longo do tempo
3. ✅ **Tabela de estudantes** e seus projetos
4. ✅ **Gráfico de pesquisadores** (NOVO!)
5. ✅ **Tabela de pesquisadores altamente engajados** (NOVO!)
6. ✅ **Rede de colaboração**
7. ✅ **Estatísticas da rede**

---

**Data:** 21 de Novembro de 2025  
**Status:** ✅ Implementado  
**Arquivos:** research_groups.md e research_groups.pt.md
