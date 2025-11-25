#!/usr/bin/env python3
"""
Script para analisar dados financeiros em students.json e scholarships.json
"""
import json
from collections import Counter

def analyze_financial_data():
    """Analisa dados financeiros nos arquivos"""
    
    print("=" * 70)
    print("ANÁLISE DE DADOS FINANCEIROS")
    print("=" * 70)
    print()
    
    # Analisar students.json
    print("📄 Arquivo: data/students.json")
    print("-" * 70)
    
    with open('data/students.json', 'r', encoding='utf-8') as f:
        students_data = json.load(f)
    
    values = []
    for student in students_data['students']:
        for scholarship in student.get('ic_scholarships', []):
            value = scholarship.get('value')
            if value is not None:
                values.append(value)
    
    print(f"Total de registros com valor: {len(values)}")
    print(f"Valores únicos encontrados: {sorted(set(values))}")
    print()
    
    # Contar por valor
    value_counts = Counter(values)
    print("Distribuição de valores:")
    for value, count in sorted(value_counts.items()):
        if value == 0:
            print(f"  R$ {value:>7.2f} (Voluntário): {count:>4} registros")
        else:
            print(f"  R$ {value:>7.2f} (Bolsista):   {count:>4} registros")
    
    print()
    print(f"Valor total (students.json): R$ {sum(values):,.2f}")
    print()
    
    # Analisar scholarships.json
    print("📄 Arquivo: data/scholarships.json")
    print("-" * 70)
    
    with open('data/scholarships.json', 'r', encoding='utf-8') as f:
        scholarships_data = json.load(f)
    
    total_value = scholarships_data['metadata'].get('total_value', 0)
    print(f"Total agregado (metadata): R$ {total_value:,.2f}")
    print()
    
    # Valores individuais
    values_schol = []
    for scholarship in scholarships_data['scholarships']:
        value = scholarship.get('value')
        if value is not None:
            values_schol.append(value)
    
    print(f"Total de registros com valor: {len(values_schol)}")
    print(f"Valores únicos encontrados: {sorted(set(values_schol))}")
    print()
    
    # Contar por valor
    value_counts_schol = Counter(values_schol)
    print("Distribuição de valores:")
    for value, count in sorted(value_counts_schol.items()):
        if value == 0:
            print(f"  R$ {value:>7.2f} (Voluntário): {count:>4} registros")
        else:
            print(f"  R$ {value:>7.2f} (Bolsista):   {count:>4} registros")
    
    print()
    print(f"Valor total calculado: R$ {sum(values_schol):,.2f}")
    print()
    
    # Resumo
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"✓ Dados financeiros encontrados em ambos os arquivos")
    print(f"✓ Campo 'value' presente em registros de bolsas")
    print(f"✓ Campo 'total_value' presente em metadata de scholarships.json")
    print()
    print("⚠️  ATENÇÃO: Dados financeiros identificados!")
    print()
    print("Consulte FINANCIAL_DATA_REPORT.md para mais informações e")
    print("recomendações sobre como proceder.")
    print()

if __name__ == '__main__':
    analyze_financial_data()
