#!/usr/bin/env python3
"""
Script para extrair informações completas de supervisores do campus Serra
e gerar arquivo CSV com nome e email
"""
import json
import csv

def extract_serra_supervisors_full():
    """Extrai informações completas de supervisores do campus Serra"""
    
    # Ler arquivo JSON
    with open('data/supervisors.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filtrar supervisores do campus Serra
    serra_supervisors = []
    for supervisor in data['supervisors']:
        if supervisor.get('campus') == 'Serra':
            serra_supervisors.append({
                'nome': supervisor['name'],
                'email': supervisor.get('email', ''),
                'total_projetos': supervisor['statistics'].get('total_projects', 0),
                'total_orientacoes': supervisor['statistics'].get('total_supervisions', 0)
            })
    
    # Ordenar alfabeticamente por nome
    serra_supervisors.sort(key=lambda x: x['nome'])
    
    # Criar arquivo CSV
    with open('supervisors_serra_full.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nome', 'email', 'total_projetos', 'total_orientacoes'])
        writer.writeheader()
        writer.writerows(serra_supervisors)
    
    print(f"✓ Arquivo criado: supervisors_serra_full.csv")
    print(f"✓ Total de supervisores do campus Serra: {len(serra_supervisors)}")
    
    # Estatísticas
    with_email = sum(1 for s in serra_supervisors if s['email'])
    with_projects = sum(1 for s in serra_supervisors if s['total_projetos'] > 0)
    with_supervisions = sum(1 for s in serra_supervisors if s['total_orientacoes'] > 0)
    
    print(f"\nEstatísticas:")
    print(f"  - Com email: {with_email}")
    print(f"  - Com projetos: {with_projects}")
    print(f"  - Com orientações: {with_supervisions}")
    
    print(f"\nPrimeiros 5 registros:")
    for i, sup in enumerate(serra_supervisors[:5], 1):
        print(f"  {i}. {sup['nome']}")
        print(f"     Email: {sup['email'] or 'N/A'}")
        print(f"     Projetos: {sup['total_projetos']}, Orientações: {sup['total_orientacoes']}")

if __name__ == '__main__':
    extract_serra_supervisors_full()
