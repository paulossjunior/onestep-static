# Guia do Makefile - OneStep Research Observatory

Este documento descreve como usar o Makefile para gerenciar o projeto OneStep Research Observatory.

## Visão Geral

O Makefile fornece comandos convenientes para:
- Instalar dependências
- Processar dados de pesquisa
- Construir documentação
- Executar testes e verificações de qualidade
- Fazer deploy

## Comandos Disponíveis

### Ajuda

```bash
make help
```
Mostra todos os comandos disponíveis com suas descrições.

### Instalação

```bash
make install
```
Instala todas as dependências Python do projeto.

```bash
make install-dev
```
Instala dependências de desenvolvimento (pytest, black, flake8, mypy).

### Limpeza

```bash
make clean
```
Remove arquivos gerados (cache Python, site construído, etc.).

```bash
make clean-data
```
Remove todos os arquivos JSON processados (⚠️ **CUIDADO**: isso apaga os dados processados).

### Processamento de Dados

#### Pipeline Completo

```bash
make process-all
```
Executa todo o pipeline de processamento de dados na ordem correta:
1. Processa grupos de pesquisa
2. Processa projetos de pesquisa
3. Processa bolsas
4. Calcula recorrência de estudantes
5. Agrega dados por estudante
6. Agrega dados por orientador
7. Analisa parcerias
8. Gera estatísticas de rede

#### Comandos Individuais

```bash
make process-groups          # Processa grupos de pesquisa
make process-projects        # Processa projetos de pesquisa
make process-scholarships    # Processa bolsas IC
make calculate-recurrence    # Calcula recorrência de estudantes
make aggregate-students      # Agrega dados por estudante
make aggregate-supervisors   # Agrega dados por orientador
make analyze-partnerships    # Analisa parcerias
make analyze-networks        # Gera estatísticas de rede
```

### Documentação

```bash
make copy-data
```
Copia arquivos JSON para o diretório de documentação.

```bash
make build-docs
```
Constrói a documentação MkDocs (inclui `copy-data`).

```bash
make serve-docs
```
Inicia servidor de desenvolvimento local em http://127.0.0.1:8000

```bash
make translate-docs
```
Traduz documentação para português.

### Workflow Completo

```bash
make build
```
Executa `process-all` + `build-docs` - pipeline completo de processamento e construção.

```bash
make dev
```
Instala dependências e inicia servidor de desenvolvimento.

### Qualidade de Código

```bash
make lint
```
Executa verificação de código com flake8.

```bash
make format
```
Formata código com black.

```bash
make type-check
```
Verifica tipos com mypy.

```bash
make test
```
Executa testes (se disponíveis).

### Informações

```bash
make status
```
Mostra status dos arquivos de dados (quais existem, tamanhos, etc.).

```bash
make info
```
Mostra informações do projeto e guia de início rápido.

### Deploy

```bash
make deploy
```
Prepara para deploy (mostra comandos git necessários).

## Exemplos de Uso

### Início Rápido

```bash
# 1. Instalar dependências
make install

# 2. Processar todos os dados
make process-all

# 3. Visualizar documentação localmente
make serve-docs
```

### Desenvolvimento

```bash
# Instalar e iniciar servidor de desenvolvimento
make dev
```

### Atualização de Dados

```bash
# Processar apenas projetos de pesquisa
make process-projects

# Reagregar dados de estudantes
make aggregate-students

# Reconstruir documentação
make build-docs
```

### Verificação de Qualidade

```bash
# Formatar código
make format

# Verificar linting
make lint

# Verificar tipos
make type-check
```

### Pipeline Completo

```bash
# Limpar tudo
make clean

# Processar dados e construir documentação
make build

# Verificar status
make status
```

## Estrutura do Projeto

```
.
├── source/              # Dados CSV originais
│   ├── research_project/
│   ├── scholarships/
│   └── research_groups/
├── src/                 # Scripts Python
├── data/                # Dados JSON processados
├── onestep-static/      # Documentação MkDocs
│   ├── docs/
│   └── site/           # Site construído
├── Makefile            # Este arquivo
└── requirements.txt    # Dependências Python
```

## Fluxo de Trabalho CI/CD

O GitHub Actions usa o Makefile para:

1. `make install` - Instalar dependências
2. `make status` - Verificar status
3. `make process-groups` - Processar grupos
4. `make process-projects` - Processar projetos
5. `make process-scholarships` - Processar bolsas
6. `make calculate-recurrence` - Calcular recorrência
7. `make aggregate-students` - Agregar estudantes
8. `make aggregate-supervisors` - Agregar orientadores
9. `make analyze-partnerships` - Analisar parcerias
10. `make analyze-networks` - Gerar estatísticas de rede
11. `make copy-data` - Copiar dados
12. `mkdocs build` - Construir documentação
13. Deploy para GitHub Pages

## Troubleshooting

### Erro: "make: command not found"

**Solução**: Instale o make:
```bash
# Ubuntu/Debian
sudo apt-get install make

# macOS
xcode-select --install

# Windows (use WSL ou Git Bash)
```

### Erro: "python3: command not found"

**Solução**: Instale Python 3.8+:
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3
```

### Erro ao processar dados

**Solução**: Verifique se os arquivos CSV existem:
```bash
make status
ls -la source/research_project/
ls -la source/scholarships/
ls -la source/research_groups/
```

### Documentação não atualiza

**Solução**: Limpe e reconstrua:
```bash
make clean
make build
```

## Dicas

1. **Use `make help`** para ver todos os comandos disponíveis
2. **Use `make status`** para verificar o estado dos dados
3. **Use `make dev`** para desenvolvimento rápido
4. **Use `make build`** antes de fazer commit
5. **Comandos são idempotentes** - pode executar múltiplas vezes

## Variáveis de Ambiente

O Makefile usa estas variáveis (podem ser sobrescritas):

```bash
PYTHON=python3          # Interpretador Python
SRC_DIR=src            # Diretório de scripts
DATA_DIR=data          # Diretório de dados
DOCS_DIR=onestep-static # Diretório de documentação
```

Exemplo de sobrescrita:
```bash
make build PYTHON=python3.12
```

## Contribuindo

Ao adicionar novos scripts:

1. Adicione um target no Makefile
2. Adicione ao `process-all` se fizer parte do pipeline
3. Atualize este guia
4. Atualize o CI/CD se necessário

## Suporte

Para problemas ou dúvidas:
- Verifique `make status`
- Consulte `make info`
- Veja logs de erro detalhados
- Abra uma issue no GitHub
