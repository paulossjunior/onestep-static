"""
Custom macros for MkDocs
"""
import json
from pathlib import Path


def define_env(env):
    """
    Define custom macros for MkDocs
    """
    
    @env.macro
    def load_partnership_data():
        """
        Load partnership analysis data from JSON file
        """
        json_path = Path(__file__).parent.parent / 'data' / 'partnership_analysis.json'
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    @env.macro
    def load_scholarship_data():
        """
        Load scholarship data from JSON file
        """
        # Try multiple paths
        possible_paths = [
            Path(__file__).parent.parent / 'data' / 'scholarships.json',
            Path('data/scholarships.json'),
            Path('../data/scholarships.json')
        ]
        
        for json_path in possible_paths:
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
        
        # If no path works, return empty structure
        return {
            'metadata': {'generated_at': '', 'total_records': 0, 'source': 'N/A'},
            'statistics': {
                'total_scholarships': 0,
                'by_year': {},
                'by_campus': {},
                'by_modality': {},
                'by_program': {},
                'total_value': 0,
                'years_range': {'min': 0, 'max': 0}
            },
            'scholarships': []
        }
    
    @env.macro
    def load_supervisors_data():
        """
        Load supervisors data from JSON file
        """
        # Try multiple paths
        possible_paths = [
            Path(__file__).parent.parent / 'data' / 'supervisors.json',
            Path('data/supervisors.json'),
            Path('../data/supervisors.json')
        ]
        
        for json_path in possible_paths:
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
        
        # If no path works, return empty structure
        return {
            'metadata': {
                'generated_at': '',
                'total_supervisors': 0,
                'supervisors_with_projects': 0,
                'supervisors_with_supervisions': 0,
                'supervisors_with_both': 0
            },
            'supervisors': []
        }
