# Guia de Anonimização de Dados

## ⚠️ IMPORTANTE

Este guia explica como substituir dados reais por dados fake para fins de demonstração, testes ou publicação pública.

## 📋 O Que Será Anonimizado

### Dados Pessoais
- ✅ **Nomes** - Substituídos por nomes fictícios
- ✅ **Emails** - Substituídos por emails fake (@example.com, @fake.edu.br)
- ✅ **Scholar IDs** - Substituídos por IDs fictícios

### Dados de Pesquisa
- ✅ **Títulos de projetos** - Substituídos por títulos genéricos
- ✅ **Afiliações** - Substituídas por instituições fictícias
- ✅ **Datas** - Randomizadas mantendo formato

### Dados Financeiros
- ⚠️ **Valores de bolsas** - Randomizados +/- 20%
- ⚠️ **Total value** - Recalculado com valores fake

### Dados Mantidos
- ✅ **Estrutura JSON** - Mantida intacta
- ✅ **Campos e tipos** - Preservados
- ✅ **Estatísticas agregadas** - Recalculadas

## 🔧 Como Usar

### Passo 1: Backup Automático

O script cria backup automaticamente em `data_backup/`:

```bash
# Executar script de anonimização
bash anonymize_data.sh
```

### Passo 2: Confirmar Operação

O script pedirá confirmação:
```
Deseja continuar? (digite 'SIM' para confirmar):
```

Digite `SIM` e pressione Enter.

### Passo 3: Verificar Resultado

```bash
# Ver arquivos anonimizados
ls -la data/

# Verificar um arquivo
cat data/scholar_ids.json | head -30
```

### Passo 4: Testar Build

```bash
# Testar se o site ainda funciona
cd onestep-static
mkdocs build --verbose
mkdocs serve
```

## 🔄 Restaurar Dados Originais

Se precisar restaurar os dados reais:

```bash
# Executar script de restauração
bash restore_data.sh
```

Ou manualmente:
```bash
# Copiar backup de volta
cp data_backup/* data/
```

## 📊 Arquivos Afetados

| Arquivo | Dados Anonimizados |
|---------|-------------------|
| network_stats.json | Nomes, emails |
| papers.json | Nomes, emails, Scholar IDs, títulos, afiliações |
| partnership_analysis.json | Nomes, instituições |
| research_group.json | Nomes, emails |
| research_lines.json | Nomes, títulos de projetos |
| research_projects.json | Nomes, títulos, parceiros |
| scholar_ids.json | Nomes, Scholar IDs |
| scholarships.json | Nomes, valores (randomizados) |
| students.json | Nomes, valores (randomizados) |
| supervisors.json | Nomes, emails |

## 🎯 Casos de Uso

### 1. Demonstração Pública
```bash
# Anonimizar dados
bash anonymize_data.sh

# Publicar site
git add data/
git commit -m "feat: Use fake data for public demo"
git push
```

### 2. Desenvolvimento e Testes
```bash
# Anonimizar para testes
bash anonymize_data.sh

# Desenvolver features
# ...

# Restaurar dados reais
bash restore_data.sh
```

### 3. Compartilhamento de Código
```bash
# Anonimizar antes de compartilhar
bash anonymize_data.sh

# Compartilhar repositório
# ...

# Restaurar localmente
bash restore_data.sh
```

## 🔍 Verificação

### Verificar Anonimização

```bash
# Verificar se nomes foram substituídos
grep -r "Nome Real" data/

# Verificar se emails foram substituídos
grep -r "@ifes.edu.br" data/

# Verificar Scholar IDs
grep -r "cFAEK0wAAAAJ" data/
```

### Validar JSON

```bash
# Validar todos os arquivos JSON
for file in data/*.json; do
    python3 -m json.tool "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"
done
```

## 📝 Exemplo de Transformação

### Antes (Dados Reais)
```json
{
  "name": "Paulo Sérgio Dos Santos Júnior",
  "email": "paulo@ifes.edu.br",
  "scholar_id": "cFAEK0wAAAAJ",
  "affiliation": "Federal Institute of Espirito Santo",
  "value": 400.0
}
```

### Depois (Dados Fake)
```json
{
  "name": "Bruno Costa Lima",
  "email": "usuario123@example.com",
  "scholar_id": "FAKE456AAAA",
  "affiliation": "Universidade Federal de Exemplo",
  "value": 380.5
}
```

## ⚙️ Configuração

### Personalizar Dados Fake

Edite `generate_fake_data.py`:

```python
# Adicionar mais nomes fake
FAKE_NAMES = [
    "Seu Nome Fake 1",
    "Seu Nome Fake 2",
    # ...
]

# Adicionar mais títulos
FAKE_TITLES = [
    "Seu Título Fake 1",
    "Seu Título Fake 2",
    # ...
]
```

### Ajustar Randomização

```python
# Mudar variação de valores financeiros
def anonymize_value(value):
    variation = random.uniform(0.9, 1.1)  # +/- 10% em vez de 20%
    return round(value * variation, 2)
```

## 🔐 Segurança

### Dados Sensíveis

O script anonimiza:
- ✅ Nomes completos
- ✅ Endereços de email
- ✅ IDs do Google Scholar
- ✅ Títulos de projetos específicos
- ✅ Afiliações institucionais

### Dados Mantidos

O script mantém:
- ✅ Estrutura dos dados
- ✅ Tipos de dados
- ✅ Estatísticas agregadas
- ✅ Relacionamentos entre entidades

## 📊 Estatísticas

### Dados Fake Gerados

- **Nomes:** 30 nomes fictícios
- **Emails:** 3 domínios fake
- **Scholar IDs:** 4 padrões de ID
- **Títulos:** 10 títulos genéricos
- **Instituições:** 4 instituições fictícias

### Randomização

- **Valores financeiros:** +/- 20% do original
- **Datas:** Últimos 5 anos
- **Seleção:** Aleatória de listas predefinidas

## 🚨 Avisos

### ⚠️ Antes de Executar

1. **Faça backup manual** (além do automático)
2. **Commit dados reais** antes de anonimizar
3. **Teste em branch separada** primeiro
4. **Verifique se backup foi criado**

### ⚠️ Após Executar

1. **Não commite dados fake** no branch principal
2. **Use branch separada** para dados fake
3. **Documente** que são dados fake
4. **Restaure dados reais** quando necessário

## 🔄 Workflow Recomendado

### Para Demonstração Pública

```bash
# 1. Criar branch para demo
git checkout -b demo-public

# 2. Anonimizar dados
bash anonymize_data.sh

# 3. Commit dados fake
git add data/
git commit -m "demo: Use fake data for public demonstration"

# 4. Push branch demo
git push origin demo-public

# 5. Voltar para branch principal
git checkout main

# Dados reais permanecem no branch main
```

### Para Desenvolvimento

```bash
# 1. Anonimizar localmente
bash anonymize_data.sh

# 2. Desenvolver e testar
# ...

# 3. Restaurar dados reais
bash restore_data.sh

# 4. Commit código (sem dados fake)
git add src/ onestep-static/
git commit -m "feat: New feature"
git push
```

## 📚 Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `generate_fake_data.py` | Script Python de anonimização |
| `anonymize_data.sh` | Script bash com confirmação |
| `restore_data.sh` | Script para restaurar dados |
| `ANONYMIZATION_GUIDE.md` | Este guia |
| `FINANCIAL_DATA_REPORT.md` | Relatório de dados financeiros |

## ✅ Checklist

Antes de anonimizar:
- [ ] Backup manual criado
- [ ] Commit atual salvo
- [ ] Branch separada criada (se necessário)
- [ ] Entendeu o processo
- [ ] Sabe como restaurar

Após anonimizar:
- [ ] Backup automático verificado
- [ ] Dados fake validados (JSON válido)
- [ ] Build testado
- [ ] Site funciona corretamente
- [ ] Documentado que são dados fake

## 🆘 Problemas?

### Backup não foi criado
```bash
# Criar backup manual
mkdir -p data_backup
cp data/*.json data_backup/
```

### JSON inválido após anonimização
```bash
# Restaurar dados
bash restore_data.sh

# Ou manualmente
cp data_backup/*.json data/
```

### Script falhou
```bash
# Verificar erro
python3 generate_fake_data.py

# Restaurar se necessário
bash restore_data.sh
```

## 📞 Suporte

- **Documentação:** Este arquivo
- **Scripts:** `generate_fake_data.py`, `anonymize_data.sh`, `restore_data.sh`
- **Backup:** `data_backup/`

---

**⚠️ LEMBRE-SE:**
- Sempre faça backup antes de anonimizar
- Use branch separada para dados fake
- Não commite dados fake no branch principal
- Documente claramente quando usar dados fake

**Data:** 2024-11-24  
**Versão:** 1.0  
**Status:** Pronto para uso
