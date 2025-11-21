# 🚀 Teste Rápido - Seletor de Idioma

## ⚡ 3 Passos para Testar

### 1️⃣ Iniciar o Servidor

```bash
cd onestep-static
mkdocs serve
```

### 2️⃣ Abrir no Navegador

```
http://127.0.0.1:8001
```

### 3️⃣ Verificar o Seletor

Procure no **canto superior direito** da página:

```
🌐 🇺🇸 EN 🇧🇷 PT
```

---

## ✅ O que Testar (2 minutos)

### Teste 1: Seletor Visível
- [ ] Abrir página inicial
- [ ] Ver seletor no canto superior direito
- [ ] Ver ícone 🌐 e bandeiras 🇺🇸 🇧🇷

### Teste 2: Trocar para Português
- [ ] Clicar em **🇧🇷 PT**
- [ ] Página recarrega
- [ ] URL muda para `/pt/`
- [ ] Conteúdo em português
- [ ] Botão PT destacado em azul

### Teste 3: Voltar para Inglês
- [ ] Clicar em **🇺🇸 EN**
- [ ] Página recarrega
- [ ] URL muda para `/`
- [ ] Conteúdo em inglês
- [ ] Botão EN destacado em azul

### Teste 4: Hover Effect
- [ ] Passar mouse sobre botões
- [ ] Ver fundo mudar para azul
- [ ] Ver texto mudar para branco

### Teste 5: Mobile
- [ ] Pressionar F12 (DevTools)
- [ ] Pressionar Ctrl+Shift+M (Device Toolbar)
- [ ] Selecionar iPhone ou Android
- [ ] Verificar seletor ainda visível
- [ ] Verificar tamanho menor

---

## 🎯 Resultado Esperado

Se tudo estiver funcionando, você verá:

```
┌────────────────────────────────────────────┐
│  OneStep - Static Report    🌐 🇺🇸 EN 🇧🇷 PT │ ← Aqui!
│                                            │
│  Research Documentation - Campus Serra    │
│                                            │
│  Welcome to the research documentation...  │
└────────────────────────────────────────────┘
```

**Ao clicar em 🇧🇷 PT:**

```
┌────────────────────────────────────────────┐
│  OneStep - Static Report    🌐 🇺🇸 EN 🇧🇷 PT │
│                                            │
│  Documentação de Pesquisa - Campus Serra  │
│                                            │
│  Bem-vindo ao portal de documentação...    │
└────────────────────────────────────────────┘
```

---

## ❌ Problemas?

### Seletor não aparece?

```bash
# Limpar e reconstruir
mkdocs build --clean
mkdocs serve
```

### Erro ao iniciar?

```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Links não funcionam?

```bash
# Verificar arquivos
ls docs/*.pt.md

# Devem existir:
# index.pt.md
# research_groups.pt.md
# research_projects.pt.md
```

---

## 📚 Mais Informações

- **Guia Completo:** `SELETOR_IDIOMA.md`
- **Guia Rápido:** `GUIA_RAPIDO_PT.md`
- **Verificação:** `VERIFICACAO_FINAL.md`

---

## ✅ Tudo Funcionando?

**Parabéns! 🎉**

Seu site agora está bilíngue com seletor de idioma funcional!

**Próximo passo:**
```bash
# Fazer commit
git add .
git commit -m "feat: add multilingual support with language selector"
git push origin main
```

O GitHub Actions fará o deploy automático! 🚀
