# 🇧🇷 Guia Rápido - Documentação Multilíngue

## 🎯 O que foi feito?

Seu portal de documentação de pesquisa agora está disponível em **dois idiomas**:
- 🇺🇸 **Inglês** (English)
- 🇧🇷 **Português Brasileiro** (Portuguese - Brazil)

## 🚀 Como usar?

### 1. Visualizar localmente

```bash
# Instalar dependências (apenas uma vez)
pip install -r requirements.txt

# Iniciar o servidor
cd onestep-static
mkdocs serve

# Abrir no navegador
# http://127.0.0.1:8001
```

### 2. Trocar de idioma

Quando o site estiver rodando, você verá um **seletor de idioma no canto superior direito** da página:

```
🌐 🇺🇸 EN 🇧🇷 PT
```

Clique no idioma desejado para alternar entre inglês e português. A página recarregará automaticamente no idioma escolhido.

### 3. Build para produção

```bash
cd onestep-static
mkdocs build --clean --strict
```

O site será gerado na pasta `site/` com ambos os idiomas.

## 📁 Estrutura dos arquivos

```
onestep-static/docs/
├── index.md                    # Página inicial (inglês)
├── index.pt.md                 # Página inicial (português)
├── research_groups.md          # Grupos (inglês)
├── research_groups.pt.md       # Grupos (português)
├── research_projects.md        # Projetos (inglês)
└── research_projects.pt.md     # Projetos (português)
```

## ✏️ Como adicionar/editar traduções?

### Opção 1: Editar manualmente

1. Abra o arquivo `.pt.md` correspondente
2. Edite o texto em português
3. Salve o arquivo

### Opção 2: Usar o script de tradução

```bash
# Edite o arquivo translate_docs.py
# Adicione novos termos ao dicionário de traduções
# Execute o script
python3 translate_docs.py
```

## 🌐 URLs do site

- **Inglês:**
  - Página inicial: `/`
  - Grupos: `/research_groups/`
  - Projetos: `/research_projects/`

- **Português:**
  - Página inicial: `/pt/`
  - Grupos: `/pt/research_groups/`
  - Projetos: `/pt/research_projects/`

## 📊 O que foi traduzido?

✅ **Todos os textos principais:**
- Títulos de páginas
- Descrições de seções
- Instruções de uso

✅ **Gráficos interativos:**
- Títulos dos gráficos
- Legendas
- Eixos (X e Y)
- Labels de dados

✅ **Tabelas:**
- Cabeçalhos de colunas
- Títulos de seções

✅ **Redes de colaboração:**
- Legendas
- Estatísticas
- Instruções

## 🔧 Configuração

A configuração está no arquivo `onestep-static/mkdocs.yml`:

```yaml
plugins:
  - i18n:
      languages:
        - locale: en
          default: true
          name: English
        - locale: pt
          name: Português (Brasil)
```

## 📝 Dicas importantes

1. **Arquivos de dados (JSON)** são compartilhados entre os idiomas
2. **Apenas o conteúdo textual** precisa ser traduzido
3. **Mantenha a mesma estrutura** nos arquivos `.md` e `.pt.md`
4. **Use UTF-8** para garantir caracteres especiais (ç, ã, õ, etc.)

## 🐛 Problemas comuns

### O idioma não aparece?
```bash
# Limpe o cache e reconstrua
mkdocs build --clean
```

### Caracteres especiais não aparecem?
- Verifique se o arquivo está salvo em UTF-8
- Verifique se não há erros de encoding

### Traduções não aplicadas?
```bash
# Reinstale o plugin
pip install --upgrade mkdocs-static-i18n
```

## 📚 Documentação completa

Para mais detalhes, consulte:
- `MULTILINGUAL_SETUP.md` - Guia completo (português e inglês)
- `CHANGELOG_MULTILINGUAL.md` - Lista de mudanças

## 🎉 Pronto!

Seu site agora está totalmente bilíngue! 🇺🇸🇧🇷

---

**Dúvidas?** Consulte a documentação ou entre em contato com a equipe de desenvolvimento.
