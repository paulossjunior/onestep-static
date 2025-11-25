#!/usr/bin/env python3
"""
Update Scholar IDs Script

This script identifies researchers in `data/scholar_ids.json` who are missing a
Google Scholar ID, searches for them using the SearchAPI.io `google_scholar_profiles`
engine, and updates the JSON file with the found IDs.

It filters results to ensure the researcher is affiliated with "Ifes" or "Instituto Federal".
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

class ScholarIdUpdater:
    BASE_URL = "https://www.searchapi.io/api/v1/search"
    
    def __init__(self, api_key: str, data_file: Path):
        self.api_key = api_key
        self.data_file = data_file
        self.session = requests.Session()
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved updates to {self.data_file}")

    def search_author(self, name: str) -> Optional[str]:
        """
        Search for an author by name and return their Scholar ID if found
        and affiliation matches.
        """
        params = {
            'engine': 'google_scholar_profiles',
            'q': name,
            'api_key': self.api_key
        }
        
        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(self.BASE_URL, params=params, timeout=30)
                
                if response.status_code == 503:
                    print(f"  ! 503 Service Unavailable. Retrying ({attempt+1}/{retries})...")
                    time.sleep(5)
                    continue
                    
                response.raise_for_status()
                data = response.json()
                
                profiles = data.get('profiles', [])
                if not profiles:
                    return None
                    
                # Filter for Ifes affiliation
                for profile in profiles:
                    affiliations = profile.get('affiliations', '').lower()
                    email = profile.get('email', '').lower()
                    
                    # Check for Ifes markers
                    if ('ifes' in affiliations or 
                        'instituto federal' in affiliations or 
                        'espírito santo' in affiliations or
                        'espirito santo' in affiliations or
                        'ifes.edu.br' in email):
                        
                        return profile.get('author_id')
                        
                return None
                
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Error searching for {name}: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    return None
        return None

    def update_ids(self):
        researchers = self.data.get('researchers', [])
        updated_count = 0
        
        print(f"Checking {len(researchers)} researchers...")
        
        for i, researcher in enumerate(researchers, 1):
            name = researcher.get('name')
            current_id = researcher.get('scholar_id')
            
            if current_id:
                continue
                
            print(f"[{i}/{len(researchers)}] Searching for: {name}")
            
            new_id = self.search_author(name)
            
            if new_id:
                print(f"  ✓ Found ID: {new_id}")
                researcher['scholar_id'] = new_id
                updated_count += 1
                # Save periodically
                if updated_count % 5 == 0:
                    self.save_data()
            else:
                print("  - No matching profile found")
                
            # Rate limiting
            time.sleep(2)
            
        print(f"\nUpdate complete. Found {updated_count} new IDs.")
        self.save_data()

def main():
    load_dotenv()
    api_key = os.getenv('SEARCHAPI_KEY')
    
    if not api_key:
        print("✗ Error: SEARCHAPI_KEY not found in .env")
        return
        
    data_file = Path('data/scholar_ids.json')
    if not data_file.exists():
        print(f"✗ Error: {data_file} not found")
        return
        
    updater = ScholarIdUpdater(api_key, data_file)
    updater.update_ids()

if __name__ == "__main__":
    main()
