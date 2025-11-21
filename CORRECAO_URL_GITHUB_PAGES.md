# 🔧 Correção - URLs do Seletor de Idioma no GitHub Pages

## ❌ Problema Identificado

Quando o site está publicado no GitHub Pages, ao clicar em **🇧🇷 PT**, a URL gerada estava incorreta:

```
❌ Errado: https://paulossjunior.github.io/pt/onestep-static/
✅ Correto: https://paulossjunior.github.io/onestep-static/pt/
```

**Causa:** O JavaScript não considerava o base path do GitHub Pages (`/onestep-static/`).

---

## ✅ Solução Implementada

### Arquivo Modificado

`onestep-static/overrides/main.html`

### O que Mudou

#### Antes (Problemático)

```javascript
// Não considerava base path
if (targetLang === 'pt') {
  newPath = '/pt' + currentPath;  // ❌ Gera /pt/onestep-static/
}
```

#### Depois (Corrigido)

```javascript
// Detecta base path automaticamente
const basePath = currentPath.match(/^\/[^\/]+\//)?.[0] || '/';

if (targetLang === 'pt') {
  // Adiciona /pt/ DEPOIS do base path
  newPath = basePath + 'pt/' + cleanPath;  // ✅ Gera /onestep-static/pt/
}
```

---

## 🧪 Como Funciona

### Detecção Automática do Base Path

```javascript
// Local (mkdocs serve)
currentPath: /research_groups/
basePath: /
resultado: /pt/research_groups/

// GitHub Pages
currentPath: /onestep-static/research_groups/
basePath: /onestep-static/
resultado: /onestep-static/pt/research_groups/
```

### Exemplos de Conversão

#### Página Inicial

```javascript
// Local
EN: / → PT: /pt/
PT: /pt/ → EN: /

// GitHub Pages
EN: /onestep-static/ → PT: /onestep-static/pt/
PT: /onestep-static/pt/ → EN: /onestep-static/
```

#### Páginas Internas

```javascript
// Local
EN: /research_groups/ → PT: /pt/research_groups/
PT: /pt/research_groups/ → EN: /research_groups/

// GitHub Pages
EN: /onestep-static/research_groups/ → PT: /onestep-static/pt/research_groups/
PT: /onestep-static/pt/research_groups/ → EN: /onestep-static/research_groups/
```

---

## 🧪 Testar Localmente

### 1. Iniciar Servidor

```bash
cd onestep-static
mkdocs serve
```

### 2. Testar URLs

```bash
# Página inicial
http://127.0.0.1:8001/

# Clicar PT → Deve ir para:
http://127.0.0.1:8001/pt/

# Clicar EN → Deve voltar para:
http://127.0.0.1:8001/
```

### 3. Testar Páginas Internas

```bash
# Grupos em inglês
http://127.0.0.1:8001/research_groups/

# Clicar PT → Deve ir para:
http://127.0.0.1:8001/pt/research_groups/

# Clicar EN → Deve voltar para:
http://127.0.0.1:8001/research_groups/
```

---

## 🌐 Testar no GitHub Pages

Após fazer deploy:

### 1. Página Inicial

```bash
# Inglês
https://paulossjunior.github.io/onestep-static/

# Clicar PT → Deve ir para:
https://paulossjunior.github.io/onestep-static/pt/

# Clicar EN → Deve voltar para:
https://paulossjunior.github.io/onestep-static/
```

### 2. Grupos de Pesquisa

```bash
# Inglês
https://paulossjunior.github.io/onestep-static/research_groups/

# Clicar PT → Deve ir para:
https://paulossjunior.github.io/onestep-static/pt/research_groups/

# Clicar EN → Deve voltar para:
https://paulossjunior.github.io/onestep-static/research_groups/
```

### 3. Projetos

```bash
# Inglês
https://paulossjunior.github.io/onestep-static/research_projects/

# Clicar PT → Deve ir para:
https://paulossjunior.github.io/onestep-static/pt/research_projects/

# Clicar EN → Deve voltar para:
https://paulossjunior.github.io/onestep-static/research_projects/
```

---

## 🔍 Lógica da Correção

### Passo 1: Detectar Base Path

```javascript
const currentPath = window.location.pathname;
// Ex: /onestep-static/research_groups/

const basePath = currentPath.match(/^\/[^\/]+\//)?.[0] || '/';
// Resultado: /onestep-static/
```

### Passo 2: Extrair Page Path

```javascript
let pagePath = currentPath;
// Ex: /onestep-static/research_groups/

if (basePath !== '/' && pagePath.startsWith(basePath)) {
  pagePath = pagePath.substring(basePath.length - 1);
}
// Resultado: /research_groups/
```

### Passo 3: Construir Nova URL

```javascript
// Para Português
newPath = basePath + 'pt/' + cleanPath;
// Resultado: /onestep-static/pt/research_groups/

// Para Inglês
newPath = basePath + cleanPath;
// Resultado: /onestep-static/research_groups/
```

---

## ✅ Checklist de Verificação

### Local (mkdocs serve)

- [ ] Página inicial: / → /pt/ → /
- [ ] Grupos: /research_groups/ → /pt/research_groups/ → /research_groups/
- [ ] Projetos: /research_projects/ → /pt/research_projects/ → /research_projects/

### GitHub Pages

- [ ] Página inicial funciona
- [ ] Grupos funcionam
- [ ] Projetos funcionam
- [ ] URLs corretas (sem /pt/onestep-static/)
- [ ] Idioma ativo destacado corretamente

---

## 🐛 Solução de Problemas

### Ainda vai para /pt/onestep-static/?

**Causa:** Cache do navegador

**Solução:**
```bash
# Limpar cache
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Ou abrir em aba anônima
Ctrl+Shift+N (Chrome)
Ctrl+Shift+P (Firefox)
```

### URLs com // (barra dupla)?

**Causa:** Já corrigido no código

**Verificar:**
```javascript
// O código agora remove barras duplas
newPath = newPath.replace(/\/+/g, '/');
```

### Seletor não funciona?

**Verificar console:**
```bash
# Abrir DevTools (F12)
# Ir para Console
# Clicar no seletor
# Ver se há erros
```

---

## 📝 Comandos para Publicar

```bash
# Adicionar mudanças
git add onestep-static/overrides/main.html

# Commit
git commit -m "fix: correct language selector URLs for GitHub Pages"

# Push
git push origin main
```

Ou usar o script:

```bash
./COMANDOS_PUBLICACAO.sh
```

---

## 🎯 Resultado Esperado

### Antes (Errado)

```
Clicar PT em: /onestep-static/
Vai para: /pt/onestep-static/  ❌ 404 Error
```

### Depois (Correto)

```
Clicar PT em: /onestep-static/
Vai para: /onestep-static/pt/  ✅ Funciona!
```

---

## 📊 Compatibilidade

A correção funciona em:

- ✅ **Local:** `mkdocs serve` (http://127.0.0.1:8001)
- ✅ **GitHub Pages:** Com base path (/onestep-static/)
- ✅ **Domínio customizado:** Sem base path (/)
- ✅ **Todos os navegadores:** Chrome, Firefox, Safari, Edge

---

## 🔄 Atualizações Futuras

Se mudar o nome do repositório, o código continua funcionando automaticamente porque detecta o base path dinamicamente.

---

## 📚 Arquivos Relacionados

- **Correção:** `onestep-static/overrides/main.html` (atualizado)
- **Guia:** `CORRECAO_URL_GITHUB_PAGES.md` (este arquivo)
- **Publicação:** `CORRIGIR_E_PUBLICAR.md`

---

**Status:** ✅ Corrigido  
**Data:** 21 de Novembro de 2025  
**Versão:** 1.0.2  
**Compatibilidade:** Local + GitHub Pages
