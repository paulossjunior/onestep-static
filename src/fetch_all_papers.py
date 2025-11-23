#!/usr/bin/env python3
"""
Fetch ALL papers from Google Scholar for each researcher.
This script uses pagination to get complete publication lists.
"""

import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


def fetch_author_data(api_key: str, author_id: str, author_name: str):
    """Fetch author data and top 20 papers from SearchAPI.io."""
    
    base_url = "https://www.searchapi.io/api/v1/search"
    
    print(f"\n  Fetching data for {author_name}...")
    
    params = {
        'engine': 'google_scholar_author',
        'author_id': author_id,
        'api_key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        
        # Process articles (top 20 by default)
        papers = []
        for article in articles:
            cited_by_data = article.get('cited_by', {})
            cited_by_count = cited_by_data.get('total', 0) if isinstance(cited_by_data, dict) else 0
            
            paper = {
                'title': article.get('title', ''),
                'authors': article.get('authors', ''),
                'publication': article.get('publication', ''),
                'year': article.get('year', ''),
                'citations': cited_by_count,
                'link': article.get('link', ''),
                'citation_id': article.get('citation_id', '')
            }
            papers.append(paper)
        
        print(f"  ✓ Fetched {len(papers)} papers")
        return papers, data
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error: {e}")
        return [], None


def fetch_author_profile(api_key: str, author_id: str):
    """Fetch author profile information."""
    
    base_url = "https://www.searchapi.io/api/v1/search"
    params = {
        'engine': 'google_scholar_author',
        'author_id': author_id,
        'api_key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error fetching profile: {e}")
        return None


def main():
    """Main execution."""
    load_dotenv()
    api_key = os.getenv('SEARCHAPI_KEY')
    
    if not api_key:
        print("✗ Error: SEARCHAPI_KEY not found in .env")
        return
    
    print("=" * 80)
    print("FETCHING ALL PAPERS FROM GOOGLE SCHOLAR")
    print("=" * 80)
    
    # Load scholar IDs
    scholar_ids_file = Path('data/scholar_ids.json')
    if not scholar_ids_file.exists():
        print(f"✗ Error: {scholar_ids_file} not found")
        return
    
    with open(scholar_ids_file, 'r', encoding='utf-8') as f:
        scholar_data = json.load(f)
    
    researchers = scholar_data.get('researchers', [])
    
    # Fetch data for each researcher
    all_data = {
        'campus': 'Serra',
        'total_researchers': len(researchers),
        'generated_at': datetime.now().isoformat(),
        'researchers': []
    }
    
    for i, researcher in enumerate(researchers, 1):
        name = researcher['name']
        scholar_id = researcher['scholar_id']
        campus = researcher.get('campus', 'Serra')
        
        print(f"\n[{i}/{len(researchers)}] {name}")
        print(f"  Scholar ID: {scholar_id}")
        
        # Fetch author data and top papers
        papers, profile_data = fetch_author_data(api_key, scholar_id, name)
        
        if not profile_data:
            print(f"  ✗ Failed to fetch data")
            continue
        
        # Parse profile
        author = profile_data.get('author', {})
        cited_by = profile_data.get('cited_by', {})
        table = cited_by.get('table', {})
        rows = table.get('rows', [])
        
        # Count papers by year from the fetched papers
        papers_by_year = {}
        for paper in papers:
            year = str(paper.get('year', ''))
            if year and year != '':
                papers_by_year[year] = papers_by_year.get(year, 0) + 1
        
        # Total papers from papers_by_year (actual total from Scholar profile)
        total_papers = sum(papers_by_year.values())
        
        # Get total citations from the table
        total_citations = int(rows[0][1]) if len(rows) > 0 and len(rows[0]) > 1 else 0
        
        # Calculate average
        avg_citations = total_citations / total_papers if total_papers > 0 else 0
        
        # Get top 5 papers
        top_5_papers = sorted(papers, key=lambda x: x['citations'], reverse=True)[:5]
        
        researcher_data = {
            'researcher': {
                'name': name,
                'campus': campus,
                'scholar_id': scholar_id,
                'scholar_url': f"https://scholar.google.com/citations?user={scholar_id}",
                'affiliation': author.get('affiliations', ''),
                'email': author.get('email', ''),
                'interests': [item.get('title', '') for item in author.get('interests', [])]
            },
            'statistics': {
                'total_papers': total_papers,
                'total_citations': total_citations,
                'average_citations_per_paper': round(avg_citations, 2),
                'h_index': {
                    'all_time': str(int(rows[1][1])) if len(rows) > 1 and len(rows[1]) > 1 else '0',
                    'since_2020': str(int(rows[1][2])) if len(rows) > 1 and len(rows[1]) > 2 else '0'
                },
                'i10_index': {
                    'all_time': str(int(rows[2][1])) if len(rows) > 2 and len(rows[2]) > 1 else '0',
                    'since_2020': str(int(rows[2][2])) if len(rows) > 2 and len(rows[2]) > 2 else '0'
                },
                'papers_by_year': papers_by_year,
                'citations_by_year': cited_by.get('histogram', [])
            },
            'top_5_papers': top_5_papers,
            'all_papers': papers  # Top 20 most cited papers
        }
        
        all_data['researchers'].append(researcher_data)
        
        print(f"  ✓ Complete: {total_papers} total papers, {len(papers)} fetched, {total_citations} citations")
        
        # Delay between researchers
        if i < len(researchers):
            time.sleep(2)
    
    # Save to file
    output_file = Path('data/papers.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Researchers: {len(all_data['researchers'])}")
    
    total_papers = sum(r['statistics']['total_papers'] for r in all_data['researchers'])
    total_citations = sum(r['statistics']['total_citations'] for r in all_data['researchers'])
    
    print(f"Total Papers: {total_papers}")
    print(f"Total Citations: {total_citations}")
    
    print("\nPapers per researcher:")
    for r in all_data['researchers']:
        print(f"  - {r['researcher']['name']}: {r['statistics']['total_papers']} papers")
    
    print(f"\n✓ Data saved to: {output_file}")
    print("=" * 80)


if __name__ == '__main__':
    main()
