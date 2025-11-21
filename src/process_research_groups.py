#!/usr/bin/env python3
"""
Object-Oriented script to convert research groups CSV to JSON format.

This module processes research group data by:
- Reading CSV files with group information
- Parsing and normalizing leader names and emails
- Generating short names (acronyms) from full names
- Converting to structured JSON format

Input: source/research_groups/research_group.csv
Output: data/research_group.json
"""

import csv
import json
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Leader:
    """Represents a research group leader."""
    
    name: str
    email: str = ''
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert leader to dictionary format.
        
        Returns:
            Dictionary with name and email
        """
        return {
            'name': self.name,
            'email': self.email
        }


@dataclass
class ResearchGroup:
    """Represents a research group with all its attributes."""
    
    name: str
    short_name: str = ''
    campus: str = ''
    knowledge_area: str = ''
    repository: str = ''
    leaders: List[Leader] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """
        Convert research group to dictionary format.
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            'short_name': self.short_name,
            'name': self.name,
            'campus': self.campus,
            'knowledge_area': self.knowledge_area,
            'repository': self.repository,
            'leaders': [leader.to_dict() for leader in self.leaders]
        }


class TextNormalizer:
    """Utility class for text normalization operations."""
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize name to title case.
        
        Args:
            name: Raw name string
            
        Returns:
            Normalized name in title case
        """
        if not name:
            return ''
        return name.strip().title()
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize general text to title case.
        
        Args:
            text: Raw text string
            
        Returns:
            Normalized text
        """
        if not text:
            return ''
        return text.strip().title()


class LeaderParser:
    """Handles parsing of leader information from CSV strings."""
    
    # Regular expression to extract email from parentheses
    EMAIL_PATTERN = re.compile(r'\(([^)]+@[^)]+)\)')
    
    def __init__(self, normalizer: TextNormalizer):
        """
        Initialize parser with a text normalizer.
        
        Args:
            normalizer: TextNormalizer instance for name normalization
        """
        self.normalizer = normalizer
    
    def parse_leaders(self, leaders_str: str) -> List[Leader]:
        """
        Parse leaders string and extract individual leaders with name and email.
        
        The expected format is: "Name1 (email1@domain.com), Name2 (email2@domain.com)"
        
        Args:
            leaders_str: Comma-separated string of leaders with emails
            
        Returns:
            List of Leader objects
        """
        if not leaders_str or not leaders_str.strip():
            return []
        
        leaders = []
        parts = leaders_str.split(',')
        current_leader = []
        
        for part in parts:
            current_leader.append(part.strip())
            
            # If this part contains an email (@), it's the end of a leader entry
            if '@' in part:
                leader_text = ' '.join(current_leader)
                leader = self._extract_leader_info(leader_text)
                leaders.append(leader)
                current_leader = []
        
        # Handle any remaining parts (leaders without email)
        if current_leader:
            leader_text = ' '.join(current_leader)
            leader = Leader(
                name=self.normalizer.normalize_name(leader_text),
                email=''
            )
            leaders.append(leader)
        
        return leaders
    
    def _extract_leader_info(self, leader_text: str) -> Leader:
        """
        Extract name and email from a leader text string.
        
        Args:
            leader_text: Text containing leader name and possibly email
            
        Returns:
            Leader object with extracted information
        """
        email_match = self.EMAIL_PATTERN.search(leader_text)
        
        if email_match:
            email = email_match.group(1).lower()
            name = self.normalizer.normalize_name(
                leader_text[:email_match.start()]
            )
        else:
            # Fallback if format is different
            email = ''
            name = self.normalizer.normalize_name(leader_text)
        
        return Leader(name=name, email=email)


class ShortNameGenerator:
    """Generates short names (acronyms) from full names."""
    
    # Portuguese stop words to ignore when generating acronyms
    STOP_WORDS = {
        'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'para', 
        'a', 'o', 'as', 'os', 'na', 'no', 'nas', 'nos'
    }
    
    @staticmethod
    def generate(name: str) -> str:
        """
        Generate a short name from initial letters of significant words.
        
        Args:
            name: Full name to generate acronym from
            
        Returns:
            Acronym composed of initial letters
        """
        if not name:
            return ''
        
        words = name.split()
        initials = []
        
        for word in words:
            # Remove punctuation from word
            clean_word = ''.join(c for c in word if c.isalnum())
            
            # Skip stop words and empty strings
            if clean_word and clean_word.lower() not in ShortNameGenerator.STOP_WORDS:
                initials.append(clean_word[0].upper())
        
        return ''.join(initials)


class ResearchGroupProcessor:
    """Main processor for converting research group CSV to JSON."""
    
    def __init__(self, input_file: str, output_file: str):
        """
        Initialize processor with file paths.
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output JSON file
        """
        self.input_file = input_file
        self.output_file = output_file
        self.normalizer = TextNormalizer()
        self.leader_parser = LeaderParser(self.normalizer)
        self.short_name_generator = ShortNameGenerator()
        self.research_groups: List[ResearchGroup] = []
    
    def read_csv(self) -> None:
        """Read and parse CSV file into ResearchGroup objects."""
        with open(self.input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                group = self._parse_row(row)
                self.research_groups.append(group)
    
    def _parse_row(self, row: Dict[str, str]) -> ResearchGroup:
        """
        Parse a CSV row into a ResearchGroup object.
        
        Args:
            row: Dictionary representing a CSV row
            
        Returns:
            ResearchGroup object
        """
        # Extract fields from CSV
        sigla = row.get('Sigla', '').strip()
        nome = row.get('Nome', '').strip()
        repository = row.get('Column1', '').strip()
        lideres = row.get('Lideres', '').strip()
        unidade = row.get('Unidade', '').strip()
        area_conhecimento = row.get('AreaConhecimento', '').strip()
        
        # Parse leaders
        leaders_list = self.leader_parser.parse_leaders(lideres)
        
        # Generate short_name if sigla is empty
        if not sigla:
            sigla = self.short_name_generator.generate(nome)
        
        # Create and return research group
        return ResearchGroup(
            name=self.normalizer.normalize_text(nome),
            short_name=sigla,
            campus=self.normalizer.normalize_text(unidade),
            knowledge_area=self.normalizer.normalize_text(area_conhecimento),
            repository=repository,
            leaders=leaders_list
        )
    
    def write_json(self) -> None:
        """Write research groups to JSON file."""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Convert to dictionaries
        groups_data = [group.to_dict() for group in self.research_groups]
        
        # Write to JSON file
        with open(self.output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(groups_data, jsonfile, ensure_ascii=False, indent=2)
    
    def process(self) -> None:
        """Execute the complete CSV to JSON conversion process."""
        print(f"Reading from: {self.input_file}")
        self.read_csv()
        
        print(f"Processing {len(self.research_groups)} research groups...")
        self.write_json()
        
        print(f"Successfully converted {len(self.research_groups)} research groups")
        print(f"Output written to: {self.output_file}")


def main():
    """Main entry point for the script."""
    processor = ResearchGroupProcessor(
        input_file='source/research_groups/research_group.csv',
        output_file='data/research_group.json'
    )
    processor.process()


if __name__ == '__main__':
    main()
