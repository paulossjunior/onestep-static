#!/usr/bin/env python3
"""
Script para extrair nomes de supervisores do campus Serra
e gerar arquivo CSV
"""
import json
import csv

def extract_serra_supervisors():
    """Extrai nomes de supervisores do campus Serra"""
    
    # Ler arquivo JSON
    with open('data/supervisors.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filtrar supervisores do campus Serra
    serra_supervisors = []
    for supervisor in data['supervisors']:
        if supervisor.get('campus') == 'Serra':
            serra_supervisors.append(supervisor['name'])
    
    # Ordenar alfabeticamente
    serra_supervisors.sort()
    
    # Criar arquivo CSV
    with open('supervisors_serra.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Nome'])  # Cabeçalho
        for name in serra_supervisors:
            writer.writerow([name])
    
    print(f"✓ Arquivo criado: supervisors_serra.csv")
    print(f"✓ Total de supervisores do campus Serra: {len(serra_supervisors)}")
    print(f"\nPrimeiros 10 nomes:")
    for i, name in enumerate(serra_supervisors[:10], 1):
        print(f"  {i}. {name}")

if __name__ == '__main__':
    extract_serra_supervisors()
