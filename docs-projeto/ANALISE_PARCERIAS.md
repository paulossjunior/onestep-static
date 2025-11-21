# Análise de Parcerias e Colaborações Externas

## Visão Geral

Foi implementado um sistema completo de análise de parcerias e colaborações externas para o observatório OneStep. O sistema identifica e classifica os principais parceiros organizacionais e grupos de pesquisa externos envolvidos nos projetos de pesquisa do Campus Serra.

## Componentes Implementados

### 1. Script de Análise (`scripts/analyze_partnerships.py`)

Script Python orientado a objetos que:

- **Carrega dados** dos projetos de pesquisa
- **Analisa parcerias** identificando organizações parceiras
- **Analisa colaborações** identificando grupos de pesquisa externos
- **Gera estatísticas** sobre as colaborações
- **Exporta resultados** em formato JSON

#### Classes Principais

```python
ProjectDataLoader      # Carrega e filtra dados de projetos
PartnershipAnalyzer    # Analisa parcerias e grupos externos
AnalysisExporter       # Exporta resultados para JSON
PartnershipStats       # Estatísticas de parceria
PartnershipAnalysis    # Análise completa
```

### 2. Arquivo de Dados Gerado (`data/partnership_analysis.json`)

Contém:

- **Top 20 parceiros** organizacionais
- **Top 20 grupos de pesquisa externos**
- **Estatísticas gerais**:
  - Total de projetos
  - Projetos com parceiros (186 - 32.12%)
  - Parceiros únicos (54)
  - Projetos com grupos externos (48 - 8.29%)
  - Grupos externos únicos (17)

### 3. Visualizações nas Páginas de Documentação

Adicionadas seções em `research_projects.md` e `research_projects.pt.md`:

#### Estatísticas em Cards
- 4 cards mostrando métricas principais
- Design responsivo com grid layout

#### Gráfico de Parceiros
- Gráfico de barras horizontal
- Top 20 organizações parceiras
- Ordenado por número de projetos

#### Gráfico de Grupos Externos
- Gráfico de barras horizontal
- Top 20 grupos de pesquisa externos
- Ordenado por número de projetos

#### Tabelas Detalhadas
- Listas completas expansíveis (details/summary)
- Informações de contagem e porcentagem

### 4. Script de Build (`scripts/build.sh`)

Script bash que:
1. Executa a análise de parcerias
2. Constrói a documentação MkDocs

## Principais Descobertas

### Top 5 Parceiros
1. **Vale S.A.** - 12 projetos (2.07%)
2. **Fapes** - 11 projetos (1.9%)
3. **Arcelormittal Tubarão** - 10 projetos (1.73%)
4. **Mogai Tecnologia Da Informação** - 8 projetos (1.38%)
5. **Cnpq** - 7 projetos (1.21%)

### Top 5 Grupos de Pesquisa Externos
1. **Labcisne** - 7 projetos (1.21%)
2. **Gain** - 5 projetos (0.86%)
3. **Lcad** - 4 projetos (0.69%)
4. **Pop-Es/Ufes** - 3 projetos (0.52%)
5. **Lcad Da Ufes** - 3 projetos (0.52%)

## Como Usar

### Executar Análise Manualmente
```bash
python3 scripts/analyze_partnerships.py
```

### Executar Build Completo
```bash
./scripts/build.sh
```

### Visualizar Resultados
Acesse as páginas:
- `/research_projects.md` (inglês)
- `/research_projects.pt.md` (português)

Role até a seção "Partnership and External Collaboration Analysis" / "Análise de Parcerias e Colaborações Externas"

## Arquitetura

```
┌─────────────────────────────────┐
│  research_projects.json         │
│  (Dados de entrada)             │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  analyze_partnerships.py        │
│  (Processamento OO)             │
│  - ProjectDataLoader            │
│  - PartnershipAnalyzer          │
│  - AnalysisExporter             │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  partnership_analysis.json      │
│  (Dados processados)            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  research_projects.md           │
│  research_projects.pt.md        │
│  (Visualização Jinja2)          │
│  - Cards de estatísticas        │
│  - Gráficos Plotly              │
│  - Tabelas detalhadas           │
└─────────────────────────────────┘
```

## Benefícios

1. **Transparência**: Identifica claramente as parcerias institucionais
2. **Análise de Impacto**: Mostra quais organizações mais colaboram
3. **Rede de Pesquisa**: Visualiza conexões interinstitucionais
4. **Tomada de Decisão**: Dados para fortalecer parcerias estratégicas
5. **Manutenibilidade**: Código OO bem estruturado e documentado

## Próximos Passos Sugeridos

1. **Análise Temporal**: Evolução das parcerias ao longo dos anos
2. **Rede de Colaboração**: Grafo de conexões entre parceiros
3. **Análise por Área**: Parcerias por área de conhecimento
4. **Métricas de Impacto**: Publicações e financiamento por parceiro
5. **Dashboard Interativo**: Filtros e visualizações dinâmicas

## Manutenção

Para atualizar a análise:
1. Atualize `data/research_projects.json` com novos dados
2. Execute `python3 scripts/analyze_partnerships.py`
3. Reconstrua a documentação

O processo é automatizado e pode ser integrado em CI/CD.
