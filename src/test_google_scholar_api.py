#!/usr/bin/env python3
"""
Google Scholar API Test Script

This script tests the SearchAPI.io integration to fetch Google Scholar data
for researchers at Campus Serra. It retrieves publication metrics, citations,
h-index, and other academic indicators.

Classes:
    GoogleScholarClient: Client for SearchAPI.io Google Scholar API
    ScholarDataParser: Parses and structures Scholar data
    ScholarDataTester: Tests API with sample researcher

Usage:
    python src/test_google_scholar_api.py
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


class GoogleScholarClient:
    """
    Client for SearchAPI.io Google Scholar API.
    
    This class handles API requests to fetch researcher profiles,
    publications, and citation metrics from Google Scholar.
    """
    
    BASE_URL = "https://www.searchapi.io/api/v1/search"
    
    def __init__(self, api_key: str):
        """
        Initialize the Google Scholar API client.
        
        Args:
            api_key: SearchAPI.io API key
        """
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_author_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch author profile from Google Scholar.
        
        Args:
            user_id: Google Scholar user ID (e.g., 'cFAEK0wAAAAJ')
            
        Returns:
            Dictionary with author profile data or None if error
        """
        params = {
            'engine': 'google_scholar_author',
            'author_id': user_id,
            'api_key': self.api_key
        }
        
        try:
            print(f"Fetching profile for user: {user_id}")
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Profile fetched successfully")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching profile: {e}")
            return None
    
    def get_author_citations(
        self, 
        user_id: str, 
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch author citations data.
        
        Args:
            user_id: Google Scholar user ID
            start_year: Start year for citation data
            end_year: End year for citation data
            
        Returns:
            Dictionary with citation data or None if error
        """
        params = {
            'engine': 'google_scholar_author',
            'author_id': user_id,
            'api_key': self.api_key
        }
        
        if start_year:
            params['start_year'] = start_year
        if end_year:
            params['end_year'] = end_year
        
        try:
            print(f"Fetching citations for user: {user_id}")
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Citations fetched successfully")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching citations: {e}")
            return None


class ScholarDataParser:
    """
    Parses and structures Google Scholar data.
    
    This class extracts relevant information from API responses
    and formats it for storage and analysis.
    """
    
    @staticmethod
    def parse_profile(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse author profile data.
        
        Args:
            data: Raw API response data
            
        Returns:
            Structured profile dictionary
        """
        author = data.get('author', {})
        cited_by = data.get('cited_by', {})
        
        profile = {
            'name': author.get('name', ''),
            'affiliations': author.get('affiliations', ''),
            'email': author.get('email', ''),
            'website': author.get('website', ''),
            'interests': author.get('interests', []),
            'thumbnail': author.get('thumbnail', ''),
            'metrics': {
                'citations_all': cited_by.get('table', [{}])[0].get('citations', {}).get('all', 0) if cited_by.get('table') else 0,
                'citations_since_2019': cited_by.get('table', [{}])[0].get('citations', {}).get('since_2019', 0) if cited_by.get('table') else 0,
                'h_index_all': cited_by.get('table', [{}])[1].get('h_index', {}).get('all', 0) if len(cited_by.get('table', [])) > 1 else 0,
                'h_index_since_2019': cited_by.get('table', [{}])[1].get('h_index', {}).get('since_2019', 0) if len(cited_by.get('table', [])) > 1 else 0,
                'i10_index_all': cited_by.get('table', [{}])[2].get('i10_index', {}).get('all', 0) if len(cited_by.get('table', [])) > 2 else 0,
                'i10_index_since_2019': cited_by.get('table', [{}])[2].get('i10_index', {}).get('since_2019', 0) if len(cited_by.get('table', [])) > 2 else 0,
            },
            'citations_by_year': cited_by.get('graph', []),
            'co_authors': data.get('co_authors', [])
        }
        
        return profile
    
    @staticmethod
    def parse_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse articles data.
        
        Args:
            data: Raw API response data
            
        Returns:
            List of article dictionaries
        """
        articles = []
        
        for article in data.get('articles', []):
            articles.append({
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'citation_id': article.get('citation_id', ''),
                'authors': article.get('authors', ''),
                'publication': article.get('publication', ''),
                'cited_by': article.get('cited_by', {}).get('value', 0),
                'year': article.get('year', '')
            })
        
        return articles
    
    @staticmethod
    def calculate_statistics(profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate additional statistics from profile data.
        
        Args:
            profile: Parsed profile dictionary
            
        Returns:
            Dictionary with calculated statistics
        """
        citations_by_year = profile.get('citations_by_year', [])
        
        if not citations_by_year:
            return {
                'total_years': 0,
                'avg_citations_per_year': 0,
                'peak_year': None,
                'peak_citations': 0,
                'recent_trend': 'N/A'
            }
        
        years = [int(item['year']) for item in citations_by_year if 'year' in item]
        citations = [int(item['citations']) for item in citations_by_year if 'citations' in item]
        
        total_years = len(years)
        avg_citations = sum(citations) / total_years if total_years > 0 else 0
        
        peak_index = citations.index(max(citations)) if citations else 0
        peak_year = years[peak_index] if years else None
        peak_citations = max(citations) if citations else 0
        
        # Calculate recent trend (last 3 years)
        if len(citations) >= 3:
            recent_avg = sum(citations[-3:]) / 3
            older_avg = sum(citations[:-3]) / len(citations[:-3]) if len(citations) > 3 else 0
            
            if older_avg > 0:
                trend_pct = ((recent_avg - older_avg) / older_avg) * 100
                if trend_pct > 10:
                    recent_trend = 'Growing'
                elif trend_pct < -10:
                    recent_trend = 'Declining'
                else:
                    recent_trend = 'Stable'
            else:
                recent_trend = 'Growing'
        else:
            recent_trend = 'Insufficient data'
        
        return {
            'total_years': total_years,
            'avg_citations_per_year': round(avg_citations, 2),
            'peak_year': peak_year,
            'peak_citations': peak_citations,
            'recent_trend': recent_trend
        }


class ScholarDataTester:
    """
    Tests Google Scholar API integration.
    
    This class runs tests with sample researchers and displays results.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize tester with API key.
        
        Args:
            api_key: SearchAPI.io API key
        """
        self.client = GoogleScholarClient(api_key)
        self.parser = ScholarDataParser()
    
    def test_researcher(self, user_id: str, name: str) -> None:
        """
        Test API with a specific researcher.
        
        Args:
            user_id: Google Scholar user ID
            name: Researcher name for display
        """
        print("\n" + "=" * 80)
        print(f"TESTING GOOGLE SCHOLAR API - {name}")
        print("=" * 80)
        
        # Fetch profile
        raw_data = self.client.get_author_profile(user_id)
        
        if not raw_data:
            print("✗ Failed to fetch data")
            return
        
        # Parse profile
        profile = self.parser.parse_profile(raw_data)
        
        # Calculate statistics
        stats = self.parser.calculate_statistics(profile)
        
        # Parse articles
        articles = self.parser.parse_articles(raw_data)
        
        # Display results
        self._display_results(profile, stats, articles)
        
        # Save to file
        self._save_results(user_id, name, profile, stats, articles, raw_data)
    
    def _display_results(
        self, 
        profile: Dict[str, Any], 
        stats: Dict[str, Any],
        articles: List[Dict[str, Any]]
    ) -> None:
        """
        Display formatted results.
        
        Args:
            profile: Parsed profile data
            stats: Calculated statistics
            articles: List of articles
        """
        print("\n" + "-" * 80)
        print("PROFILE INFORMATION")
        print("-" * 80)
        print(f"Name: {profile['name']}")
        print(f"Affiliation: {profile['affiliations']}")
        print(f"Email: {profile['email']}")
        print(f"Website: {profile['website']}")
        print(f"Interests: {', '.join(profile['interests'])}")
        
        print("\n" + "-" * 80)
        print("CITATION METRICS")
        print("-" * 80)
        metrics = profile['metrics']
        print(f"Total Citations: {metrics['citations_all']}")
        print(f"Citations (since 2019): {metrics['citations_since_2019']}")
        print(f"h-index: {metrics['h_index_all']}")
        print(f"h-index (since 2019): {metrics['h_index_since_2019']}")
        print(f"i10-index: {metrics['i10_index_all']}")
        print(f"i10-index (since 2019): {metrics['i10_index_since_2019']}")
        
        print("\n" + "-" * 80)
        print("STATISTICS")
        print("-" * 80)
        print(f"Years Active: {stats['total_years']}")
        print(f"Avg Citations/Year: {stats['avg_citations_per_year']}")
        print(f"Peak Year: {stats['peak_year']} ({stats['peak_citations']} citations)")
        print(f"Recent Trend: {stats['recent_trend']}")
        
        print("\n" + "-" * 80)
        print("CITATIONS BY YEAR")
        print("-" * 80)
        for item in profile['citations_by_year']:
            year = item.get('year', 'N/A')
            citations = item.get('citations', 0)
            print(f"  {year}: {citations} citations")
        
        print("\n" + "-" * 80)
        print(f"TOP 10 PUBLICATIONS (Total: {len(articles)})")
        print("-" * 80)
        for i, article in enumerate(articles[:10], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Authors: {article['authors']}")
            print(f"   Publication: {article['publication']}")
            print(f"   Year: {article['year']}")
            print(f"   Cited by: {article['cited_by']}")
        
        print("\n" + "-" * 80)
        print(f"CO-AUTHORS (Total: {len(profile['co_authors'])})")
        print("-" * 80)
        for i, coauthor in enumerate(profile['co_authors'][:10], 1):
            print(f"{i}. {coauthor.get('name', 'N/A')} - {coauthor.get('affiliations', 'N/A')}")
    
    def _save_results(
        self,
        user_id: str,
        name: str,
        profile: Dict[str, Any],
        stats: Dict[str, Any],
        articles: List[Dict[str, Any]],
        raw_data: Dict[str, Any]
    ) -> None:
        """
        Save results to JSON file.
        
        Args:
            user_id: Google Scholar user ID
            name: Researcher name
            profile: Parsed profile data
            stats: Calculated statistics
            articles: List of articles
            raw_data: Raw API response
        """
        output_dir = Path('data/scholar_test')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save parsed data
        parsed_file = output_dir / f'{user_id}_parsed.json'
        parsed_data = {
            'metadata': {
                'user_id': user_id,
                'name': name,
                'fetched_at': datetime.now().isoformat(),
                'source': 'SearchAPI.io - Google Scholar'
            },
            'profile': profile,
            'statistics': stats,
            'articles': articles
        }
        
        with open(parsed_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Parsed data saved to: {parsed_file}")
        
        # Save raw data
        raw_file = output_dir / f'{user_id}_raw.json'
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Raw data saved to: {raw_file}")


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('SEARCHAPI_KEY')
    
    if not api_key:
        print("✗ Error: SEARCHAPI_KEY not found in .env file")
        return
    
    print("=" * 80)
    print("GOOGLE SCHOLAR API TEST - SearchAPI.io")
    print("=" * 80)
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    
    # Initialize tester
    tester = ScholarDataTester(api_key)
    
    # Test with Paulo Sergio dos Santos Junior
    tester.test_researcher(
        user_id='cFAEK0wAAAAJ',
        name='Paulo Sergio dos Santos Junior'
    )
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
