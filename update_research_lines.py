#!/usr/bin/env python3
"""
Script to update research_lines.json with publication data from papers.json
"""
import json
from collections import defaultdict
from datetime import datetime

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file with proper formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def normalize_name(name):
    """Normalize researcher name for matching"""
    return name.lower().strip()

def main():
    # Load data
    print("Loading papers.json...")
    papers_data = load_json('data/papers.json')
    
    print("Loading research_lines.json...")
    research_lines_data = load_json('data/research_lines.json')
    
    # Create a mapping of researcher names to their paper data
    researcher_papers = {}
    for researcher_info in papers_data['researchers']:
        researcher = researcher_info['researcher']
        name = researcher['name']
        researcher_papers[normalize_name(name)] = {
            'name': name,
            'scholar_id': researcher.get('scholar_id'),
            'scholar_url': researcher.get('scholar_url'),
            'interests': researcher.get('interests', []),
            'statistics': researcher_info['statistics'],
            'top_papers': researcher_info.get('top_5_papers', []),
            'all_papers': researcher_info.get('all_papers', [])
        }
    
    print(f"Found {len(researcher_papers)} researchers in papers.json")
    
    # Update each research line with publication data
    for research_line in research_lines_data['research_lines']:
        line_name = research_line['name']
        print(f"\nProcessing research line: {line_name}")
        
        # Initialize publication statistics for this research line
        line_stats = {
            'total_papers': 0,
            'total_citations': 0,
            'h_index_max': 0,
            'researchers_with_publications': []
        }
        
        # Check each supervisor in this research line
        supervisors = research_line.get('supervisors', [])
        
        for supervisor in supervisors:
            normalized_supervisor = normalize_name(supervisor)
            
            # Find matching researcher in papers data
            if normalized_supervisor in researcher_papers:
                paper_info = researcher_papers[normalized_supervisor]
                stats = paper_info['statistics']
                
                line_stats['total_papers'] += stats.get('total_papers', 0)
                line_stats['total_citations'] += stats.get('total_citations', 0)
                
                h_index_all = int(stats.get('h_index', {}).get('all_time', 0))
                if h_index_all > line_stats['h_index_max']:
                    line_stats['h_index_max'] = h_index_all
                
                line_stats['researchers_with_publications'].append({
                    'name': paper_info['name'],
                    'scholar_id': paper_info['scholar_id'],
                    'scholar_url': paper_info['scholar_url'],
                    'interests': paper_info['interests'],
                    'total_papers': stats.get('total_papers', 0),
                    'total_citations': stats.get('total_citations', 0),
                    'h_index': stats.get('h_index', {}),
                    'i10_index': stats.get('i10_index', {}),
                    'top_5_papers': paper_info['top_papers'][:5]
                })
                
                print(f"  - Matched: {supervisor} ({stats.get('total_papers', 0)} papers, {stats.get('total_citations', 0)} citations)")
        
        # Add publication statistics to research line
        if line_stats['researchers_with_publications']:
            research_line['publication_statistics'] = {
                'total_papers': line_stats['total_papers'],
                'total_citations': line_stats['total_citations'],
                'h_index_max': line_stats['h_index_max'],
                'average_papers_per_researcher': round(line_stats['total_papers'] / len(line_stats['researchers_with_publications']), 2),
                'average_citations_per_researcher': round(line_stats['total_citations'] / len(line_stats['researchers_with_publications']), 2),
                'researchers_count': len(line_stats['researchers_with_publications'])
            }
            research_line['researchers_publications'] = line_stats['researchers_with_publications']
            
            print(f"  Total: {line_stats['total_papers']} papers, {line_stats['total_citations']} citations")
        else:
            print(f"  No researchers with publications found")
    
    # Update metadata
    research_lines_data['metadata']['last_updated'] = datetime.now().isoformat()
    research_lines_data['metadata']['papers_data_generated_at'] = papers_data.get('generated_at')
    
    # Save updated data
    print("\nSaving updated research_lines.json...")
    save_json('data/research_lines.json', research_lines_data)
    
    print("\n✓ Research lines updated successfully!")
    
    # Print summary
    lines_with_pubs = sum(1 for line in research_lines_data['research_lines'] 
                          if 'publication_statistics' in line)
    print(f"\nSummary:")
    print(f"  - Total research lines: {len(research_lines_data['research_lines'])}")
    print(f"  - Research lines with publications: {lines_with_pubs}")

if __name__ == '__main__':
    main()
