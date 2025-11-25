#!/usr/bin/env python3
"""
Script para adicionar supervisores do CSV ao scholar_ids.json
"""
import json
import csv

def merge_supervisors():
    """Adiciona supervisores do CSV ao scholar_ids.json"""
    
    # Ler arquivo JSON existente
    with open('data/scholar_ids.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Criar set com nomes já existentes (normalizado para comparação)
    existing_names = {r['name'].lower() for r in data['researchers']}
    
    # Ler CSV de supervisores
    supervisors = []
    with open('supervisors_serra.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Nome']
            # Adicionar apenas se não existir
            if name.lower() not in existing_names:
                supervisors.append({
                    "name": name,
                    "scholar_id": "",  # Vazio, pois não temos o ID
                    "campus": "Serra"
                })
    
    # Adicionar novos supervisores
    data['researchers'].extend(supervisors)
    
    # Ordenar por nome
    data['researchers'].sort(key=lambda x: x['name'])
    
    # Salvar arquivo atualizado
    with open('data/scholar_ids.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Arquivo atualizado: data/scholar_ids.json")
    print(f"\nEstatísticas:")
    print(f"  - Total de pesquisadores: {len(data['researchers'])}")
    print(f"  - Novos adicionados: {len(supervisors)}")
    print(f"  - Com Scholar ID: {sum(1 for r in data['researchers'] if r['scholar_id'])}")
    print(f"  - Sem Scholar ID: {sum(1 for r in data['researchers'] if not r['scholar_id'])}")
    
    if supervisors:
        print(f"\nPrimeiros 10 supervisores adicionados:")
        for i, sup in enumerate(supervisors[:10], 1):
            print(f"  {i}. {sup['name']}")

if __name__ == '__main__':
    merge_supervisors()
