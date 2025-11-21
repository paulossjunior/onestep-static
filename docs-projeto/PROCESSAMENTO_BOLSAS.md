# Processamento de Dados de Bolsas

## Visão Geral

Sistema completo para processar dados de bolsas de pesquisa do IFES Campus Serra, incluindo remoção de dados sensíveis e geração de JSON consolidado para análise e visualização.

## Componentes Implementados

### 1. Remoção de Dados Sensíveis (`scripts/remove_phone_columns.py`)

Script para remover colunas com números de telefone dos arquivos CSV, garantindo conformidade com LGPD.

#### Funcionalidades
- Remove colunas: `CelularOrientado` e `CelularOrientador`
- Processa todos os arquivos CSV no diretório
- Preserva todos os outros dados
- Design orientado a objetos

#### Uso
```bash
python3 scripts/remove_phone_columns.py
```

#### Resultado
- 10 arquivos CSV processados (2016-2025)
- 2 colunas removidas de cada arquivo
- 35 → 33 colunas por arquivo

### 2. Processamento e Consolidação (`scripts/process_scholarships.py`)

Script principal que lê todos os CSVs, valida dados e gera JSON consolidado com estatísticas.

#### Funcionalidades
- Leitura de múltiplos arquivos CSV
- Validação e parsing de dados
- Geração de estatísticas abrangentes
- Exportação para JSON estruturado
- Design orientado a objetos com dataclasses

#### Uso
```bash
python3 scripts/process_scholarships.py
```

#### Saída
- `data/scholarships.json` (1.3 MB)
- 981 bolsas processadas (2015-2025)
- Metadados completos
- Estatísticas detalhadas

## Estrutura de Dados

### Scholarship (Dataclass)

```python
@dataclass
class Scholarship:
    id: str
    year: int
    management: str
    modality: str
    program: str
    value: Optional[float]
    start_date: str
    end_date: str
    funding_agency: str
    advisor_accepted: str
    advisor_accepted_date: str
    student_accepted: str
    student_accepted_date: str
    cancelled: str
    cancelled_by: str
    aware: str
    report_evaluation: str
    execution_campus: str
    advisor: str
    advisor_email: str
    advisor_campus: str
    student: str
    student_email: str
    student_cpf: str
    course: str
    campus: str
    notice: str
    project_code: str
    project_title: str
    research_project_code: str
    research_project_title: str
    knowledge_area: str
    grade_area: str
```

### JSON Output Structure

```json
{
  "metadata": {
    "generated_at": "2025-01-XX...",
    "total_records": 981,
    "source": "SIGPESQ - Sistema de Gestão de Pesquisa do IFES"
  },
  "statistics": {
    "total_scholarships": 981,
    "by_year": { "2015": 29, "2016": 59, ... },
    "by_campus": { "Serra": 500, ... },
    "by_modality": { "Iniciação Científica": 800, ... },
    "by_program": { "PIBIC": 400, ... },
    "total_value": 284716.00,
    "years_range": { "min": 2015, "max": 2025 }
  },
  "scholarships": [ ... ]
}
```

## Estatísticas Geradas

### Resumo Geral
- **Total de bolsas:** 981
- **Período:** 2015 - 2025
- **Campi:** 15
- **Modalidades:** 2
- **Programas:** 9
- **Valor total:** R$ 284.716,00

### Distribuição por Ano
| Ano  | Bolsas |
|------|--------|
| 2015 | 29     |
| 2016 | 59     |
| 2017 | 64     |
| 2018 | 68     |
| 2019 | 55     |
| 2020 | 107    |
| 2021 | 59     |
| 2022 | 74     |
| 2023 | 151    |
| 2024 | 215    |
| 2025 | 100    |

## Arquitetura

```
source/scholarships/*.csv
        ↓
remove_phone_columns.py (Privacy)
        ↓
CSV files (cleaned)
        ↓
process_scholarships.py (Processing)
        ↓
data/scholarships.json
        ↓
Documentation / Visualization
```

## Classes Implementadas

### remove_phone_columns.py
- `CSVColumnRemover` - Remove colunas específicas de CSVs

### process_scholarships.py
- `Scholarship` - Dataclass para representar uma bolsa
- `ScholarshipCSVReader` - Lê e parseia arquivos CSV
- `ScholarshipProcessor` - Processa múltiplos arquivos e gera estatísticas
- `ScholarshipJSONExporter` - Exporta dados para JSON

## Fluxo de Processamento

### Passo 1: Limpeza de Dados Sensíveis
1. Identifica arquivos CSV
2. Remove colunas de telefone
3. Preserva outros dados
4. Salva arquivos limpos

### Passo 2: Processamento e Consolidação
1. Lê todos os CSVs
2. Parseia cada registro
3. Valida dados
4. Gera estatísticas
5. Exporta JSON consolidado

### Passo 3: Disponibilização
1. JSON disponível em `data/scholarships.json`
2. Pronto para consumo por visualizações
3. Pode ser usado em páginas .md com Jinja2

## Uso no Build

O script `scripts/build.sh` automatiza todo o processo:

```bash
./scripts/build.sh
```

Executa:
1. Processamento de bolsas
2. Análise de parcerias
3. Build da documentação

## Próximos Passos Sugeridos

1. **Visualizações**:
   - Gráficos de evolução temporal
   - Distribuição por campus
   - Análise de programas

2. **Análises Avançadas**:
   - Taxa de conclusão
   - Tempo médio de bolsa
   - Relação com projetos de pesquisa

3. **Integração**:
   - Criar páginas .md para visualizar dados
   - Adicionar gráficos interativos
   - Conectar com dados de projetos

4. **Dashboards**:
   - Painel de bolsas ativas
   - Histórico de orientadores
   - Estatísticas por área de conhecimento

## Conformidade e Privacidade

✅ **LGPD Compliance:**
- Números de telefone removidos
- Dados sensíveis protegidos
- Apenas informações necessárias mantidas

✅ **Dados Mantidos:**
- Informações acadêmicas
- Dados de projeto
- Informações de orientação
- Emails institucionais

## Manutenção

Para atualizar os dados:

1. Adicione novos CSVs em `source/scholarships/`
2. Execute `python3 scripts/remove_phone_columns.py`
3. Execute `python3 scripts/process_scholarships.py`
4. JSON será atualizado automaticamente

## Logs e Monitoramento

O script fornece logs detalhados:
- ✓ Sucesso
- ℹ Informação
- ⚠ Aviso
- ✗ Erro

Exemplo de saída:
```
Processing: Relatorio_orientacoes_2024.xlsx - Relatório.csv
  ✓ Loaded 187 scholarship(s)
```
