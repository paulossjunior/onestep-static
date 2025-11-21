# Configuração Multilíngue / Multilingual Setup

## 🌍 Visão Geral / Overview

Este projeto agora suporta dois idiomas: **Inglês (English)** e **Português Brasileiro (Portuguese - Brazil)**.

This project now supports two languages: **English** and **Portuguese (Brazil)**.

---

## 📁 Estrutura de Arquivos / File Structure

```
onestep-static/docs/
├── index.md                    # Página inicial em inglês / English homepage
├── index.pt.md                 # Página inicial em português / Portuguese homepage
├── research_groups.md          # Grupos de pesquisa em inglês / Research groups in English
├── research_groups.pt.md       # Grupos de pesquisa em português / Research groups in Portuguese
├── research_projects.md        # Projetos em inglês / Projects in English
└── research_projects.pt.md     # Projetos em português / Projects in Portuguese
```

## 🔧 Configuração / Configuration

O suporte multilíngue é configurado no arquivo `onestep-static/mkdocs.yml` usando o plugin `mkdocs-static-i18n`:

The multilingual support is configured in `onestep-static/mkdocs.yml` using the `mkdocs-static-i18n` plugin:

```yaml
plugins:
  - i18n:
      docs_structure: suffix
      fallback_to_default: true
      reconfigure_material: true
      reconfigure_search: true
      languages:
        - locale: en
          default: true
          name: English
          build: true
        - locale: pt
          name: Português (Brasil)
          build: true
          nav_translations:
            Research Groups: Grupos de Pesquisa
            Research Projects: Projetos de Pesquisa
```

## 🚀 Como Usar / How to Use

### Visualizar Localmente / View Locally

```bash
# Instalar dependências / Install dependencies
pip install -r requirements.txt

# Navegar para o diretório / Navigate to directory
cd onestep-static

# Iniciar servidor de desenvolvimento / Start development server
mkdocs serve

# Abrir no navegador / Open in browser
# http://127.0.0.1:8001
```

O seletor de idioma aparecerá automaticamente na barra de navegação superior.

The language selector will appear automatically in the top navigation bar.

### Build para Produção / Production Build

```bash
cd onestep-static
mkdocs build --clean --strict
```

O site será gerado no diretório `site/` com suporte completo para ambos os idiomas.

The site will be generated in the `site/` directory with full support for both languages.

## ✏️ Adicionando Traduções / Adding Translations

### Para adicionar uma nova página / To add a new page:

1. **Criar versão em inglês / Create English version:**
   ```bash
   # Exemplo / Example
   touch onestep-static/docs/new_page.md
   ```

2. **Criar versão em português / Create Portuguese version:**
   ```bash
   # Adicionar sufixo .pt / Add .pt suffix
   touch onestep-static/docs/new_page.pt.md
   ```

3. **Atualizar navegação no mkdocs.yml / Update navigation in mkdocs.yml:**
   ```yaml
   nav_translations:
     New Page: Nova Página
   ```

### Para traduzir conteúdo existente / To translate existing content:

Use o script `translate_docs.py` como referência para traduções em massa:

Use the `translate_docs.py` script as a reference for bulk translations:

```bash
python3 translate_docs.py
```

## 📝 Convenções de Nomenclatura / Naming Conventions

- **Inglês (padrão) / English (default):** `filename.md`
- **Português / Portuguese:** `filename.pt.md`
- **Outros idiomas / Other languages:** `filename.<locale>.md`

## 🔍 Busca / Search

A funcionalidade de busca funciona em ambos os idiomas automaticamente.

Search functionality works in both languages automatically.

## 🌐 URLs

- **Inglês / English:** `/` ou `/en/`
- **Português / Portuguese:** `/pt/`

Exemplos / Examples:
- `/` → Página inicial em inglês / English homepage
- `/pt/` → Página inicial em português / Portuguese homepage
- `/research_groups/` → Grupos em inglês / Groups in English
- `/pt/research_groups/` → Grupos em português / Groups in Portuguese

## 📊 Dados / Data

Os dados JSON são compartilhados entre ambos os idiomas. Apenas o conteúdo textual e as labels dos gráficos são traduzidos.

JSON data is shared between both languages. Only textual content and chart labels are translated.

## 🐛 Solução de Problemas / Troubleshooting

### Problema: Idioma não aparece / Issue: Language not showing

**Solução / Solution:**
1. Verificar se o arquivo `.pt.md` existe / Check if `.pt.md` file exists
2. Limpar cache do build / Clear build cache:
   ```bash
   mkdocs build --clean
   ```

### Problema: Traduções não aplicadas / Issue: Translations not applied

**Solução / Solution:**
1. Verificar configuração no `mkdocs.yml` / Check configuration in `mkdocs.yml`
2. Reinstalar plugin / Reinstall plugin:
   ```bash
   pip install --upgrade mkdocs-static-i18n
   ```

## 📚 Recursos / Resources

- [mkdocs-static-i18n Documentation](https://github.com/ultrabug/mkdocs-static-i18n)
- [MkDocs Documentation](https://www.mkdocs.org/)

---

**Última Atualização / Last Updated:** Novembro 2025  
**Versão / Version:** 1.0.0
