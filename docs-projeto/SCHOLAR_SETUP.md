# Google Scholar Integration Setup

Este documento explica como configurar e usar a integração com Google Scholar para buscar publicações dos pesquisadores.

## Visão Geral

O sistema busca dados de publicações do Google Scholar para pesquisadores do Campus Serra listados em `data/supervisors.json`. Os dados são processados e exibidos na página Papers do site.

## Arquivos Principais

- `data/scholar_ids.json` - Mapeamento de pesquisadores para seus IDs do Google Scholar
- `data/serra_researchers_papers.json` - Dados consolidados de publicações
- `data/scholar_{id}.json` - Dados individuais de cada pesquisador
- `src/fetch_all_researchers_papers.py` - Script para buscar dados do Scholar
- `src/process_papers_from_json.py` - Script para gerar páginas a partir do JSON

## Como Adicionar Pesquisadores

### 1. Encontrar o Scholar ID

Para adicionar um pesquisador, você precisa encontrar seu Google Scholar ID:

1. Acesse [Google Scholar](https://scholar.google.com)
2. Busque pelo nome do pesquisador
3. Clique no perfil do pesquisador
4. O ID está na URL: `https://scholar.google.com/citations?user=SCHOLAR_ID`

**Exemplo:**
- URL: `https://scholar.google.com/citations?user=cFAEK0wAAAAJ`
- Scholar ID: `cFAEK0wAAAAJ`

### 2. Adicionar ao arquivo scholar_ids.json

Edite o arquivo `data/scholar_ids.json` e adicione o pesquisador:

```json
{
  "researchers": [
    {
      "name": "Paulo Sérgio Dos Santos Júnior",
      "scholar_id": "cFAEK0wAAAAJ",
      "campus": "Serra",
      "email": "paulo.junior@ifes.edu.br"
    },
    {
      "name": "Nome Do Novo Pesquisador",
      "scholar_id": "NOVO_SCHOLAR_ID",
      "campus": "Serra",
      "email": "email@ifes.edu.br"
    }
  ],
  "total": 2,
  "updated_at": "2025-11-23 10:00:00"
}
```

**Importante:** O campo `name` deve corresponder EXATAMENTE ao nome no arquivo `data/supervisors.json`.

### 3. Buscar Dados do Scholar

Execute o comando para buscar os dados:

```bash
make fetch-scholar-data
```

Ou diretamente:

```bash
export SEARCHAPI_API_KEY=sua_chave_aqui
python3 src/fetch_all_researchers_papers.py
```

Este script irá:
- Ler os IDs do `scholar_ids.json`
- Buscar dados do Google Scholar para cada pesquisador
- Salvar dados individuais em `data/scholar_{id}.json`
- Gerar arquivo consolidado `data/serra_researchers_papers.json`

### 4. Gerar Páginas

Execute o comando para gerar as páginas HTML:

```bash
make process-papers-json
```

Ou diretamente:

```bash
python3 src/process_papers_from_json.py
```

Este script irá:
- Ler dados de `data/serra_researchers_papers.json`
- Calcular estatísticas globais
- Gerar `onestep-static/docs/papers.md` (inglês)
- Gerar `onestep-static/docs/papers.pt.md` (português)

## Estrutura dos Dados

### scholar_ids.json

```json
{
  "researchers": [
    {
      "name": "Nome Completo",
      "scholar_id": "ID_DO_SCHOLAR",
      "campus": "Serra",
      "email": "email@ifes.edu.br"
    }
  ],
  "total": 1,
  "updated_at": "2025-11-23 10:00:00"
}
```

### serra_researchers_papers.json

```json
{
  "campus": "Serra",
  "total_researchers": 1,
  "generated_at": "2025-11-23T10:00:00",
  "researchers": [
    {
      "researcher": {
        "name": "Nome",
        "campus": "Serra",
        "scholar_id": "ID",
        "scholar_url": "URL",
        "affiliation": "Afiliação",
        "email": "Email",
        "interests": ["Interesse 1", "Interesse 2"]
      },
      "statistics": {
        "total_papers": 20,
        "total_citations": 403,
        "average_citations_per_paper": 20.15,
        "h_index": {"all_time": "11", "since_2020": "7"},
        "i10_index": {"all_time": "11", "since_2020": "6"},
        "papers_by_year": {"2024": 1, "2023": 2},
        "citations_by_year": [{"year": 2024, "citations": 30}]
      },
      "top_5_papers": [...],
      "all_papers": [...]
    }
  ]
}
```

## Workflow Completo

```bash
# 1. Adicione IDs ao scholar_ids.json manualmente

# 2. Busque dados do Scholar
make fetch-scholar-data

# 3. Gere as páginas
make process-papers-json

# 4. Copie dados para docs e construa o site
make build-docs

# 5. Visualize localmente
make serve-docs
```

## Troubleshooting

### Erro: "Nenhum ID do Scholar encontrado"

Verifique se o arquivo `data/scholar_ids.json` existe e contém pesquisadores.

### Erro: "Scholar ID não encontrado"

Certifique-se de que:
1. O nome no `scholar_ids.json` corresponde EXATAMENTE ao nome em `supervisors.json`
2. O Scholar ID está correto

### Erro: "503 Service Unavailable"

A API do SearchAPI pode estar temporariamente indisponível. Aguarde alguns minutos e tente novamente.

### Pesquisador não aparece na página

Verifique:
1. O pesquisador está em `supervisors.json` com `campus: "Serra"`
2. O nome corresponde exatamente entre os arquivos
3. Os dados foram buscados com sucesso (verifique `data/scholar_{id}.json`)
4. As páginas foram regeneradas com `make process-papers-json`

## Configuração da API

A chave da API SearchAPI deve estar configurada:

```bash
# No arquivo .env
SEARCHAPI_API_KEY=sua_chave_aqui

# Ou como variável de ambiente
export SEARCHAPI_API_KEY=sua_chave_aqui
```

## Limitações

- O script processa apenas pesquisadores do Campus Serra
- É necessário ter o Scholar ID de cada pesquisador
- A API tem limites de requisições (aguarda 2 segundos entre cada requisição)
- Nem todos os pesquisadores têm perfil no Google Scholar

## Manutenção

Para atualizar os dados periodicamente:

```bash
# Atualizar dados do Scholar (busca novos artigos)
make fetch-scholar-data

# Regenerar páginas
make process-papers-json

# Reconstruir site
make build-docs
```

Recomenda-se atualizar os dados mensalmente ou quando houver novas publicações significativas.
