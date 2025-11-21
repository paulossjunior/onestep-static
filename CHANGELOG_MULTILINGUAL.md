# Changelog - Suporte Multilíngue / Multilingual Support

## [1.1.0] - 2025-11-21

### ✨ Adicionado / Added

#### Suporte Multilíngue / Multilingual Support
- ✅ Configurado suporte para **Inglês (English)** e **Português Brasileiro (Portuguese - Brazil)**
- ✅ Plugin `mkdocs-static-i18n` adicionado ao `requirements.txt`
- ✅ Configuração multilíngue no `mkdocs.yml`

#### Novos Arquivos / New Files
- ✅ `onestep-static/docs/index.pt.md` - Página inicial em português
- ✅ `onestep-static/docs/research_groups.pt.md` - Grupos de pesquisa em português
- ✅ `onestep-static/docs/research_projects.pt.md` - Projetos de pesquisa em português
- ✅ `translate_docs.py` - Script para tradução automatizada de termos
- ✅ `MULTILINGUAL_SETUP.md` - Documentação sobre configuração multilíngue
- ✅ `CHANGELOG_MULTILINGUAL.md` - Este arquivo

#### Traduções / Translations
- ✅ Todos os títulos de seções traduzidos
- ✅ Labels de gráficos traduzidos (Plotly)
- ✅ Cabeçalhos de tabelas traduzidos
- ✅ Descrições e textos explicativos traduzidos
- ✅ Legendas de redes de colaboração traduzidas
- ✅ Estatísticas e métricas traduzidas

### 🔧 Modificado / Modified

#### Arquivos Atualizados / Updated Files
- ✅ `requirements.txt` - Adicionado `mkdocs-static-i18n==1.2.3`
- ✅ `onestep-static/mkdocs.yml` - Configuração do plugin i18n
- ✅ `README.md` - Documentação atualizada com informações sobre multilíngue

### 📊 Estatísticas / Statistics

- **Idiomas Suportados / Supported Languages:** 2 (English, Português)
- **Páginas Traduzidas / Translated Pages:** 3 (index, research_groups, research_projects)
- **Termos Traduzidos / Translated Terms:** 100+
- **Gráficos com Labels Traduzidos / Charts with Translated Labels:** 10+

### 🌐 Funcionalidades / Features

#### Seletor de Idioma / Language Selector
- Aparece automaticamente na barra de navegação
- Appears automatically in the navigation bar
- Permite alternar entre inglês e português
- Allows switching between English and Portuguese

#### URLs Localizadas / Localized URLs
- `/` - Inglês (padrão) / English (default)
- `/pt/` - Português / Portuguese
- `/research_groups/` - Grupos em inglês / Groups in English
- `/pt/research_groups/` - Grupos em português / Groups in Portuguese

#### Busca Multilíngue / Multilingual Search
- Busca funciona em ambos os idiomas
- Search works in both languages
- Resultados contextualizados por idioma
- Results contextualized by language

### 🎯 Elementos Traduzidos / Translated Elements

#### Gráficos / Charts
- ✅ Títulos de gráficos / Chart titles
- ✅ Eixos X e Y / X and Y axes
- ✅ Legendas / Legends
- ✅ Tooltips / Tooltips
- ✅ Labels de dados / Data labels

#### Tabelas / Tables
- ✅ Cabeçalhos de colunas / Column headers
- ✅ Títulos de seções / Section titles
- ✅ Rodapés / Footers

#### Redes de Colaboração / Collaboration Networks
- ✅ Títulos / Titles
- ✅ Legendas / Legends
- ✅ Instruções de uso / Usage instructions
- ✅ Estatísticas de rede / Network statistics
- ✅ Insights / Insights

#### Conteúdo Textual / Textual Content
- ✅ Descrições de seções / Section descriptions
- ✅ Instruções / Instructions
- ✅ Notas explicativas / Explanatory notes
- ✅ Mensagens de status / Status messages

### 🔄 Processo de Tradução / Translation Process

1. **Arquivos Base / Base Files**
   - Arquivos `.md` originais mantidos em inglês
   - Original `.md` files kept in English

2. **Arquivos Traduzidos / Translated Files**
   - Criados com sufixo `.pt.md`
   - Created with `.pt.md` suffix

3. **Script de Tradução / Translation Script**
   - `translate_docs.py` automatiza traduções de termos comuns
   - `translate_docs.py` automates common term translations

4. **Dados Compartilhados / Shared Data**
   - Arquivos JSON compartilhados entre idiomas
   - JSON files shared between languages
   - Apenas labels e textos são traduzidos
   - Only labels and texts are translated

### 📝 Convenções / Conventions

#### Nomenclatura de Arquivos / File Naming
```
filename.md       → Inglês / English
filename.pt.md    → Português / Portuguese
```

#### Estrutura de Navegação / Navigation Structure
```yaml
nav_translations:
  English Term: Termo em Português
```

### 🚀 Deploy

- ✅ GitHub Actions configurado para build multilíngue
- ✅ GitHub Actions configured for multilingual build
- ✅ Ambos os idiomas publicados automaticamente
- ✅ Both languages published automatically
- ✅ Sem necessidade de configuração adicional
- ✅ No additional configuration needed

### 📚 Documentação / Documentation

#### Novos Guias / New Guides
- ✅ `MULTILINGUAL_SETUP.md` - Guia completo de configuração
- ✅ `MULTILINGUAL_SETUP.md` - Complete setup guide
- ✅ Instruções em português e inglês
- ✅ Instructions in Portuguese and English

#### README Atualizado / Updated README
- ✅ Seção sobre suporte multilíngue
- ✅ Section about multilingual support
- ✅ Estrutura de arquivos atualizada
- ✅ Updated file structure
- ✅ Comandos de build atualizados
- ✅ Updated build commands

### 🎨 Interface do Usuário / User Interface

#### Melhorias / Improvements
- ✅ Seletor de idioma visível
- ✅ Visible language selector
- ✅ Navegação consistente entre idiomas
- ✅ Consistent navigation between languages
- ✅ URLs amigáveis
- ✅ Friendly URLs

### 🔍 SEO e Acessibilidade / SEO and Accessibility

- ✅ Tags `lang` apropriadas em cada página
- ✅ Appropriate `lang` tags on each page
- ✅ URLs localizadas para melhor indexação
- ✅ Localized URLs for better indexing
- ✅ Conteúdo acessível em ambos os idiomas
- ✅ Content accessible in both languages

### 🐛 Correções / Bug Fixes

- ✅ Encoding UTF-8 garantido em todos os arquivos
- ✅ UTF-8 encoding ensured in all files
- ✅ Caracteres especiais portugueses suportados
- ✅ Portuguese special characters supported

### 📦 Dependências / Dependencies

#### Adicionadas / Added
```
mkdocs-static-i18n==1.2.3
```

#### Compatibilidade / Compatibility
- ✅ Python 3.12+
- ✅ MkDocs 1.6.1
- ✅ Todos os plugins existentes
- ✅ All existing plugins

### 🎯 Próximos Passos / Next Steps

#### Possíveis Melhorias / Possible Improvements
- [ ] Adicionar mais idiomas (Espanhol, Francês, etc.)
- [ ] Add more languages (Spanish, French, etc.)
- [ ] Traduzir mensagens de erro
- [ ] Translate error messages
- [ ] Localizar formatos de data
- [ ] Localize date formats
- [ ] Adicionar glossário de termos técnicos
- [ ] Add technical terms glossary

### 📞 Suporte / Support

Para questões sobre o suporte multilíngue:
For questions about multilingual support:

1. Consulte `MULTILINGUAL_SETUP.md`
2. Verifique a documentação do plugin: https://github.com/ultrabug/mkdocs-static-i18n
3. Entre em contato com a equipe de desenvolvimento

---

**Versão / Version:** 1.1.0  
**Data / Date:** 21 de Novembro de 2025 / November 21, 2025  
**Autor / Author:** IFES Campus Serra Research Team
