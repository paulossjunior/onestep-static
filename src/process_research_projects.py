#!/usr/bin/env python3
"""
Object-Oriented script to convert research projects CSV files to JSON format.

This module processes research project data by:
- Reading multiple CSV files from a directory
- Parsing and normalizing project information
- Converting to structured JSON format
- Automatically detecting and adding missing research groups

Input: source/research_project/*.csv
Output: data/research_projects.json
Updates: data/research_group.json (adds missing groups)
"""

import csv
import json
import os
import glob
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class ResearchProject:
    """Represents a research project with all its attributes."""
    
    campus: str
    id: str
    start_date: str
    end_date: str
    title: str
    coordinator: str
    coordinator_email: str
    researchers: List[str] = field(default_factory=list)
    students: List[str] = field(default_factory=list)
    other_count: str = '0'
    research_group: str = ''
    external_research_group: str = ''
    research_line: str = ''
    publications_count: str = '0'
    funding_count: str = '0'
    knowledge_area: str = ''
    keywords: List[str] = field(default_factory=list)
    nature: str = ''
    partner: str = ''
    innovation_pole_partnership: str = ''
    confidential: bool = False
    board_opinion: str = ''
    
    def to_dict(self) -> Dict:
        """
        Convert project to dictionary format.
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return asdict(self)


class TextNormalizer:
    """Utility class for text normalization operations."""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text to title case.
        
        Args:
            text: Raw text string
            
        Returns:
            Normalized text in title case
        """
        if not text:
            return ''
        return text.strip().title()
    
    @staticmethod
    def normalize_email(email: str) -> str:
        """
        Normalize email to lowercase.
        
        Args:
            email: Raw email string
            
        Returns:
            Normalized email in lowercase
        """
        if not email:
            return ''
        return email.strip().lower()


class FieldParser:
    """Handles parsing of various field types from CSV."""
    
    def __init__(self, normalizer: TextNormalizer):
        """
        Initialize parser with a text normalizer.
        
        Args:
            normalizer: TextNormalizer instance
        """
        self.normalizer = normalizer
    
    def parse_list_field(self, field_str: str) -> List[str]:
        """
        Parse semicolon-separated fields into a list.
        
        Args:
            field_str: Semicolon-separated string
            
        Returns:
            List of normalized items
        """
        if not field_str or not field_str.strip():
            return []
        
        return [
            self.normalizer.normalize_text(item)
            for item in field_str.split(';')
            if item.strip()
        ]
    
    @staticmethod
    def parse_boolean(value: str) -> bool:
        """
        Parse boolean values from CSV.
        
        Args:
            value: String representation of boolean
            
        Returns:
            Boolean value
        """
        if isinstance(value, str):
            return value.upper() == 'TRUE'
        return bool(value)


class ResearchGroupManager:
    """Manages research groups and handles missing group detection."""
    
    def __init__(self, groups_file: str):
        """
        Initialize manager with groups file path.
        
        Args:
            groups_file: Path to research groups JSON file
        """
        self.groups_file = groups_file
        self.groups: List[Dict] = []
        self.new_groups_added = 0
    
    def load_groups(self) -> None:
        """Load existing research groups from JSON file."""
        if not os.path.exists(self.groups_file):
            self.groups = []
            return
        
        with open(self.groups_file, 'r', encoding='utf-8') as f:
            self.groups = json.load(f)
        
        print(f"Loaded {len(self.groups)} existing research groups")
    
    def save_groups(self) -> None:
        """Save research groups to JSON file."""
        with open(self.groups_file, 'w', encoding='utf-8') as f:
            json.dump(self.groups, f, ensure_ascii=False, indent=2)
    
    def group_exists(self, group_name: str) -> bool:
        """
        Check if a research group already exists.
        
        Args:
            group_name: Name of the research group
            
        Returns:
            True if group exists, False otherwise
        """
        return any(
            group.get('name', '') == group_name
            for group in self.groups
        )
    
    def add_missing_group(
        self,
        group_name: str,
        campus: str,
        knowledge_area: str
    ) -> bool:
        """
        Add a research group if it doesn't exist.
        
        Args:
            group_name: Name of the research group
            campus: Campus where the group is located
            knowledge_area: Knowledge area of the group
            
        Returns:
            True if group was added, False if it already existed
        """
        if not group_name or self.group_exists(group_name):
            return False
        
        # Create new group entry
        new_group = {
            'short_name': '',
            'name': group_name,
            'campus': campus,
            'knowledge_area': knowledge_area,
            'repository': '',
            'leaders': []
        }
        
        self.groups.append(new_group)
        self.new_groups_added += 1
        print(f"  Added new research group: {group_name}")
        
        return True


class CSVProjectParser:
    """Parses research projects from CSV rows."""
    
    def __init__(self, normalizer: TextNormalizer, field_parser: FieldParser):
        """
        Initialize parser with normalizer and field parser.
        
        Args:
            normalizer: TextNormalizer instance
            field_parser: FieldParser instance
        """
        self.normalizer = normalizer
        self.field_parser = field_parser
    
    def parse_row(self, row: Dict[str, str]) -> ResearchProject:
        """
        Parse a CSV row into a ResearchProject object.
        
        Args:
            row: Dictionary representing a CSV row
            
        Returns:
            ResearchProject object
        """
        return ResearchProject(
            campus=self.normalizer.normalize_text(row.get('CampusExecucao', '')),
            id=row.get('Id', '').strip(),
            start_date=row.get('Inicio', '').strip(),
            end_date=row.get('Fim', '').strip(),
            title=self.normalizer.normalize_text(row.get('Titulo', '')),
            coordinator=self.normalizer.normalize_text(row.get('Coordenador', '')),
            coordinator_email=self.normalizer.normalize_email(row.get('EmailCoordenador', '')),
            researchers=self.field_parser.parse_list_field(row.get('Pesquisadores', '')),
            students=self.field_parser.parse_list_field(row.get('Estudantes', '')),
            other_count=row.get('QtdOutros', '0').strip(),
            research_group=self.normalizer.normalize_text(row.get('GrupoPesquisa', '')),
            external_research_group=self.normalizer.normalize_text(row.get('GrupoPesquisaExterno', '')),
            research_line=self.normalizer.normalize_text(row.get('LinhaPesquisa', '')),
            publications_count=row.get('QtdPts', '0').strip(),
            funding_count=row.get('QtdFinanciamentos', '0').strip(),
            knowledge_area=self.normalizer.normalize_text(row.get('AreaConhecimento', '')),
            keywords=self.field_parser.parse_list_field(row.get('PalavraChave', '')),
            nature=self.normalizer.normalize_text(row.get('Natureza', '')),
            partner=self.normalizer.normalize_text(row.get('ParceiroDemandante', '')),
            innovation_pole_partnership=row.get('ParceriaPoloInovacaoConfirmado', '').strip(),
            confidential=self.field_parser.parse_boolean(row.get('Sigilo', 'FALSE')),
            board_opinion=self.normalizer.normalize_text(row.get('ParecerDiretoria', ''))
        )


class ResearchProjectProcessor:
    """Main processor for converting research project CSV files to JSON."""
    
    def __init__(self, input_dir: str, output_file: str, groups_file: str):
        """
        Initialize processor with file paths.
        
        Args:
            input_dir: Directory containing CSV files
            output_file: Path to output JSON file
            groups_file: Path to research groups JSON file
        """
        self.input_dir = input_dir
        self.output_file = output_file
        self.normalizer = TextNormalizer()
        self.field_parser = FieldParser(self.normalizer)
        self.csv_parser = CSVProjectParser(self.normalizer, self.field_parser)
        self.group_manager = ResearchGroupManager(groups_file)
        self.projects: List[ResearchProject] = []
    
    def read_csv_files(self) -> None:
        """Read and parse all CSV files in the input directory."""
        # Get all CSV files
        csv_files = glob.glob(os.path.join(self.input_dir, '*.csv'))
        
        if not csv_files:
            print(f"Warning: No CSV files found in {self.input_dir}")
            return
        
        for csv_file in sorted(csv_files):
            print(f"Processing: {csv_file}")
            self._process_csv_file(csv_file)
    
    def _process_csv_file(self, csv_file: str) -> None:
        """
        Process a single CSV file.
        
        Args:
            csv_file: Path to CSV file
        """
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                project = self.csv_parser.parse_row(row)
                self.projects.append(project)
                
                # Check and add missing research group
                if project.research_group:
                    self.group_manager.add_missing_group(
                        project.research_group,
                        project.campus,
                        project.knowledge_area
                    )
    
    def write_json(self) -> None:
        """Write research projects to JSON file."""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Convert to dictionaries
        projects_data = [project.to_dict() for project in self.projects]
        
        # Write to JSON file
        with open(self.output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(projects_data, jsonfile, ensure_ascii=False, indent=2)
    
    def process(self) -> None:
        """Execute the complete CSV to JSON conversion process."""
        # Load existing research groups
        self.group_manager.load_groups()
        
        # Process CSV files
        self.read_csv_files()
        
        # Write outputs
        print(f"\nWriting {len(self.projects)} projects to JSON...")
        self.write_json()
        
        # Save updated research groups
        self.group_manager.save_groups()
        
        # Print summary
        print(f"\nSuccessfully converted {len(self.projects)} research projects")
        print(f"Output written to: {self.output_file}")
        print(f"Added {self.group_manager.new_groups_added} new research groups")
        print(f"Total research groups: {len(self.group_manager.groups)}")


def main():
    """Main entry point for the script."""
    processor = ResearchProjectProcessor(
        input_dir='source/research_project',
        output_file='data/research_projects.json',
        groups_file='data/research_group.json'
    )
    processor.process()


if __name__ == '__main__':
    main()
