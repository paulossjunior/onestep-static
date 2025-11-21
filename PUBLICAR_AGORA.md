# 🚀 Publicar Agora - Guia Rápido

## ⚡ 3 Passos para Publicar

### 1️⃣ Configurar GitHub Pages (Uma vez)

```
1. Abra: https://github.com/paulossjunior/onestep-static/settings/pages

2. Em "Source", selecione: GitHub Actions

3. Pronto! ✅
```

### 2️⃣ Configurar Permissões (Uma vez)

```
1. Abra: https://github.com/paulossjunior/onestep-static/settings/actions

2. Role até "Workflow permissions"

3. Selecione: ● Read and write permissions

4. Marque: ☑ Allow GitHub Actions to create and approve pull requests

5. Clique em "Save"
```

### 3️⃣ Fazer Push

```bash
# Adicionar todos os arquivos
git add .

# Commit
git commit -m "feat: add multilingual support with language selector"

# Push para GitHub
git push origin main
```

---

## 🎯 Acompanhar Deploy

### Ver Progresso

```
1. Abra: https://github.com/paulossjunior/onestep-static/actions

2. Você verá "Deploy to GitHub Pages" rodando

3. Aguarde 3-5 minutos ⏱️
```

### Status

```
● Running...  → Aguarde
✅ Success   → Site publicado!
❌ Failed    → Ver logs de erro
```

---

## 🌐 Acessar Site Publicado

Após o deploy concluir (3-5 min):

### Inglês
```
https://paulossjunior.github.io/onestep-static/
```

### Português
```
https://paulossjunior.github.io/onestep-static/pt/
```

---

## ✅ Verificar

- [ ] Site carrega
- [ ] Seletor de idioma visível (🌐 🇺🇸 EN 🇧🇷 PT)
- [ ] Clicar em PT funciona
- [ ] Clicar em EN funciona
- [ ] Gráficos aparecem
- [ ] Redes de colaboração funcionam

---

## 🔄 Atualizações Futuras

Sempre que quiser atualizar o site:

```bash
# 1. Fazer mudanças nos arquivos
# 2. Commit e push
git add .
git commit -m "sua mensagem"
git push origin main

# 3. Deploy automático! 🚀
```

---

## 🐛 Problemas?

### Deploy falhou?

```bash
# Testar localmente primeiro
cd onestep-static
mkdocs build --strict

# Se funcionar local, fazer push novamente
```

### Site não carrega?

```
1. Verificar se deploy concluiu (Actions)
2. Aguardar 5-10 minutos
3. Limpar cache: Ctrl+Shift+R
4. Verificar URL está correta
```

### Seletor não funciona?

```
1. Verificar console (F12)
2. Ver se há erros
3. Limpar cache do navegador
```

---

## 📚 Mais Informações

- **Guia Completo:** `GUIA_PUBLICACAO_GITHUB.md`
- **Verificação:** `VERIFICACAO_FINAL.md`
- **Teste:** `TESTE_RAPIDO.md`

---

## 🎉 Pronto!

Seu site estará online em:

```
🌐 https://paulossjunior.github.io/onestep-static/
```

Com suporte para:
- 🇺🇸 Inglês
- 🇧🇷 Português
- 📊 Gráficos interativos
- 🔗 Redes de colaboração
- 📱 Design responsivo

**Tempo total:** 10 minutos (primeira vez)  
**Deploy automático:** 3-5 minutos  
**Custo:** Gratuito! 🎉
