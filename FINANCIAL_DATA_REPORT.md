# Relatório de Dados Financeiros

## ⚠️ DADOS FINANCEIROS ENCONTRADOS

Foram identificados **dados financeiros** nos seguintes arquivos:

### 1. data/students.json ✅
- **Campo:** `value` (valor da bolsa)
- **Tipo:** Número (float)
- **Exemplos de valores:**
  - `0.0` - Voluntários (sem bolsa)
  - `100.0` - Bolsas de R$ 100,00
  - `300.0` - Bolsas de R$ 300,00
  - `400.0` - Bolsas de R$ 400,00
  - `700.0` - Bolsas de R$ 700,00
  - `800.0` - Bolsas de R$ 800,00
  - `900.0` - Bolsas de R$ 900,00
  - `null` - Valor não informado

### 2. data/scholarships.json ✅
- **Campo 1:** `value` (valor individual da bolsa)
- **Campo 2:** `total_value` (valor total agregado)
- **Tipo:** Número (float)
- **Exemplo de total_value:** `177408.0` (R$ 177.408,00)

## 📊 Estrutura dos Dados Financeiros

### Em students.json

```json
{
  "ic_scholarships": [
    {
      "id": "12345",
      "student": "Nome do Estudante",
      "advisor": "Nome do Orientador",
      "year": 2024,
      "modality": "Bolsista",
      "program": "Pibic",
      "value": 400.0,  // ⚠️ DADO FINANCEIRO
      "start_date": "01-08-24",
      "end_date": "31-07-25"
    }
  ]
}
```

### Em scholarships.json

```json
{
  "metadata": {
    "total_value": 177408.0  // ⚠️ DADO FINANCEIRO AGREGADO
  },
  "scholarships": [
    {
      "id": "12345",
      "student": "Nome do Estudante",
      "advisor": "Nome do Orientador",
      "year": 2024,
      "modality": "Bolsista",
      "program": "Pibic",
      "value": 400.0,  // ⚠️ DADO FINANCEIRO
      "start_date": "01-08-24",
      "end_date": "31-07-25"
    }
  ]
}
```

## 🔍 Análise dos Valores

### Valores Encontrados (em Reais)

| Valor | Tipo | Programa Típico |
|-------|------|-----------------|
| 0.0 | Voluntário | Pivic, Piviti |
| 100.0 | Bolsa | Pibic-Jr, Pibic-EM |
| 300.0 | Bolsa | Pibic-Jr, Propós |
| 400.0 | Bolsa | Pibic, Pibiti |
| 700.0 | Bolsa | Pibic |
| 800.0 | Bolsa | Pibic, Pibiti |
| 900.0 | Bolsa | Pibic, Pibiti |
| null | Não informado | Vários |

### Total Agregado

- **scholarships.json:** R$ 177.408,00 (total_value)

## ⚠️ Considerações de Privacidade

### Dados Sensíveis

Os valores de bolsas podem ser considerados **dados financeiros sensíveis** dependendo do contexto:

1. **Valores individuais** - Mostram quanto cada estudante recebe
2. **Valores agregados** - Mostram investimento total em pesquisa
3. **Histórico temporal** - Permite rastrear mudanças nos valores

### Recomendações

#### Opção 1: Manter os Dados (Justificativa)
- ✅ Valores de bolsas são públicos (editais CNPq/FAPES)
- ✅ Transparência em investimento público
- ✅ Útil para análises e relatórios
- ✅ Não identifica renda pessoal dos estudantes

#### Opção 2: Anonimizar Valores
- Remover campo `value` dos arquivos
- Manter apenas `modality` (Bolsista/Voluntário)
- Remover `total_value` das estatísticas

#### Opção 3: Agregar Apenas
- Manter apenas estatísticas agregadas
- Remover valores individuais
- Mostrar apenas totais por programa/ano

## 🛠️ Scripts para Remoção (Se Necessário)

### Remover campo 'value' de students.json

```python
import json

with open('data/students.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remover campo 'value' de todas as bolsas
for student in data['students']:
    for scholarship in student.get('ic_scholarships', []):
        if 'value' in scholarship:
            del scholarship['value']

# Salvar arquivo
with open('data/students.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Campo 'value' removido de students.json")
```

### Remover campos financeiros de scholarships.json

```python
import json

with open('data/scholarships.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remover total_value dos metadados
if 'total_value' in data['metadata']:
    del data['metadata']['total_value']

# Remover campo 'value' de todas as bolsas
for scholarship in data['scholarships']:
    if 'value' in scholarship:
        del scholarship['value']

# Salvar arquivo
with open('data/scholarships.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Campos financeiros removidos de scholarships.json")
```

### Substituir valores por categorias

```python
import json

def categorize_value(value):
    """Converte valor numérico em categoria"""
    if value is None:
        return "não informado"
    elif value == 0:
        return "voluntário"
    elif value <= 200:
        return "bolsa baixa"
    elif value <= 500:
        return "bolsa média"
    else:
        return "bolsa alta"

with open('data/students.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Substituir valores por categorias
for student in data['students']:
    for scholarship in student.get('ic_scholarships', []):
        if 'value' in scholarship:
            scholarship['value_category'] = categorize_value(scholarship['value'])
            del scholarship['value']

# Salvar arquivo
with open('data/students.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Valores substituídos por categorias")
```

## 📋 Checklist de Decisão

- [ ] Avaliar se valores de bolsas são considerados sensíveis
- [ ] Verificar políticas de privacidade da instituição
- [ ] Consultar LGPD (Lei Geral de Proteção de Dados)
- [ ] Decidir entre: manter, anonimizar ou agregar
- [ ] Atualizar documentação se houver mudanças
- [ ] Testar scripts antes de aplicar em produção
- [ ] Fazer backup dos arquivos originais

## 💡 Recomendação

### Minha Sugestão: **MANTER OS DADOS**

**Justificativa:**

1. **Valores públicos** - Bolsas de IC são valores tabelados e públicos
2. **Transparência** - Importante para prestação de contas
3. **Não é renda pessoal** - É auxílio institucional, não salário
4. **Útil para análises** - Permite estudos sobre investimento em pesquisa
5. **Já é público** - Valores estão em editais e portarias

**Mas considere:**
- Adicionar nota explicativa no site
- Deixar claro que são valores institucionais
- Não associar com dados pessoais sensíveis

## 📝 Nota Explicativa Sugerida

Para adicionar ao site:

```markdown
**Sobre os valores de bolsas:**
Os valores apresentados referem-se às bolsas de iniciação científica 
conforme editais públicos das agências de fomento (CNPq, FAPES, etc.). 
Estes valores são tabelados e públicos, não constituindo informação 
financeira pessoal dos estudantes.
```

## 🔗 Referências

- [LGPD - Lei 13.709/2018](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [CNPq - Valores de Bolsas](https://www.gov.br/cnpq/pt-br/acesso-a-informacao/acoes-e-programas/programas-induzidos/pibic)
- [FAPES - Editais](https://fapes.es.gov.br/)

---

**Data do Relatório:** 2024-11-24  
**Arquivos Analisados:** data/students.json, data/scholarships.json  
**Status:** ⚠️ Dados financeiros identificados - Aguardando decisão
