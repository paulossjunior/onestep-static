#!/usr/bin/env python3
"""
Google Scholar Data Fetcher

This module fetches Google Scholar data for all researchers at Campus Serra
and generates a comprehensive publications database.

Classes:
    GoogleScholarClient: API client for SearchAPI.io
    ScholarDataParser: Parses Scholar API responses
    ScholarDataFetcher: Fetches data for multiple researchers
    PublicationsAggregator: Aggregates all publications

Input: data/scholar_ids.json
Output: data/scholar_profiles.json, data/publications.json
"""

import os
import json
import time
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


class GoogleScholarClient:
    """Client for SearchAPI.io Google Scholar API."""
    
    BASE_URL = "https://www.searchapi.io/api/v1/search"
    
    def __init__(self, api_key: str):
        """
        Initialize client.
        
        Args:
            api_key: SearchAPI.io API key
        """
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_author_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch author profile.
        
        Args:
            user_id: Google Scholar user ID
            
        Returns:
            API response data or None
        """
        params = {
            'engine': 'google_scholar_author',
            'author_id': user_id,
            'api_key': self.api_key
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error: {e}")
            return None


class ScholarDataParser:
    """Parses Google Scholar API responses."""
    
    @staticmethod
    def parse_profile(data: Dict[str, Any], researcher_name: str) -> Dict[str, Any]:
        """
        Parse author profile.
        
        Args:
            data: Raw API response
            researcher_name: Name from our database
            
        Returns:
            Structured profile dictionary
        """
        author = data.get('author', {})
        cited_by = data.get('cited_by', {})
        
        # Parse table
        table = cited_by.get('table', {})
        rows = table.get('rows', [])
        
        metrics = {
            'citations_all': int(rows[0][1]) if len(rows) > 0 and len(rows[0]) > 1 else 0,
            'citations_since_2020': int(rows[0][2]) if len(rows) > 0 and len(rows[0]) > 2 else 0,
            'h_index_all': int(rows[1][1]) if len(rows) > 1 and len(rows[1]) > 1 else 0,
            'h_index_since_2020': int(rows[1][2]) if len(rows) > 1 and len(rows[1]) > 2 else 0,
            'i10_index_all': int(rows[2][1]) if len(rows) > 2 and len(rows[2]) > 1 else 0,
            'i10_index_since_2020': int(rows[2][2]) if len(rows) > 2 and len(rows[2]) > 2 else 0,
        }
        
        interests = [item.get('title', '') for item in author.get('interests', [])]
        
        return {
            'name': researcher_name,
            'scholar_name': author.get('name', ''),
            'affiliations': author.get('affiliations', ''),
            'email': author.get('email', ''),
            'interests': interests,
            'thumbnail': author.get('thumbnail', ''),
            'metrics': metrics,
            'citations_by_year': cited_by.get('histogram', []),
            'co_authors': [
                {
                    'name': ca.get('name', ''),
                    'affiliations': ca.get('affiliations', ''),
                    'link': ca.get('link', '')
                }
                for ca in data.get('co_authors', [])
            ]
        }
    
    @staticmethod
    def parse_articles(data: Dict[str, Any], researcher_name: str) -> List[Dict[str, Any]]:
        """
        Parse articles.
        
        Args:
            data: Raw API response
            researcher_name: Name from our database
            
        Returns:
            List of article dictionaries
        """
        articles = []
        
        for article in data.get('articles', []):
            cited_by_data = article.get('cited_by', {})
            cited_by_count = cited_by_data.get('total', 0) if isinstance(cited_by_data, dict) else 0
            
            articles.append({
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'authors': article.get('authors', ''),
                'publication': article.get('publication', ''),
                'cited_by': cited_by_count,
                'year': article.get('year', ''),
                'researcher': researcher_name
            })
        
        return articles


class ScholarDataFetcher:
    """Fetches Scholar data for multiple researchers."""
    
    def __init__(self, api_key: str, scholar_ids_file: Path):
        """
        Initialize fetcher.
        
        Args:
            api_key: SearchAPI.io API key
            scholar_ids_file: Path to scholar IDs mapping file
        """
        self.client = GoogleScholarClient(api_key)
        self.parser = ScholarDataParser()
        self.scholar_ids_file = scholar_ids_file
        self.profiles: List[Dict[str, Any]] = []
        self.all_articles: List[Dict[str, Any]] = []
    
    def load_scholar_ids(self) -> List[Dict[str, str]]:
        """
        Load researcher Scholar IDs.
        
        Returns:
            List of researcher dictionaries with Scholar IDs
        """
        with open(self.scholar_ids_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('researchers', [])
    
    def fetch_all(self, delay: float = 2.0) -> None:
        """
        Fetch data for all researchers.
        
        Args:
            delay: Delay between requests in seconds
        """
        researchers = self.load_scholar_ids()
        
        print(f"\nFetching data for {len(researchers)} researcher(s)...")
        print("-" * 80)
        
        for i, researcher in enumerate(researchers, 1):
            name = researcher['name']
            scholar_id = researcher['scholar_id']
            
            print(f"\n[{i}/{len(researchers)}] {name}")
            print(f"  Scholar ID: {scholar_id}")
            
            # Fetch profile
            raw_data = self.client.get_author_profile(scholar_id)
            
            if raw_data:
                # Parse profile
                profile = self.parser.parse_profile(raw_data, name)
                profile['scholar_id'] = scholar_id
                profile['campus'] = researcher.get('campus', 'Serra')
                
                self.profiles.append(profile)
                
                # Parse articles
                articles = self.parser.parse_articles(raw_data, name)
                self.all_articles.extend(articles)
                
                print(f"  ✓ Fetched: {profile['metrics']['citations_all']} citations, "
                      f"{len(articles)} articles")
            else:
                print(f"  ✗ Failed to fetch data")
            
            # Delay to avoid rate limiting
            if i < len(researchers):
                time.sleep(delay)
        
        print("\n" + "-" * 80)
        print(f"✓ Fetched data for {len(self.profiles)} researcher(s)")
        print(f"✓ Total articles: {len(self.all_articles)}")


class PublicationsAggregator:
    """Aggregates and exports publications data."""
    
    def __init__(self, profiles: List[Dict], articles: List[Dict]):
        """
        Initialize aggregator.
        
        Args:
            profiles: List of researcher profiles
            articles: List of all articles
        """
        self.profiles = profiles
        self.articles = articles
    
    def generate_profiles_output(self) -> Dict[str, Any]:
        """
        Generate profiles output structure.
        
        Returns:
            Dictionary with metadata and profiles
        """
        # Sort by total citations
        sorted_profiles = sorted(
            self.profiles,
            key=lambda x: x['metrics']['citations_all'],
            reverse=True
        )
        
        total_citations = sum(p['metrics']['citations_all'] for p in self.profiles)
        total_h_index = sum(p['metrics']['h_index_all'] for p in self.profiles)
        
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'campus': 'Serra',
                'total_researchers': len(self.profiles),
                'total_citations': total_citations,
                'total_h_index': total_h_index,
                'source': 'Google Scholar via SearchAPI.io'
            },
            'profiles': sorted_profiles
        }
    
    def generate_publications_output(self) -> Dict[str, Any]:
        """
        Generate publications output structure.
        
        Returns:
            Dictionary with metadata and publications
        """
        # Sort by citations
        sorted_articles = sorted(
            self.articles,
            key=lambda x: x['cited_by'],
            reverse=True
        )
        
        # Calculate statistics
        total_citations = sum(a['cited_by'] for a in self.articles)
        
        # Count by year
        by_year = {}
        for article in self.articles:
            year = article.get('year', 'Unknown')
            if year:
                by_year[str(year)] = by_year.get(str(year), 0) + 1
        
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'campus': 'Serra',
                'total_publications': len(self.articles),
                'total_citations': total_citations,
                'publications_by_year': dict(sorted(by_year.items())),
                'source': 'Google Scholar via SearchAPI.io'
            },
            'publications': sorted_articles
        }
    
    def save(self, profiles_file: Path, publications_file: Path) -> None:
        """
        Save data to files.
        
        Args:
            profiles_file: Path for profiles output
            publications_file: Path for publications output
        """
        profiles_data = self.generate_profiles_output()
        publications_data = self.generate_publications_output()
        
        # Save profiles
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Profiles saved to: {profiles_file}")
        
        # Save publications
        with open(publications_file, 'w', encoding='utf-8') as f:
            json.dump(publications_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Publications saved to: {publications_file}")
        
        # Print summary
        self._print_summary(profiles_data, publications_data)
    
    def _print_summary(self, profiles_data: Dict, publications_data: Dict) -> None:
        """Print summary statistics."""
        print("\n" + "=" * 80)
        print("SCHOLAR DATA SUMMARY")
        print("=" * 80)
        print(f"Researchers: {profiles_data['metadata']['total_researchers']}")
        print(f"Total Citations: {profiles_data['metadata']['total_citations']}")
        print(f"Total Publications: {publications_data['metadata']['total_publications']}")
        print(f"Publication Citations: {publications_data['metadata']['total_citations']}")
        
        print("\nTop 5 Researchers by Citations:")
        for i, profile in enumerate(profiles_data['profiles'][:5], 1):
            print(f"  {i}. {profile['name']}: {profile['metrics']['citations_all']} citations")
        
        print("\nTop 5 Most Cited Publications:")
        for i, pub in enumerate(publications_data['publications'][:5], 1):
            print(f"  {i}. {pub['title'][:60]}...")
            print(f"     {pub['cited_by']} citations - {pub['researcher']}")
        
        print("=" * 80)


def main():
    """Main execution function."""
    # Load environment
    load_dotenv()
    api_key = os.getenv('SEARCHAPI_KEY')
    
    if not api_key:
        print("✗ Error: SEARCHAPI_KEY not found in .env")
        return
    
    print("=" * 80)
    print("GOOGLE SCHOLAR DATA FETCHER")
    print("=" * 80)
    
    # Configuration
    scholar_ids_file = Path('data/scholar_ids.json')
    profiles_output = Path('data/scholar_profiles.json')
    publications_output = Path('data/publications.json')
    
    if not scholar_ids_file.exists():
        print(f"✗ Error: {scholar_ids_file} not found")
        return
    
    # Fetch data
    fetcher = ScholarDataFetcher(api_key, scholar_ids_file)
    fetcher.fetch_all(delay=2.0)
    
    # Aggregate and save
    aggregator = PublicationsAggregator(fetcher.profiles, fetcher.all_articles)
    aggregator.save(profiles_output, publications_output)
    
    print("\n✓ Scholar data fetch complete!")


if __name__ == '__main__':
    main()
