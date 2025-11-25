#!/bin/bash

# Script para anonimizar dados com confirmação

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         ANONIMIZAÇÃO DE DADOS - IFES Research Data         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  ATENÇÃO: Este script irá substituir dados REAIS por dados FAKE!"
echo ""
echo "Arquivos que serão modificados:"
echo "  • data/network_stats.json"
echo "  • data/papers.json"
echo "  • data/partnership_analysis.json"
echo "  • data/research_group.json"
echo "  • data/research_lines.json"
echo "  • data/research_projects.json"
echo "  • data/scholar_ids.json"
echo "  • data/scholarships.json"
echo "  • data/students.json"
echo "  • data/supervisors.json"
echo ""
echo "✓ Um backup será criado em: data_backup/"
echo ""
read -p "Deseja continuar? (digite 'SIM' para confirmar): " confirm

if [ "$confirm" != "SIM" ]; then
    echo ""
    echo "❌ Operação cancelada pelo usuário."
    exit 1
fi

echo ""
echo "🔄 Iniciando anonimização..."
echo ""

# Executar script Python
python3 generate_fake_data.py

echo ""
echo "✅ Anonimização concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Verificar arquivos em data/"
echo "   2. Testar build: cd onestep-static && mkdocs build"
echo "   3. Para restaurar: bash restore_data.sh"
echo ""
