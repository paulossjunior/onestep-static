# 🔧 Correção - GitHub Actions Workflow

## ❌ Problema Identificado

```
Error: Config file 'mkdocs.yml' does not exist.
Error: Process completed with exit code 1.
```

**Causa:** O workflow estava procurando `mkdocs.yml` na raiz do projeto, mas o arquivo está em `onestep-static/mkdocs.yml`.

---

## ✅ Solução Aplicada

### Arquivo Modificado

`.github/workflows/deploy-pages.yml`

### Mudanças

#### Antes (Incorreto)

```yaml
- name: Build with MkDocs
  run: |
    echo "Building documentation with MkDocs..."
    mkdocs build --clean --strict  # ❌ Procura na raiz

- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./site  # ❌ Caminho errado
```

#### Depois (Correto)

```yaml
- name: Build with MkDocs
  run: |
    echo "Building documentation with MkDocs..."
    cd onestep-static  # ✅ Entra no diretório correto
    mkdocs build --clean --strict

- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./onestep-static/site  # ✅ Caminho correto
```

---

## 🧪 Como Testar

### 1. Commit e Push

```bash
git add .github/workflows/deploy-pages.yml
git commit -m "fix: correct mkdocs path in workflow"
git push origin main
```

### 2. Acompanhar Deploy

```
1. Abra: https://github.com/paulossjunior/onestep-static/actions
2. Veja o workflow "Deploy to GitHub Pages" rodando
3. Aguarde conclusão (3-5 min)
```

### 3. Verificar Sucesso

```
✅ Build with MkDocs - Success
✅ Upload artifact - Success
✅ Deploy to GitHub Pages - Success
```

---

## 📊 Estrutura do Projeto

```
onestep-static/                    # Repositório
├── .github/
│   └── workflows/
│       └── deploy-pages.yml       # ✅ Corrigido
├── onestep-static/                # Diretório do MkDocs
│   ├── mkdocs.yml                 # ← Arquivo está aqui!
│   ├── docs/
│   │   ├── index.md
│   │   ├── index.pt.md
│   │   └── ...
│   └── site/                      # ← Build gera aqui
├── src/
│   └── *.py
└── data/
    └── *.json
```

---

## 🔍 Workflow Completo Corrigido

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 1. Checkout código
      - uses: actions/checkout@v4
      
      # 2. Setup Python
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      # 3. Instalar dependências
      - run: pip install -r requirements.txt
      
      # 4. Processar dados
      - run: python src/process_research_groups.py
      - run: python src/process_research_projects.py
      - run: python src/generate_network_stats.py
      
      # 5. Build MkDocs (CORRIGIDO)
      - run: |
          cd onestep-static
          mkdocs build --clean --strict
      
      # 6. Upload (CORRIGIDO)
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./onestep-static/site
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

---

## ✅ Checklist de Verificação

Após fazer push:

- [ ] Workflow iniciou sem erros
- [ ] Step "Build with MkDocs" passou
- [ ] Step "Upload artifact" passou
- [ ] Step "Deploy to GitHub Pages" passou
- [ ] Site acessível em: https://paulossjunior.github.io/onestep-static/

---

## 🐛 Se Ainda Houver Erros

### Erro: "No such file or directory"

**Verificar estrutura:**
```bash
# Verificar se mkdocs.yml existe
ls onestep-static/mkdocs.yml

# Deve mostrar: onestep-static/mkdocs.yml
```

### Erro: "Build failed"

**Testar localmente:**
```bash
cd onestep-static
mkdocs build --strict

# Ver erros
# Corrigir
# Push novamente
```

### Erro: "Permission denied"

**Verificar permissões:**
```
Settings → Actions → General
→ Workflow permissions
→ Read and write permissions
→ Save
```

---

## 📝 Comandos para Publicar

Agora você pode publicar:

```bash
# Adicionar mudanças
git add .

# Commit
git commit -m "fix: correct mkdocs path in workflow"

# Push
git push origin main
```

Ou usar o script:

```bash
./COMANDOS_PUBLICACAO.sh
```

---

## 🎯 Resultado Esperado

Após o push, o workflow deve:

```
1. ✅ Checkout repository
2. ✅ Setup Python
3. ✅ Install dependencies
4. ✅ Process research groups
5. ✅ Process research projects
6. ✅ Generate network statistics
7. ✅ Setup Pages
8. ✅ Build with MkDocs          ← Agora funciona!
9. ✅ Upload artifact            ← Caminho correto!
10. ✅ Deploy to GitHub Pages
```

---

## 🌐 Acessar Site

Após deploy concluir:

```
https://paulossjunior.github.io/onestep-static/
```

---

## 📚 Arquivos Relacionados

- **Workflow:** `.github/workflows/deploy-pages.yml` (corrigido)
- **Config:** `onestep-static/mkdocs.yml`
- **Guia:** `GUIA_PUBLICACAO_GITHUB.md`
- **Script:** `COMANDOS_PUBLICACAO.sh`

---

**Status:** ✅ Corrigido  
**Data:** 21 de Novembro de 2025  
**Versão:** 1.0.1
