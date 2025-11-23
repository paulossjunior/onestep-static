#!/usr/bin/env python3
"""
Student Recurrence Statistics Calculator

This module calculates and analyzes student participation recurrence in IC 
(Scientific Initiation) scholarship programs. It tracks how many times each 
student participated, their modality preferences (scholarship holder vs volunteer),
and generates distribution statistics.

Classes:
    StudentParticipation: Tracks individual student participation counts
    RecurrenceAnalyzer: Analyzes recurrence patterns across all students
    RecurrenceStatisticsCalculator: Main orchestrator for the analysis

Input: data/scholarships.json
Output: Updates data/scholarships.json with recurrence statistics
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class StudentParticipation:
    """
    Tracks participation counts for a single student.
    
    Attributes:
        student_name: Name of the student
        total: Total number of IC participations
        bolsista: Number of participations as scholarship holder
        voluntario: Number of participations as volunteer
    """
    
    student_name: str
    total: int = 0
    bolsista: int = 0
    voluntario: int = 0
    
    def add_participation(self, modality: str) -> None:
        """
        Record a new participation for this student.
        
        Args:
            modality: Type of participation ('Bolsista' or 'Voluntário')
        """
        self.total += 1
        
        if modality == 'Bolsista':
            self.bolsista += 1
        elif modality == 'Voluntário':
            self.voluntario += 1
    
    @property
    def profile_type(self) -> str:
        """
        Determine the student's participation profile.
        
        Returns:
            'only_bolsista', 'only_voluntario', or 'mixed'
        """
        if self.bolsista > 0 and self.voluntario > 0:
            return 'mixed'
        elif self.bolsista > 0:
            return 'only_bolsista'
        elif self.voluntario > 0:
            return 'only_voluntario'
        return 'none'


class ScholarshipFilter:
    """Filters and deduplicates scholarship data."""
    
    @staticmethod
    def filter_by_campus(
        scholarships: List[Dict[str, Any]], 
        campus: str
    ) -> List[Dict[str, Any]]:
        """
        Filter scholarships by campus and remove duplicates.
        
        Args:
            scholarships: List of scholarship dictionaries
            campus: Campus name to filter by
            
        Returns:
            List of unique scholarships for the specified campus
        """
        seen_ids = set()
        filtered = []
        
        for scholarship in scholarships:
            scholarship_id = scholarship.get('id')
            execution_campus = scholarship.get('execution_campus')
            
            if execution_campus == campus and scholarship_id not in seen_ids:
                seen_ids.add(scholarship_id)
                filtered.append(scholarship)
        
        return filtered


class RecurrenceAnalyzer:
    """
    Analyzes student recurrence patterns in IC scholarships.
    
    This class processes scholarship data to identify how many times students
    participated in IC programs and calculates various distribution statistics.
    """
    
    def __init__(self, scholarships: List[Dict[str, Any]]):
        """
        Initialize analyzer with scholarship data.
        
        Args:
            scholarships: List of scholarship dictionaries
        """
        self.scholarships = scholarships
        self.student_participations: Dict[str, StudentParticipation] = {}
    
    def analyze(self) -> None:
        """Process all scholarships and build participation records."""
        for scholarship in self.scholarships:
            student_name = scholarship.get('student', '').strip()
            if not student_name:
                continue
            
            # Get or create student participation record
            if student_name not in self.student_participations:
                self.student_participations[student_name] = StudentParticipation(
                    student_name=student_name
                )
            
            # Record this participation
            modality = scholarship.get('modality', '')
            self.student_participations[student_name].add_participation(modality)
    
    def get_profile_counts(self) -> Dict[str, int]:
        """
        Count students by their participation profile.
        
        Returns:
            Dictionary with counts for each profile type
        """
        profiles = {
            'only_bolsista': 0,
            'only_voluntario': 0,
            'mixed': 0
        }
        
        for participation in self.student_participations.values():
            profile = participation.profile_type
            if profile in profiles:
                profiles[profile] += 1
        
        return profiles
    
    def get_participation_distribution(self) -> Dict[int, int]:
        """
        Calculate distribution of total participations.
        
        Returns:
            Dictionary mapping participation count to number of students
        """
        distribution = defaultdict(int)
        
        for participation in self.student_participations.values():
            distribution[participation.total] += 1
        
        return dict(sorted(distribution.items()))
    
    def get_bolsista_distribution(self) -> Dict[int, int]:
        """
        Calculate distribution of scholarship holder participations.
        
        Returns:
            Dictionary mapping bolsista count to number of students
        """
        distribution = defaultdict(int)
        
        for participation in self.student_participations.values():
            if participation.bolsista > 0:
                distribution[participation.bolsista] += 1
        
        return dict(sorted(distribution.items()))
    
    def get_voluntario_distribution(self) -> Dict[int, int]:
        """
        Calculate distribution of volunteer participations.
        
        Returns:
            Dictionary mapping voluntario count to number of students
        """
        distribution = defaultdict(int)
        
        for participation in self.student_participations.values():
            if participation.voluntario > 0:
                distribution[participation.voluntario] += 1
        
        return dict(sorted(distribution.items()))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Generate complete recurrence statistics.
        
        Returns:
            Dictionary containing all calculated statistics
        """
        return {
            'total_unique_students': len(self.student_participations),
            'total_scholarships': len(self.scholarships),
            'student_profiles': self.get_profile_counts(),
            'participation_distribution': self.get_participation_distribution(),
            'bolsista_distribution': self.get_bolsista_distribution(),
            'voluntario_distribution': self.get_voluntario_distribution()
        }


class StatisticsPrinter:
    """Handles formatted printing of recurrence statistics."""
    
    @staticmethod
    def print_summary(stats: Dict[str, Any]) -> None:
        """
        Print formatted summary of recurrence statistics.
        
        Args:
            stats: Statistics dictionary from RecurrenceAnalyzer
        """
        print(f"\n{'='*60}")
        print("STUDENT RECURRENCE STATISTICS - CAMPUS SERRA")
        print(f"{'='*60}")
        print(f"Total unique students: {stats['total_unique_students']}")
        print(f"Total scholarships: {stats['total_scholarships']}")
        
        print(f"\nStudent Profiles:")
        profiles = stats['student_profiles']
        print(f"  Only Bolsista: {profiles['only_bolsista']}")
        print(f"  Only Voluntário: {profiles['only_voluntario']}")
        print(f"  Mixed (both): {profiles['mixed']}")
        
        print(f"\nParticipation Distribution:")
        for count, students in stats['participation_distribution'].items():
            print(f"  {count} IC(s): {students} students")
        
        print(f"\nBolsista Distribution:")
        for count, students in stats['bolsista_distribution'].items():
            print(f"  {count} bolsa(s): {students} students")
        
        print(f"\nVoluntário Distribution:")
        for count, students in stats['voluntario_distribution'].items():
            print(f"  {count} voluntário(s): {students} students")
        
        print(f"{'='*60}\n")


class RecurrenceStatisticsCalculator:
    """
    Main calculator for student recurrence statistics.
    
    This class orchestrates the entire process of loading scholarship data,
    analyzing recurrence patterns, and saving the results.
    """
    
    def __init__(self, data_file: Path, campus: str = 'Serra'):
        """
        Initialize calculator with file path and campus filter.
        
        Args:
            data_file: Path to scholarships JSON file
            campus: Campus name to filter by (default: 'Serra')
        """
        self.data_file = data_file
        self.campus = campus
        self.data: Dict[str, Any] = {}
        self.scholarships: List[Dict[str, Any]] = []
    
    def load_data(self) -> None:
        """Load scholarship data from JSON file."""
        print(f"Loading data from {self.data_file}...")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.scholarships = self.data.get('scholarships', [])
        print(f"Total scholarships in file: {len(self.scholarships)}")
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Calculate recurrence statistics for the specified campus.
        
        Returns:
            Dictionary containing all recurrence statistics
        """
        print(f"\nCalculating student recurrence statistics for Campus {self.campus}...")
        
        # Filter scholarships by campus
        filtered_scholarships = ScholarshipFilter.filter_by_campus(
            self.scholarships, 
            self.campus
        )
        
        # Analyze recurrence patterns
        analyzer = RecurrenceAnalyzer(filtered_scholarships)
        analyzer.analyze()
        
        return analyzer.get_statistics()
    
    def save_statistics(self, stats: Dict[str, Any]) -> None:
        """
        Save statistics to the data file.
        
        Args:
            stats: Statistics dictionary to save
        """
        # Ensure statistics section exists
        if 'statistics' not in self.data:
            self.data['statistics'] = {}
        
        # Add recurrence statistics
        self.data['statistics']['student_recurrence_serra'] = stats
        
        # Save updated data
        print(f"Saving updated data to {self.data_file}...")
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print("✓ Student recurrence statistics calculated and saved successfully!")
        print(f"\nStatistics added to: data['statistics']['student_recurrence_serra']")
    
    def run(self) -> None:
        """Execute the complete recurrence statistics calculation process."""
        self.load_data()
        stats = self.calculate_statistics()
        StatisticsPrinter.print_summary(stats)
        self.save_statistics(stats)


def main():
    """Main entry point for the script."""
    calculator = RecurrenceStatisticsCalculator(
        data_file=Path('data/scholarships.json'),
        campus='Serra'
    )
    calculator.run()


if __name__ == '__main__':
    main()
