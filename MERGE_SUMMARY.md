# Resumo da Mesclagem de Dados

## ✅ Operação Concluída

Os dados do arquivo `supervisors_serra.csv` foram adicionados ao `data/scholar_ids.json`.

## 📊 Resultado

### Antes
- **8 pesquisadores** com Scholar ID

### Depois
- **113 pesquisadores** no total
- **8 com Scholar ID** (mantidos)
- **105 sem Scholar ID** (adicionados do CSV)

## 👥 Pesquisadores com Scholar ID

| Nome | Scholar ID |
|------|------------|
| Daniel Cruz Cavalieri | y6Smt-cAAAAJ |
| Fabiano Borges Ruy | StrLqxIAAAAJ |
| Francisco de Assis Boldt | cVUbNyMAAAAJ |
| Hilario Oliveira | Xp4tZ0cAAAAJ |
| Mateus Conrad Barcellos Da Costa | eH4gxyUAAAAJ |
| Paulo Sérgio Dos Santos Júnior | cFAEK0wAAAAJ |
| Rodrigo Fernandes Calhau | mrBLyX0AAAAJ |
| Sérgio Nery Simões | cWxRO1kAAAAJ |

## 📝 Pesquisadores Adicionados (Sem Scholar ID)

105 supervisores do campus Serra foram adicionados com `scholar_id: ""` (vazio).

Exemplos:
- Adelson Pereira Do Nascimento
- Adilson Ribeiro Prado
- Adonias Ribeiro Franco Junior
- Adriana Padua Lovatte
- Alextian Bartholomeu Liberato
- ... (e mais 100)

## 🔧 Como Foi Feito

### Script Utilizado
```bash
python3 merge_supervisors_to_scholar_ids.py
```

### Processo
1. Leu `data/scholar_ids.json` existente
2. Leu `supervisors_serra.csv`
3. Comparou nomes (case-insensitive)
4. Adicionou supervisores que não existiam
5. Ordenou alfabeticamente
6. Salvou arquivo atualizado

## 📁 Estrutura do JSON

```json
{
  "researchers": [
    {
      "name": "Nome do Pesquisador",
      "scholar_id": "ID_ou_vazio",
      "campus": "Serra"
    }
  ]
}
```

### Campos

- **name**: Nome completo do pesquisador/supervisor
- **scholar_id**: ID do Google Scholar (vazio se não disponível)
- **campus**: Campus do IFES (todos "Serra")

## 💡 Próximos Passos

### Adicionar Scholar IDs Manualmente

Para adicionar Scholar ID de um pesquisador:

```python
import json

# Ler arquivo
with open('data/scholar_ids.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Encontrar e atualizar pesquisador
for researcher in data['researchers']:
    if researcher['name'] == "Nome do Pesquisador":
        researcher['scholar_id'] = "NOVO_SCHOLAR_ID"
        break

# Salvar
with open('data/scholar_ids.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Buscar Scholar IDs Automaticamente

Criar script para buscar Scholar IDs por nome (requer web scraping ou API).

### Filtrar por Scholar ID

Para trabalhar apenas com pesquisadores que têm Scholar ID:

```python
import json

with open('data/scholar_ids.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filtrar apenas com Scholar ID
with_id = [r for r in data['researchers'] if r['scholar_id']]
print(f"Pesquisadores com Scholar ID: {len(with_id)}")
```

## 🔍 Verificação

### Validar JSON
```bash
python3 -m json.tool data/scholar_ids.json > /dev/null && echo "✓ JSON válido"
```

### Contar Pesquisadores
```bash
cat data/scholar_ids.json | grep '"name"' | wc -l
```

### Listar Com Scholar ID
```bash
cat data/scholar_ids.json | grep -B 1 '"scholar_id": "[a-zA-Z]' | grep '"name"'
```

### Listar Sem Scholar ID
```bash
cat data/scholar_ids.json | grep -B 1 '"scholar_id": ""' | grep '"name"' | head -10
```

## 📚 Arquivos Relacionados

- **Fonte CSV:** `supervisors_serra.csv`
- **Arquivo JSON:** `data/scholar_ids.json`
- **Script de mesclagem:** `merge_supervisors_to_scholar_ids.py`
- **Script de extração:** `extract_serra_supervisors.py`
- **Documentação:** `data/SCHOLAR_IDS_README.md`

## ⚠️ Notas Importantes

1. **Scholar IDs vazios** - Pesquisadores sem Scholar ID têm o campo vazio (`""`)
2. **Ordenação alfabética** - Lista ordenada por nome
3. **Sem duplicatas** - Script verifica nomes existentes antes de adicionar
4. **Case-insensitive** - Comparação de nomes ignora maiúsculas/minúsculas
5. **UTF-8** - Arquivo salvo com encoding UTF-8 para suportar acentuação

## 🎯 Uso no Sistema

Este arquivo pode ser usado para:

1. **Coleta seletiva** - Coletar dados apenas de pesquisadores com Scholar ID
2. **Lista completa** - Ter registro de todos os supervisores do campus
3. **Atualização gradual** - Adicionar Scholar IDs conforme disponíveis
4. **Relatórios** - Gerar relatórios de pesquisadores com/sem perfil Scholar

## ✅ Checklist de Verificação

- [x] CSV lido corretamente
- [x] JSON atualizado
- [x] Pesquisadores originais mantidos
- [x] Novos supervisores adicionados
- [x] Sem duplicatas
- [x] Ordenação alfabética
- [x] JSON válido
- [x] Encoding UTF-8
- [x] Documentação atualizada

---

**Data:** 2024-11-24  
**Origem:** supervisors_serra.csv (112 supervisores)  
**Destino:** data/scholar_ids.json (113 pesquisadores)  
**Status:** ✅ Concluído com sucesso
