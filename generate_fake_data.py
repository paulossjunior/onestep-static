#!/usr/bin/env python3
"""
Script para gerar dados fake para todos os arquivos JSON em data/
Substitui dados reais por dados fictícios mantendo a estrutura
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuração
DATA_DIR = Path("data")
BACKUP_DIR = Path("data_backup")

# Listas de dados fake
FAKE_NAMES = [
    "Ana Silva Santos", "Bruno Costa Lima", "Carlos Oliveira Souza",
    "Diana Ferreira Alves", "Eduardo Santos Rocha", "Fernanda Lima Costa",
    "Gabriel Alves Martins", "Helena Costa Ferreira", "Igor Santos Lima",
    "Julia Oliveira Costa", "Kevin Lima Santos", "Laura Ferreira Souza",
    "Marcos Costa Alves", "Natalia Santos Lima", "Otavio Ferreira Costa",
    "Patricia Lima Alves", "Rafael Costa Santos", "Sabrina Alves Lima",
    "Thiago Santos Costa", "Ursula Lima Ferreira", "Victor Costa Alves",
    "Wesley Santos Lima", "Xavier Ferreira Costa", "Yasmin Lima Santos",
    "Zoe Costa Ferreira", "Andre Lima Alves", "Beatriz Santos Costa",
    "Caio Ferreira Lima", "Daniela Costa Santos", "Elias Lima Ferreira"
]

FAKE_EMAILS = [
    "usuario{}@example.com",
    "pesquisador{}@fake.edu.br",
    "estudante{}@test.br"
]

FAKE_TITLES = [
    "Análise de Sistemas Computacionais Distribuídos",
    "Estudo sobre Algoritmos de Aprendizado de Máquina",
    "Desenvolvimento de Aplicações Web Modernas",
    "Pesquisa em Inteligência Artificial Aplicada",
    "Otimização de Processos Industriais",
    "Análise de Dados em Grande Escala",
    "Sistemas de Informação Gerenciais",
    "Redes de Computadores e Segurança",
    "Engenharia de Software Ágil",
    "Computação em Nuvem e Virtualização"
]

FAKE_INSTITUTIONS = [
    "Universidade Federal de Exemplo",
    "Instituto de Tecnologia Fictício",
    "Centro de Pesquisa Teste",
    "Faculdade de Ciências Fake"
]

FAKE_SCHOLAR_IDS = [
    "FAKE{}AAAA", "TEST{}BBBB", "DEMO{}CCCC", "SAMP{}DDDD"
]

def anonymize_name(name):
    """Substitui nome real por nome fake"""
    return random.choice(FAKE_NAMES)

def anonymize_email(email):
    """Substitui email real por email fake"""
    if not email or email == "":
        return ""
    return random.choice(FAKE_EMAILS).format(random.randint(1, 999))

def anonymize_scholar_id(scholar_id):
    """Substitui Scholar ID real por fake"""
    if not scholar_id or scholar_id == "":
        return ""
    return random.choice(FAKE_SCHOLAR_IDS).format(random.randint(100, 999))

def anonymize_title(title):
    """Substitui título real por título fake"""
    return random.choice(FAKE_TITLES)

def anonymize_value(value):
    """Mantém valores financeiros mas randomiza um pouco"""
    if value is None or value == 0:
        return value
    # Randomiza +/- 20%
    variation = random.uniform(0.8, 1.2)
    return round(value * variation, 2)

def anonymize_date(date_str):
    """Mantém formato de data mas randomiza"""
    if not date_str:
        return date_str
    try:
        # Gera data aleatória nos últimos 5 anos
        days_ago = random.randint(0, 1825)
        fake_date = datetime.now() - timedelta(days=days_ago)
        return fake_date.strftime("%d-%m-%y")
    except:
        return date_str

def anonymize_recursively(obj, depth=0):
    """Anonimiza dados recursivamente"""
    if depth > 20:  # Prevenir recursão infinita
        return obj
    
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            # Campos que devem ser anonimizados
            if key in ['name', 'student', 'advisor', 'coordinator', 'researcher']:
                new_obj[key] = anonymize_name(value) if isinstance(value, str) else value
            elif key == 'email':
                new_obj[key] = anonymize_email(value) if isinstance(value, str) else value
            elif key == 'scholar_id':
                new_obj[key] = anonymize_scholar_id(value) if isinstance(value, str) else value
            elif key == 'title':
                new_obj[key] = anonymize_title(value) if isinstance(value, str) else value
            elif key == 'affiliation':
                new_obj[key] = random.choice(FAKE_INSTITUTIONS) if isinstance(value, str) else value
            elif key == 'value' and isinstance(value, (int, float)):
                new_obj[key] = anonymize_value(value)
            elif key in ['start_date', 'end_date']:
                new_obj[key] = anonymize_date(value) if isinstance(value, str) else value
            elif key in ['generated_at', 'last_updated']:
                new_obj[key] = datetime.now().isoformat()
            else:
                new_obj[key] = anonymize_recursively(value, depth + 1)
        return new_obj
    elif isinstance(obj, list):
        return [anonymize_recursively(item, depth + 1) for item in obj]
    else:
        return obj

def backup_data():
    """Faz backup dos dados originais"""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir()
        print(f"✓ Diretório de backup criado: {BACKUP_DIR}")
    
    for json_file in DATA_DIR.glob("*.json"):
        backup_file = BACKUP_DIR / json_file.name
        if not backup_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ Backup: {json_file.name} -> {backup_file}")

def anonymize_file(file_path):
    """Anonimiza um arquivo JSON"""
    print(f"\n📄 Processando: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Anonimizar dados
        fake_data = anonymize_recursively(data)
        
        # Salvar arquivo fake
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(fake_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Dados fake gerados para {file_path.name}")
        return True
    except Exception as e:
        print(f"✗ Erro ao processar {file_path.name}: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("GERADOR DE DADOS FAKE")
    print("=" * 70)
    print()
    print("⚠️  ATENÇÃO: Este script irá substituir dados reais por dados fake!")
    print()
    
    # Fazer backup
    print("1. Fazendo backup dos dados originais...")
    backup_data()
    print()
    
    # Processar arquivos
    print("2. Gerando dados fake...")
    json_files = list(DATA_DIR.glob("*.json"))
    
    success_count = 0
    for json_file in json_files:
        if anonymize_file(json_file):
            success_count += 1
    
    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"✓ Arquivos processados: {success_count}/{len(json_files)}")
    print(f"✓ Backup salvo em: {BACKUP_DIR}/")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Dados originais salvos em data_backup/")
    print("   - Para restaurar: cp data_backup/* data/")
    print()

if __name__ == '__main__':
    main()
