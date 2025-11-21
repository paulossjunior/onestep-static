# 🧪 Testar URLs - Guia Rápido

## ⚡ Teste Rápido (2 minutos)

### 1️⃣ Testar Localmente

```bash
cd onestep-static
mkdocs serve
```

#### Teste 1: Página Inicial
```
1. Abrir: http://127.0.0.1:8001/
2. Clicar: 🇧🇷 PT
3. Verificar URL: http://127.0.0.1:8001/pt/  ✅
4. Clicar: 🇺🇸 EN
5. Verificar URL: http://127.0.0.1:8001/  ✅
```

#### Teste 2: Grupos
```
1. Abrir: http://127.0.0.1:8001/research_groups/
2. Clicar: 🇧🇷 PT
3. Verificar URL: http://127.0.0.1:8001/pt/research_groups/  ✅
4. Clicar: 🇺🇸 EN
5. Verificar URL: http://127.0.0.1:8001/research_groups/  ✅
```

---

### 2️⃣ Publicar e Testar no GitHub Pages

```bash
# Publicar
git add .
git commit -m "fix: correct language selector URLs for GitHub Pages"
git push origin main

# Aguardar 3-5 minutos
# Acessar: https://paulossjunior.github.io/onestep-static/
```

#### Teste 1: Página Inicial
```
1. Abrir: https://paulossjunior.github.io/onestep-static/
2. Clicar: 🇧🇷 PT
3. Verificar URL: https://paulossjunior.github.io/onestep-static/pt/  ✅
   (NÃO deve ser: /pt/onestep-static/)
4. Clicar: 🇺🇸 EN
5. Verificar URL: https://paulossjunior.github.io/onestep-static/  ✅
```

#### Teste 2: Grupos
```
1. Abrir: https://paulossjunior.github.io/onestep-static/research_groups/
2. Clicar: 🇧🇷 PT
3. Verificar URL: https://paulossjunior.github.io/onestep-static/pt/research_groups/  ✅
4. Clicar: 🇺🇸 EN
5. Verificar URL: https://paulossjunior.github.io/onestep-static/research_groups/  ✅
```

---

## ✅ URLs Corretas

### Local (mkdocs serve)

| Página | Inglês | Português |
|--------|--------|-----------|
| Inicial | `/` | `/pt/` |
| Grupos | `/research_groups/` | `/pt/research_groups/` |
| Projetos | `/research_projects/` | `/pt/research_projects/` |

### GitHub Pages

| Página | Inglês | Português |
|--------|--------|-----------|
| Inicial | `/onestep-static/` | `/onestep-static/pt/` |
| Grupos | `/onestep-static/research_groups/` | `/onestep-static/pt/research_groups/` |
| Projetos | `/onestep-static/research_projects/` | `/onestep-static/pt/research_projects/` |

---

## ❌ URLs Incorretas (Antes da Correção)

### Erros que NÃO devem mais acontecer:

```
❌ /pt/onestep-static/
❌ /pt/onestep-static/research_groups/
❌ /onestep-static//pt/research_groups/
```

---

## 🐛 Se Houver Problema

### URL ainda incorreta?

```bash
# Limpar cache do navegador
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Ou abrir em aba anônima
Ctrl+Shift+N
```

### Erro 404?

```bash
# Verificar se deploy concluiu
https://github.com/paulossjunior/onestep-static/actions

# Aguardar 5-10 minutos
# Tentar novamente
```

### Seletor não aparece?

```bash
# Verificar console (F12)
# Ver se há erros JavaScript
# Limpar cache
```

---

## 📊 Checklist Completo

### Local
- [ ] Página inicial: / ↔ /pt/
- [ ] Grupos: /research_groups/ ↔ /pt/research_groups/
- [ ] Projetos: /research_projects/ ↔ /pt/research_projects/
- [ ] Idioma ativo destacado
- [ ] Sem erros no console

### GitHub Pages
- [ ] Página inicial: /onestep-static/ ↔ /onestep-static/pt/
- [ ] Grupos: /onestep-static/research_groups/ ↔ /onestep-static/pt/research_groups/
- [ ] Projetos: /onestep-static/research_projects/ ↔ /onestep-static/pt/research_projects/
- [ ] URLs corretas (sem /pt/onestep-static/)
- [ ] Idioma ativo destacado
- [ ] Sem erros no console

---

## 🎉 Sucesso!

Se todos os testes passarem, o seletor de idioma está funcionando perfeitamente! 🚀

---

**Tempo:** 2 minutos  
**Dificuldade:** Fácil  
**Status esperado:** ✅ Tudo funcionando
