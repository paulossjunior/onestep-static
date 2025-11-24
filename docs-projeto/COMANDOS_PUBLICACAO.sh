#!/bin/bash
# 🚀 Script de Publicação - OneStep Static

echo "🚀 Iniciando publicação..."
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "onestep-static/mkdocs.yml" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto"
    exit 1
fi

# Verificar se workflow está correto
if ! grep -q "cd onestep-static" .github/workflows/deploy-pages.yml; then
    echo "⚠️  Aviso: Workflow pode estar desatualizado"
    echo "   Verifique se o workflow usa 'cd onestep-static'"
fi

# Adicionar todos os arquivos
echo "📦 Adicionando arquivos..."
git add .

# Verificar se há mudanças
if git diff --staged --quiet; then
    echo "ℹ️  Nenhuma mudança para commit"
else
    # Commit
    echo "💾 Fazendo commit..."
    git commit -m "feat: add multilingual support with language selector"
    
    # Push
    echo "⬆️  Enviando para GitHub..."
    git push origin main
    
    echo ""
    echo "✅ Push concluído!"
    echo ""
    echo "🎯 Próximos passos:"
    echo ""
    echo "1. Configure GitHub Pages (uma vez):"
    echo "   https://github.com/paulossjunior/onestep-static/settings/pages"
    echo "   → Source: GitHub Actions"
    echo ""
    echo "2. Configure permissões (uma vez):"
    echo "   https://github.com/paulossjunior/onestep-static/settings/actions"
    echo "   → Read and write permissions"
    echo ""
    echo "3. Acompanhe o deploy:"
    echo "   https://github.com/paulossjunior/onestep-static/actions"
    echo ""
    echo "4. Acesse o site (após 3-5 min):"
    echo "   https://paulossjunior.github.io/onestep-static/"
    echo ""
fi
