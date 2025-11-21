# 🌐 Seletor de Idioma - Guia Completo

## 📍 Localização

O seletor de idioma aparece **no canto superior direito** de todas as páginas do site.

```
┌─────────────────────────────────────────────┐
│  OneStep - Static Report      🌐 🇺🇸 EN 🇧🇷 PT │
│                                             │
│  Conteúdo da página...                      │
└─────────────────────────────────────────────┘
```

## 🎨 Aparência

O seletor tem:
- 🌐 Ícone de globo
- 🇺🇸 Bandeira dos EUA para inglês
- 🇧🇷 Bandeira do Brasil para português
- Botões clicáveis com hover effect
- Design responsivo para mobile

## 🔧 Como Funciona

### Implementação

O seletor foi implementado usando **3 métodos** para garantir compatibilidade:

#### 1. Plugin mkdocs-static-i18n
```yaml
plugins:
  - i18n:
      languages:
        - locale: en
        - locale: pt
```

#### 2. Template Override
- Arquivo: `onestep-static/overrides/main.html`
- Adiciona botões de idioma no topo da página
- Funciona com tema ReadTheDocs

#### 3. JavaScript Customizado
- Arquivo: `onestep-static/docs/js/language-selector.js`
- Detecta idioma atual
- Cria seletor dropdown
- Gerencia navegação entre idiomas

#### 4. CSS Customizado
- Arquivo: `onestep-static/docs/css/extra.css`
- Estilização do seletor
- Posicionamento fixo
- Responsividade mobile

## 🚀 Como Usar

### Para Usuários

1. **Abra o site**
   ```
   http://127.0.0.1:8001  (local)
   ou
   https://seu-site.github.io  (produção)
   ```

2. **Localize o seletor**
   - Canto superior direito
   - Ícone 🌐 com bandeiras

3. **Clique no idioma desejado**
   - 🇺🇸 EN → Inglês
   - 🇧🇷 PT → Português

4. **A página recarrega no idioma escolhido**
   - Mantém a mesma seção
   - URL atualizada automaticamente

### Para Desenvolvedores

#### Testar Localmente

```bash
cd onestep-static
mkdocs serve
# Abra http://127.0.0.1:8001
# Teste o seletor de idioma
```

#### Verificar URLs

**Inglês (padrão):**
```
/                          → Página inicial
/research_groups/          → Grupos de pesquisa
/research_projects/        → Projetos de pesquisa
```

**Português:**
```
/pt/                       → Página inicial
/pt/research_groups/       → Grupos de pesquisa
/pt/research_projects/     → Projetos de pesquisa
```

## 📱 Responsividade

### Desktop
```css
.language-switcher {
  top: 10px;
  right: 20px;
  padding: 10px 15px;
}
```

### Mobile (< 768px)
```css
.language-switcher {
  top: 5px;
  right: 10px;
  padding: 6px 10px;
  font-size: 12px;
}
```

## 🎨 Personalização

### Mudar Posição

Edite `onestep-static/docs/css/extra.css`:

```css
.language-switcher {
  /* Canto superior esquerdo */
  top: 10px;
  left: 20px;  /* em vez de right */
  
  /* Ou canto inferior direito */
  bottom: 10px;
  right: 20px;
}
```

### Mudar Cores

```css
.language-switcher {
  background: #your-color;
  border-color: #your-border-color;
}

.language-switcher a {
  color: #your-text-color;
}

.language-switcher a:hover {
  background: #your-hover-color;
}
```

### Adicionar Mais Idiomas

1. **Adicionar no mkdocs.yml:**
```yaml
languages:
  - locale: en
  - locale: pt
  - locale: es  # Espanhol
    name: Español
```

2. **Criar arquivos .es.md:**
```bash
touch onestep-static/docs/index.es.md
touch onestep-static/docs/research_groups.es.md
```

3. **Atualizar JavaScript:**
```javascript
const languages = {
    'en': { name: 'English', flag: '🇺🇸' },
    'pt': { name: 'Português', flag: '🇧🇷' },
    'es': { name: 'Español', flag: '🇪🇸' }
};
```

4. **Atualizar template HTML:**
```html
<a href="{{ page.url }}">🇺🇸 EN</a>
<a href="pt/{{ page.url }}">🇧🇷 PT</a>
<a href="es/{{ page.url }}">🇪🇸 ES</a>
```

## 🐛 Solução de Problemas

### Seletor não aparece

**Causa:** Arquivos não carregados

**Solução:**
```bash
# Verificar arquivos
ls onestep-static/docs/css/extra.css
ls onestep-static/docs/js/language-selector.js
ls onestep-static/overrides/main.html

# Reconstruir
mkdocs build --clean
```

### Links não funcionam

**Causa:** URLs incorretas

**Solução:**
1. Verificar estrutura de arquivos
2. Confirmar que arquivos .pt.md existem
3. Limpar cache do navegador

### Estilo quebrado

**Causa:** CSS não carregado

**Solução:**
```bash
# Verificar mkdocs.yml
grep "extra_css" onestep-static/mkdocs.yml

# Deve conter:
# extra_css:
#   - css/extra.css
```

## 📊 Estrutura de Arquivos

```
onestep-static/
├── mkdocs.yml                    # Configuração principal
├── overrides/
│   └── main.html                 # Template customizado
└── docs/
    ├── css/
    │   └── extra.css             # Estilos do seletor
    ├── js/
    │   └── language-selector.js  # Lógica do seletor
    ├── index.md                  # Inglês
    ├── index.pt.md               # Português
    ├── research_groups.md        # Inglês
    ├── research_groups.pt.md     # Português
    ├── research_projects.md      # Inglês
    └── research_projects.pt.md   # Português
```

## ✅ Checklist de Verificação

- [x] Plugin i18n instalado
- [x] Arquivos .pt.md criados
- [x] CSS customizado adicionado
- [x] JavaScript adicionado
- [x] Template override criado
- [x] mkdocs.yml configurado
- [x] Teste local realizado
- [x] Responsividade verificada

## 🎯 Resultado Final

Quando tudo estiver configurado, você terá:

✅ Seletor visível no canto superior direito  
✅ Botões com bandeiras (🇺🇸 EN / 🇧🇷 PT)  
✅ Hover effect nos botões  
✅ Navegação suave entre idiomas  
✅ URLs amigáveis (/pt/)  
✅ Design responsivo  
✅ Funciona em todos os navegadores  

## 📞 Suporte

Se o seletor não aparecer:

1. Verifique o console do navegador (F12)
2. Confirme que todos os arquivos existem
3. Teste com `mkdocs serve`
4. Limpe o cache: `mkdocs build --clean`

---

**Última Atualização:** 21 de Novembro de 2025  
**Versão:** 1.1.0
