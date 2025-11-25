# Supervisores do Campus Serra - CSV

## 📄 Arquivo Gerado

**Arquivo:** `supervisors_serra.csv`

## 📊 Estatísticas

- **Total de supervisores:** 112
- **Campus:** Serra
- **Formato:** CSV (Comma-Separated Values)
- **Encoding:** UTF-8
- **Ordenação:** Alfabética

## 📋 Estrutura do CSV

```csv
Nome
Adelson Pereira Do Nascimento
Adilson Ribeiro Prado
...
```

### Colunas

| Coluna | Descrição |
|--------|-----------|
| Nome | Nome completo do supervisor |

## 🔧 Como Foi Gerado

### Script Utilizado

```bash
python3 extract_serra_supervisors.py
```

### Processo

1. Lê `data/supervisors.json`
2. Filtra supervisores com `campus == "Serra"`
3. Ordena alfabeticamente
4. Gera CSV com cabeçalho

## 📖 Exemplos de Uso

### Ler o CSV

```bash
# Ver primeiras linhas
head supervisors_serra.csv

# Ver últimas linhas
tail supervisors_serra.csv

# Contar total
wc -l supervisors_serra.csv

# Ver todos
cat supervisors_serra.csv
```

### Usar em Python

```python
import csv

with open('supervisors_serra.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['Nome'])
```

### Usar em Excel/LibreOffice

1. Abrir Excel ou LibreOffice Calc
2. Arquivo → Abrir
3. Selecionar `supervisors_serra.csv`
4. Confirmar encoding UTF-8

### Usar em Pandas

```python
import pandas as pd

df = pd.read_csv('supervisors_serra.csv')
print(df.head())
print(f"Total: {len(df)}")
```

## 📊 Amostra dos Dados

### Primeiros 10 Supervisores

1. Adelson Pereira Do Nascimento
2. Adilson Ribeiro Prado
3. Adonias Ribeiro Franco Junior
4. Adriana Padua Lovatte
5. Alextian Bartholomeu Liberato
6. Amarildo Mendes Lemos
7. André Assis Pires
8. André Gustavo De Sousa Galdino
9. Archimedes Alves Detoni
10. Arthur Eduardo Alves Amorim

### Últimos 10 Supervisores

103. Tatiane Policário Chagas
104. Thiago Meireles Paixão
105. Victor Dias Pirovani
106. Victorio Albani De Carvalho
107. Vinicius Da Rocha Motta
108. Vinicius Moura Marques
109. Vinícius Secchin De Melo
110. Vitor Faiçal Campana
111. Wagner Teixeira Da Costa
112. Wallas Gusmao Thomas

## 🔄 Regenerar o Arquivo

Se precisar regenerar o CSV:

```bash
# Executar script
python3 extract_serra_supervisors.py

# Verificar resultado
head supervisors_serra.csv
```

## 📁 Arquivos Relacionados

- **Fonte de dados:** `data/supervisors.json`
- **Script:** `extract_serra_supervisors.py`
- **Saída:** `supervisors_serra.csv`

## 🎯 Casos de Uso

### 1. Lista de Email

Combinar com dados de email para criar lista de contatos:

```python
import json
import csv

with open('data/supervisors.json', 'r') as f:
    data = json.load(f)

with open('supervisors_serra_emails.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Nome', 'Email'])
    
    for sup in data['supervisors']:
        if sup['campus'] == 'Serra':
            writer.writerow([sup['name'], sup.get('email', '')])
```

### 2. Análise Estatística

```python
import pandas as pd

df = pd.read_csv('supervisors_serra.csv')
print(f"Total de supervisores: {len(df)}")
print(f"Nomes únicos: {df['Nome'].nunique()}")
```

### 3. Importar para Banco de Dados

```sql
-- PostgreSQL
COPY supervisors(nome)
FROM '/path/to/supervisors_serra.csv'
DELIMITER ','
CSV HEADER;
```

## ✅ Validação

### Verificar Integridade

```bash
# Verificar encoding
file supervisors_serra.csv

# Verificar formato
head -1 supervisors_serra.csv  # Deve mostrar: Nome

# Contar linhas (deve ser 113: 1 cabeçalho + 112 supervisores)
wc -l supervisors_serra.csv
```

### Verificar Duplicatas

```bash
# Verificar se há nomes duplicados
sort supervisors_serra.csv | uniq -d
```

## 📝 Notas

- Todos os nomes estão em formato "Nome Completo"
- Ordenação alfabética case-sensitive
- Encoding UTF-8 para suportar acentuação
- Sem duplicatas
- Sem valores vazios

## 🔗 Links Relacionados

- **Dados completos:** [data/supervisors.json](data/supervisors.json)
- **Script de extração:** [extract_serra_supervisors.py](extract_serra_supervisors.py)

---

**Gerado em:** 2024-11-24  
**Fonte:** data/supervisors.json  
**Campus:** Serra  
**Total:** 112 supervisores
