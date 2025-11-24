# 🚀 Guia de Publicação - GitHub Pages

## 📋 Pré-requisitos

- ✅ Repositório no GitHub
- ✅ Código commitado
- ✅ GitHub Actions habilitado

---

## 🔧 Passo 1: Configurar GitHub Pages

### 1.1 Acessar Configurações do Repositório

```
1. Abra seu repositório no GitHub
   https://github.com/SEU-USUARIO/SEU-REPOSITORIO

2. Clique em "Settings" (Configurações)

3. No menu lateral esquerdo, clique em "Pages"
```

### 1.2 Configurar Source (Fonte)

```
Em "Build and deployment":

┌─────────────────────────────────────┐
│ Source: [GitHub Actions ▼]         │
└─────────────────────────────────────┘

Selecione "GitHub Actions" no dropdown
```

**⚠️ Importante:** 
- NÃO selecione "Deploy from a branch"
- Use "GitHub Actions"

### 1.3 Resultado

Você verá uma mensagem:
```
✅ Your site is ready to be published at 
   https://SEU-USUARIO.github.io/SEU-REPOSITORIO/
```

---

## 🔧 Passo 2: Verificar Permissões do Workflow

### 2.1 Acessar Actions Settings

```
1. Settings → Actions → General
2. Rolar até "Workflow permissions"
```

### 2.2 Configurar Permissões

```
Workflow permissions:

● Read and write permissions  ← Selecione esta opção

☑ Allow GitHub Actions to create and approve pull requests
```

### 2.3 Salvar

Clique em **"Save"** no final da página.

---

## 🔧 Passo 3: Adicionar site_url ao mkdocs.yml

Edite o arquivo `onestep-static/mkdocs.yml` e adicione a URL do seu site:

```yaml
site_name: OneStep - Static Report
site_url: https://SEU-USUARIO.github.io/SEU-REPOSITORIO/  # ← Adicione esta linha

theme:
  name: readthedocs
  # ... resto da configuração
```

**Exemplo:**
```yaml
site_url: https://paulossjunior.github.io/onestep-static/
```

---

## 🔧 Passo 4: Commit e Push

### 4.1 Adicionar Arquivos

```bash
git add .
```

### 4.2 Commit

```bash
git commit -m "feat: add multilingual support with language selector"
```

### 4.3 Push para GitHub

```bash
git push origin main
```

**Nota:** Se sua branch principal for `master`, use:
```bash
git push origin master
```

---

## 🔧 Passo 5: Acompanhar o Deploy

### 5.1 Acessar Actions

```
1. No GitHub, clique na aba "Actions"
2. Você verá o workflow "Deploy to GitHub Pages" rodando
```

### 5.2 Acompanhar Progresso

```
┌─────────────────────────────────────────────┐
│ Deploy to GitHub Pages                      │
│ ● Running...                                │
│                                             │
│ Jobs:                                       │
│ ✓ build     (2m 30s)                       │
│ ● deploy    (running...)                    │
└─────────────────────────────────────────────┘
```

### 5.3 Aguardar Conclusão

O processo leva cerca de 3-5 minutos:
- ✅ Build (2-3 min)
- ✅ Deploy (1-2 min)

---

## 🎉 Passo 6: Acessar o Site Publicado

### 6.1 URL do Site

Após o deploy concluir, acesse:

```
https://SEU-USUARIO.github.io/SEU-REPOSITORIO/
```

**Exemplo:**
```
https://paulossjunior.github.io/onestep-static/
```

### 6.2 Verificar Funcionalidades

- ✅ Site carrega
- ✅ Seletor de idioma visível (🌐 🇺🇸 EN 🇧🇷 PT)
- ✅ Troca de idioma funciona
- ✅ Todas as páginas acessíveis
- ✅ Gráficos carregam
- ✅ Redes de colaboração funcionam

---

## 🔄 Atualizações Futuras

### Processo Automático

Sempre que você fizer push para a branch `main`:

```bash
# 1. Fazer mudanças
vim onestep-static/docs/index.pt.md

# 2. Commit
git add .
git commit -m "docs: update Portuguese homepage"

# 3. Push
git push origin main

# 4. GitHub Actions faz deploy automaticamente! 🚀
```

### Acompanhar Deploy

```
1. GitHub → Actions
2. Ver workflow rodando
3. Aguardar conclusão (3-5 min)
4. Site atualizado automaticamente!
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "Workflow permissions"

**Sintoma:**
```
Error: Resource not accessible by integration
```

**Solução:**
```
Settings → Actions → General → Workflow permissions
→ Selecionar "Read and write permissions"
→ Save
```

### ❌ Erro: "Pages not enabled"

**Sintoma:**
```
Error: GitHub Pages is not enabled
```

**Solução:**
```
Settings → Pages
→ Source: GitHub Actions
→ Save
```

### ❌ Erro: "404 Not Found"

**Sintoma:**
Site não carrega, mostra erro 404

**Solução:**
```
1. Verificar se deploy concluiu (Actions)
2. Aguardar 5-10 minutos (propagação DNS)
3. Limpar cache do navegador (Ctrl+Shift+R)
4. Verificar URL está correta
```

### ❌ Erro: "Build failed"

**Sintoma:**
```
Error: Command 'mkdocs build' failed
```

**Solução:**
```bash
# Testar build localmente
cd onestep-static
mkdocs build --strict

# Ver erros
# Corrigir
# Commit e push novamente
```

### ❌ Seletor de idioma não funciona

**Sintoma:**
Seletor aparece mas links não funcionam

**Solução:**
```yaml
# Verificar site_url no mkdocs.yml
site_url: https://SEU-USUARIO.github.io/SEU-REPOSITORIO/

# Deve terminar com /
```

---

## 📊 Estrutura do Workflow

O arquivo `.github/workflows/deploy-pages.yml` já está configurado:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    - Process data
    - Build MkDocs
    - Upload artifact
  
  deploy:
    - Deploy to GitHub Pages
```

**Não precisa modificar este arquivo!**

---

## 🔍 Verificar Status do Deploy

### Via GitHub Interface

```
1. GitHub → Actions
2. Ver último workflow
3. Status:
   ✅ Success → Site publicado
   ❌ Failed → Ver logs de erro
   ● Running → Aguardar
```

### Via URL

```bash
# Verificar se site está online
curl -I https://SEU-USUARIO.github.io/SEU-REPOSITORIO/

# Resposta esperada:
# HTTP/2 200 OK
```

---

## 📝 Checklist de Publicação

### Antes do Push

- [ ] Código testado localmente (`mkdocs serve`)
- [ ] Build funciona (`mkdocs build --strict`)
- [ ] Seletor de idioma testado
- [ ] Todas as páginas acessíveis
- [ ] Sem erros no console

### Configuração GitHub

- [ ] GitHub Pages habilitado
- [ ] Source: GitHub Actions
- [ ] Workflow permissions: Read and write
- [ ] site_url configurado no mkdocs.yml

### Após o Push

- [ ] Workflow iniciou (Actions)
- [ ] Build concluiu com sucesso
- [ ] Deploy concluiu com sucesso
- [ ] Site acessível na URL
- [ ] Seletor de idioma funciona
- [ ] Ambos os idiomas acessíveis

---

## 🎯 URLs Importantes

### Repositório
```
https://github.com/SEU-USUARIO/SEU-REPOSITORIO
```

### Configurações
```
https://github.com/SEU-USUARIO/SEU-REPOSITORIO/settings
```

### Actions
```
https://github.com/SEU-USUARIO/SEU-REPOSITORIO/actions
```

### Site Publicado
```
https://SEU-USUARIO.github.io/SEU-REPOSITORIO/
```

### Site em Português
```
https://SEU-USUARIO.github.io/SEU-REPOSITORIO/pt/
```

---

## 🔐 Domínio Customizado (Opcional)

Se quiser usar um domínio próprio (ex: `pesquisa.ifes.edu.br`):

### 1. Adicionar CNAME

Crie o arquivo `onestep-static/docs/CNAME`:
```
pesquisa.ifes.edu.br
```

### 2. Configurar DNS

No seu provedor de DNS, adicione:
```
Type: CNAME
Name: pesquisa
Value: SEU-USUARIO.github.io
```

### 3. Aguardar Propagação

Pode levar até 24 horas.

### 4. Verificar

```bash
dig pesquisa.ifes.edu.br
# Deve apontar para SEU-USUARIO.github.io
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [GitHub Pages](https://docs.github.com/en/pages)
- [GitHub Actions](https://docs.github.com/en/actions)
- [MkDocs](https://www.mkdocs.org/)

### Logs e Debugging

```bash
# Ver logs do workflow
GitHub → Actions → Workflow → View logs

# Testar build localmente
mkdocs build --verbose

# Ver site local
mkdocs serve --verbose
```

---

## 🎉 Resumo

### Comandos Essenciais

```bash
# 1. Fazer mudanças
git add .
git commit -m "sua mensagem"
git push origin main

# 2. Aguardar deploy (3-5 min)

# 3. Acessar site
# https://SEU-USUARIO.github.io/SEU-REPOSITORIO/
```

### Fluxo Completo

```
Código Local
    ↓ (git push)
GitHub Repository
    ↓ (trigger)
GitHub Actions
    ↓ (build)
MkDocs Build
    ↓ (deploy)
GitHub Pages
    ↓ (publish)
Site Online! 🎉
```

---

**Tempo estimado:** 10-15 minutos (primeira vez)  
**Tempo de deploy:** 3-5 minutos (automático)  
**Custo:** Gratuito (GitHub Pages)

**Última Atualização:** 21 de Novembro de 2025  
**Versão:** 1.0.0
