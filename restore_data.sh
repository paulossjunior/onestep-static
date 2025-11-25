#!/bin/bash

# Script para restaurar dados originais do backup

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         RESTAURAÇÃO DE DADOS - IFES Research Data          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se backup existe
if [ ! -d "data_backup" ]; then
    echo "❌ Erro: Diretório data_backup/ não encontrado!"
    echo ""
    echo "   O backup não existe. Não é possível restaurar os dados."
    exit 1
fi

# Contar arquivos no backup
BACKUP_COUNT=$(ls -1 data_backup/*.json 2>/dev/null | wc -l)

if [ "$BACKUP_COUNT" -eq 0 ]; then
    echo "❌ Erro: Nenhum arquivo de backup encontrado em data_backup/"
    exit 1
fi

echo "📦 Backup encontrado com $BACKUP_COUNT arquivos"
echo ""
echo "⚠️  ATENÇÃO: Esta operação irá:"
echo "   • Substituir dados FAKE por dados REAIS"
echo "   • Sobrescrever arquivos em data/"
echo ""
read -p "Deseja continuar? (digite 'SIM' para confirmar): " confirm

if [ "$confirm" != "SIM" ]; then
    echo ""
    echo "❌ Operação cancelada pelo usuário."
    exit 1
fi

echo ""
echo "🔄 Restaurando dados originais..."
echo ""

# Restaurar arquivos
for file in data_backup/*.json; do
    filename=$(basename "$file")
    cp "$file" "data/$filename"
    echo "✓ Restaurado: $filename"
done

echo ""
echo "✅ Restauração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Verificar arquivos em data/"
echo "   2. Testar build: cd onestep-static && mkdocs build"
echo ""
