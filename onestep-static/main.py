"""
MkDocs Custom Macros Module

This module provides custom macros for MkDocs documentation generation.
It enables dynamic content loading from JSON data files and provides
utility functions for date handling.

Classes:
    DataLoader: Handles loading of JSON data files with fallback paths
    DateProvider: Provides current date information
    MacroRegistry: Registers all custom macros with MkDocs

Functions:
    define_env: Entry point for MkDocs macro registration
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class DataLoader:
    """
    Handles loading of JSON data files with multiple fallback paths.
    
    This class provides robust data loading with automatic path resolution
    and fallback to empty structures if files are not found.
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize data loader with base path.
        
        Args:
            base_path: Base directory path for resolving relative paths
        """
        self.base_path = base_path
    
    def _get_possible_paths(self, filename: str) -> List[Path]:
        """
        Generate list of possible paths for a data file.
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            List of Path objects to try in order
        """
        return [
            self.base_path.parent / 'data' / filename,
            Path('data') / filename,
            Path('..') / 'data' / filename
        ]
    
    def _load_json(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from a file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Parsed JSON data or None if file doesn't exist or is invalid
        """
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def load_with_fallback(
        self, 
        filename: str, 
        default_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Load JSON file with fallback to default structure.
        
        Args:
            filename: Name of the JSON file
            default_structure: Default structure to return if file not found
            
        Returns:
            Loaded data or default structure
        """
        for path in self._get_possible_paths(filename):
            data = self._load_json(path)
            if data is not None:
                return data
        
        return default_structure
    
    def load_partnership_data(self) -> Dict[str, Any]:
        """
        Load partnership analysis data.
        
        Returns:
            Partnership analysis data dictionary
        """
        json_path = self.base_path.parent / 'data' / 'partnership_analysis.json'
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_scholarship_data(self) -> Dict[str, Any]:
        """
        Load scholarship data with fallback structure.
        
        Returns:
            Scholarship data dictionary
        """
        default = {
            'metadata': {
                'generated_at': '',
                'total_records': 0,
                'source': 'N/A'
            },
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
        
        return self.load_with_fallback('scholarships.json', default)
    
    def load_supervisors_data(self) -> Dict[str, Any]:
        """
        Load supervisors data with fallback structure.
        
        Returns:
            Supervisors data dictionary
        """
        default = {
            'metadata': {
                'generated_at': '',
                'total_supervisors': 0,
                'supervisors_with_projects': 0,
                'supervisors_with_supervisions': 0,
                'supervisors_with_both': 0
            },
            'supervisors': []
        }
        
        return self.load_with_fallback('supervisors.json', default)
    
    def load_students_data(self) -> Dict[str, Any]:
        """
        Load students data with fallback structure.
        
        Returns:
            Students data dictionary
        """
        default = {
            'metadata': {
                'generated_at': '',
                'total_students': 0,
                'students_with_projects': 0,
                'students_with_scholarships': 0,
                'students_with_both': 0,
                'students_with_collaborations': 0
            },
            'students': []
        }
        
        return self.load_with_fallback('students.json', default)
    
    def load_research_lines_data(self) -> Dict[str, Any]:
        """
        Load research lines data with fallback structure.
        
        Returns:
            Research lines data dictionary
        """
        default = {
            'metadata': {
                'generated_at': '',
                'campus': 'Serra',
                'total_research_lines': 0,
                'total_projects': 0,
                'total_supervisors': 0,
                'total_students': 0,
                'total_ic_scholarships': 0
            },
            'research_lines': []
        }
        
        return self.load_with_fallback('research_lines.json', default)
    
    def load_papers_data(self) -> Dict[str, Any]:
        """
        Load papers data with fallback structure.
        
        Returns:
            Papers data dictionary
        """
        default = {
            'campus': 'Serra',
            'total_researchers': 0,
            'generated_at': '',
            'researchers': []
        }
        
        return self.load_with_fallback('papers.json', default)


class DateProvider:
    """Provides current date and time information."""
    
    @staticmethod
    def get_current_date() -> Dict[str, Any]:
        """
        Get current date information.
        
        Returns:
            Dictionary with year, month, day, and formatted date string
        """
        now = datetime.now()
        return {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'date_str': now.strftime('%Y-%m-%d')
        }


class MacroRegistry:
    """
    Registers custom macros with MkDocs environment.
    
    This class manages the registration of all custom macros that
    can be used in MkDocs markdown files.
    """
    
    def __init__(self, env: Any):
        """
        Initialize macro registry.
        
        Args:
            env: MkDocs macro environment object
        """
        self.env = env
        self.data_loader = DataLoader(Path(__file__).parent)
        self.date_provider = DateProvider()
    
    def register_all(self) -> None:
        """Register all custom macros with the environment."""
        # Register date macro
        self.env.macro(self.date_provider.get_current_date)
        
        # Register data loading macros
        self.env.macro(self.data_loader.load_partnership_data)
        self.env.macro(self.data_loader.load_scholarship_data)
        self.env.macro(self.data_loader.load_supervisors_data)
        self.env.macro(self.data_loader.load_students_data)
        self.env.macro(self.data_loader.load_research_lines_data)
        self.env.macro(self.data_loader.load_papers_data)


def define_env(env: Any) -> None:
    """
    Define custom macros for MkDocs.
    
    This function is called by MkDocs to register custom macros
    that can be used in markdown documentation files.
    
    Args:
        env: MkDocs macro environment object
        
    Example:
        In markdown files, use macros like:
        {{ get_current_date() }}
        {{ load_scholarship_data() }}
    """
    registry = MacroRegistry(env)
    registry.register_all()
