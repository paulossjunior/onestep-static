# ⚡ Teste Rápido - Verificar Correção

## 🎯 Objetivo

Verificar se o erro ao selecionar inglês foi corrigido.

---

## 🚀 Passo a Passo (2 minutos)

### 1️⃣ Reiniciar o Servidor

```bash
# Se o servidor estiver rodando, pare (Ctrl+C)

# Reinicie
cd onestep-static
mkdocs serve
```

### 2️⃣ Teste Principal: PT → EN

```bash
# 1. Abrir no navegador:
http://127.0.0.1:8001/pt/

# 2. Verificar:
✅ Página em português
✅ Seletor visível: 🌐 🇺🇸 EN 🇧🇷 PT
✅ Botão PT destacado em azul

# 3. Clicar em: 🇺🇸 EN

# 4. Resultado esperado:
✅ URL muda para: http://127.0.0.1:8001/
✅ Página em inglês
✅ Botão EN destacado em azul
✅ SEM ERROS!
```

### 3️⃣ Teste Reverso: EN → PT

```bash
# 1. Já está em inglês (/)

# 2. Clicar em: 🇧🇷 PT

# 3. Resultado esperado:
✅ URL muda para: http://127.0.0.1:8001/pt/
✅ Página em português
✅ Botão PT destacado em azul
```

### 4️⃣ Teste em Página Interna

```bash
# 1. Ir para grupos em português:
http://127.0.0.1:8001/pt/research_groups/

# 2. Clicar em: 🇺🇸 EN

# 3. Resultado esperado:
✅ URL: http://127.0.0.1:8001/research_groups/
✅ Conteúdo em inglês
✅ SEM ERROS!
```

---

## ✅ Checklist Rápido

- [ ] Servidor reiniciado
- [ ] Teste PT → EN funciona
- [ ] Teste EN → PT funciona
- [ ] Teste em página interna funciona
- [ ] Sem erros no console (F12)
- [ ] Idioma ativo destacado corretamente

---

## 🎯 Se Tudo Funcionar

**Parabéns! 🎉** O erro foi corrigido!

Você pode agora:
```bash
# Fazer commit das mudanças
git add .
git commit -m "fix: correct language selector navigation"
git push origin main
```

---

## ❌ Se Ainda Houver Erro

### Verificar Console

```bash
# 1. Pressionar F12 (DevTools)
# 2. Ir para aba "Console"
# 3. Clicar no seletor de idioma
# 4. Ver se há erros em vermelho
```

### Verificar Arquivo

```bash
# Verificar se o arquivo foi atualizado
cat onestep-static/overrides/main.html | grep "switchLanguage"

# Deve mostrar a função switchLanguage
```

### Limpar Cache

```bash
# Limpar cache do MkDocs
cd onestep-static
mkdocs build --clean

# Reiniciar
mkdocs serve

# Limpar cache do navegador
# Ctrl+Shift+R (ou Cmd+Shift+R no Mac)
```

---

## 📞 Mais Informações

- **Detalhes da correção:** `CORRECAO_ERRO_IDIOMA.md`
- **Guia completo:** `SELETOR_IDIOMA.md`
- **Teste completo:** `VERIFICACAO_FINAL.md`

---

**Tempo estimado:** 2 minutos  
**Dificuldade:** Fácil  
**Status esperado:** ✅ Funcionando
