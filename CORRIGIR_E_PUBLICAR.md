# ⚡ Corrigir e Publicar - Guia Rápido

## ✅ Correção Aplicada

O erro do GitHub Actions foi corrigido! O workflow agora procura o `mkdocs.yml` no lugar correto.

---

## 🚀 Publicar Agora (3 Passos)

### 1️⃣ Commit e Push

```bash
# Adicionar todos os arquivos (incluindo workflow corrigido)
git add .

# Commit
git commit -m "fix: correct mkdocs path in workflow and add multilingual support"

# Push
git push origin main
```

### 2️⃣ Configurar GitHub Pages (Uma vez)

```
1. Abra: https://github.com/paulossjunior/onestep-static/settings/pages

2. Em "Source", selecione: GitHub Actions

3. Pronto! ✅
```

### 3️⃣ Configurar Permissões (Uma vez)

```
1. Abra: https://github.com/paulossjunior/onestep-static/settings/actions

2. Role até "Workflow permissions"

3. Selecione: ● Read and write permissions

4. Marque: ☑ Allow GitHub Actions to create and approve pull requests

5. Clique em "Save"
```

---

## 🎯 Acompanhar Deploy

### Ver Progresso

```
1. Abra: https://github.com/paulossjunior/onestep-static/actions

2. Você verá "Deploy to GitHub Pages" rodando

3. Aguarde 3-5 minutos ⏱️
```

### Verificar Sucesso

```
✅ Build with MkDocs - Success
✅ Upload artifact - Success  
✅ Deploy to GitHub Pages - Success
```

---

## 🌐 Acessar Site

Após deploy concluir:

```
https://paulossjunior.github.io/onestep-static/
```

---

## 🔍 O que Foi Corrigido

### Problema

```yaml
# Antes (errado)
- name: Build with MkDocs
  run: mkdocs build  # ❌ Procurava na raiz
```

### Solução

```yaml
# Depois (correto)
- name: Build with MkDocs
  run: |
    cd onestep-static  # ✅ Entra no diretório correto
    mkdocs build --clean --strict
```

---

## ✅ Checklist

### Antes do Push
- [x] Workflow corrigido
- [x] mkdocs.yml configurado
- [x] Seletor de idioma funcionando
- [x] Traduções completas

### Configuração GitHub (Uma vez)
- [ ] GitHub Pages: Source = GitHub Actions
- [ ] Workflow permissions: Read and write
- [ ] Allow GitHub Actions to create PRs

### Após o Push
- [ ] Workflow iniciou sem erros
- [ ] Build passou
- [ ] Deploy passou
- [ ] Site acessível

---

## 🐛 Se Houver Erro

### Erro: "mkdocs.yml does not exist"

**Já corrigido!** O workflow agora usa `cd onestep-static`.

### Erro: "Permission denied"

**Solução:**
```
Settings → Actions → General
→ Read and write permissions
→ Save
```

### Erro: "Build failed"

**Testar localmente:**
```bash
cd onestep-static
mkdocs build --strict
```

---

## 📚 Documentação

- **CORRECAO_WORKFLOW.md** - Detalhes da correção
- **GUIA_PUBLICACAO_GITHUB.md** - Guia completo
- **PUBLICAR_AGORA.md** - Guia rápido

---

## 🎉 Pronto!

Agora você pode publicar sem erros:

```bash
git add .
git commit -m "fix: correct workflow and add multilingual support"
git push origin main
```

Seu site estará online em 3-5 minutos! 🚀

---

**Status:** ✅ Corrigido e Pronto  
**Tempo:** 10 minutos  
**Custo:** Gratuito
