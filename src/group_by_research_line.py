#!/usr/bin/env python3
"""
Research Line Data Aggregator

This module aggregates research projects, supervisors, students, and IC scholarships
by research line. It creates a comprehensive view of research activities organized
by thematic areas.

Classes:
    ResearchLineAggregator: Main aggregation logic for research lines
    ResearchLineExporter: Exports aggregated data to JSON

Input: data/research_projects.json, data/supervisors.json, data/students.json, data/scholarships.json
Output: data/research_lines.json
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Set
from datetime import datetime


class ResearchLineAggregator:
    """
    Aggregates research data by research line.
    
    This class processes projects, supervisors, students, and scholarships
    to create a comprehensive view organized by research lines.
    """
    
    def __init__(
        self,
        projects_file: Path,
        supervisors_file: Path,
        students_file: Path,
        scholarships_file: Path
    ):
        """
        Initialize aggregator with data file paths.
        
        Args:
            projects_file: Path to research projects JSON
            supervisors_file: Path to supervisors JSON
            students_file: Path to students JSON
            scholarships_file: Path to scholarships JSON
        """
        self.projects_file = projects_file
        self.supervisors_file = supervisors_file
        self.students_file = students_file
        self.scholarships_file = scholarships_file
        
        self.research_lines: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                'name': '',
                'projects': [],
                'supervisors': set(),
                'students': set(),
                'ic_scholarships': [],
                'knowledge_areas': set(),
                'statistics': {
                    'total_projects': 0,
                    'total_supervisors': 0,
                    'total_students': 0,
                    'total_ic_scholarships': 0,
                    'projects_with_funding': 0,
                    'projects_without_funding': 0,
                    'years_active': set()
                }
            }
        )
    
    def load_data(self) -> None:
        """Load all data files."""
        print("Loading data files...")
        
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            self.projects_data = json.load(f)
        
        with open(self.supervisors_file, 'r', encoding='utf-8') as f:
            self.supervisors_data = json.load(f)
        
        with open(self.students_file, 'r', encoding='utf-8') as f:
            self.students_data = json.load(f)
        
        with open(self.scholarships_file, 'r', encoding='utf-8') as f:
            self.scholarships_data = json.load(f)
        
        print(f"✓ Loaded {len(self.projects_data)} projects")
        print(f"✓ Loaded {len(self.supervisors_data['supervisors'])} supervisors")
        print(f"✓ Loaded {len(self.students_data['students'])} students")
        print(f"✓ Loaded {len(self.scholarships_data['scholarships'])} scholarships")
    
    def process_projects(self) -> None:
        """Process research projects and group by research line."""
        print("\nProcessing research projects by research line...")
        
        for project in self.projects_data:
            # Skip if not Serra campus
            if project.get('campus') != 'Serra':
                continue
            
            research_line = project.get('research_line', '').strip()
            
            # Skip if no research line
            if not research_line:
                research_line = 'Not Specified'
            
            # Initialize research line
            if not self.research_lines[research_line]['name']:
                self.research_lines[research_line]['name'] = research_line
            
            # Add project
            project_info = {
                'id': project.get('id', ''),
                'title': project.get('title', ''),
                'coordinator': project.get('coordinator', ''),
                'start_date': project.get('start_date', ''),
                'end_date': project.get('end_date', ''),
                'knowledge_area': project.get('knowledge_area', ''),
                'research_group': project.get('research_group', ''),
                'nature': project.get('nature', ''),
                'partner': project.get('partner', ''),
                'funding_count': project.get('funding_count', '0'),
                'publications_count': project.get('publications_count', '0'),
                'students': project.get('students', []),
                'researchers': project.get('researchers', [])
            }
            
            self.research_lines[research_line]['projects'].append(project_info)
            self.research_lines[research_line]['statistics']['total_projects'] += 1
            
            # Track funding
            if project.get('partner') or int(project.get('funding_count', '0')) > 0:
                self.research_lines[research_line]['statistics']['projects_with_funding'] += 1
            else:
                self.research_lines[research_line]['statistics']['projects_without_funding'] += 1
            
            # Track coordinator
            coordinator = project.get('coordinator', '').strip()
            if coordinator:
                self.research_lines[research_line]['supervisors'].add(coordinator)
            
            # Track researchers
            for researcher in project.get('researchers', []):
                if researcher and researcher.strip():
                    self.research_lines[research_line]['supervisors'].add(researcher.strip())
            
            # Track students
            for student in project.get('students', []):
                if student and student.strip():
                    self.research_lines[research_line]['students'].add(student.strip())
            
            # Track knowledge area
            knowledge_area = project.get('knowledge_area', '').strip()
            if knowledge_area:
                self.research_lines[research_line]['knowledge_areas'].add(knowledge_area)
            
            # Track year
            if project.get('start_date') and len(project['start_date']) >= 8:
                year = int('20' + project['start_date'][-2:])
                self.research_lines[research_line]['statistics']['years_active'].add(year)
        
        print(f"✓ Processed {len(self.research_lines)} research lines")
    
    def process_scholarships(self) -> None:
        """Process IC scholarships and associate with research lines."""
        print("\nProcessing IC scholarships...")
        
        # Create a mapping of project titles to research lines
        project_to_line = {}
        for line_name, line_data in self.research_lines.items():
            for project in line_data['projects']:
                if project['title']:
                    project_to_line[project['title'].lower()] = line_name
        
        scholarships_added = 0
        for scholarship in self.scholarships_data['scholarships']:
            # Skip if not Serra campus
            if scholarship.get('execution_campus') != 'Serra':
                continue
            
            # Try to match scholarship to research line via project title
            research_project_title = scholarship.get('research_project_title', '').strip()
            project_title = scholarship.get('project_title', '').strip()
            
            matched_line = None
            
            # Try to match by research project title
            if research_project_title:
                matched_line = project_to_line.get(research_project_title.lower())
            
            # Try to match by project title
            if not matched_line and project_title:
                matched_line = project_to_line.get(project_title.lower())
            
            # If matched, add to research line
            if matched_line:
                scholarship_info = {
                    'id': scholarship.get('id', ''),
                    'student': scholarship.get('student', ''),
                    'advisor': scholarship.get('advisor', ''),
                    'year': scholarship.get('year'),
                    'modality': scholarship.get('modality', ''),
                    'program': scholarship.get('program', ''),
                    'project_title': project_title or research_project_title
                }
                
                self.research_lines[matched_line]['ic_scholarships'].append(scholarship_info)
                self.research_lines[matched_line]['statistics']['total_ic_scholarships'] += 1
                
                # Track student
                student = scholarship.get('student', '').strip()
                if student:
                    self.research_lines[matched_line]['students'].add(student)
                
                # Track advisor
                advisor = scholarship.get('advisor', '').strip()
                if advisor:
                    self.research_lines[matched_line]['supervisors'].add(advisor)
                
                scholarships_added += 1
        
        print(f"✓ Associated {scholarships_added} scholarships with research lines")
    
    def finalize_statistics(self) -> None:
        """Convert sets to lists and calculate final statistics."""
        print("\nFinalizing statistics...")
        
        for line_name, line_data in self.research_lines.items():
            # Convert sets to sorted lists
            line_data['supervisors'] = sorted(list(line_data['supervisors']))
            line_data['students'] = sorted(list(line_data['students']))
            line_data['knowledge_areas'] = sorted(list(line_data['knowledge_areas']))
            
            stats = line_data['statistics']
            stats['years_active'] = sorted(list(stats['years_active']))
            
            # Update counts
            stats['total_supervisors'] = len(line_data['supervisors'])
            stats['total_students'] = len(line_data['students'])
            
            # Calculate year range
            if stats['years_active']:
                stats['year_range'] = {
                    'min': min(stats['years_active']),
                    'max': max(stats['years_active'])
                }
            else:
                stats['year_range'] = None
        
        print(f"✓ Finalized statistics for {len(self.research_lines)} research lines")
    
    def generate_output(self) -> Dict[str, Any]:
        """
        Generate output data structure.
        
        Returns:
            Dictionary with metadata and research lines data
        """
        # Sort research lines by number of projects (descending)
        sorted_lines = sorted(
            self.research_lines.items(),
            key=lambda x: x[1]['statistics']['total_projects'],
            reverse=True
        )
        
        research_lines_list = []
        for line_name, line_data in sorted_lines:
            # Skip "Not Specified" if it has no projects
            if line_name == 'Not Specified' and line_data['statistics']['total_projects'] == 0:
                continue
            
            research_lines_list.append({
                'name': line_data['name'],
                'statistics': line_data['statistics'],
                'projects': sorted(
                    line_data['projects'],
                    key=lambda x: x.get('start_date', ''),
                    reverse=True
                ),
                'supervisors': line_data['supervisors'],
                'students': line_data['students'],
                'ic_scholarships': sorted(
                    line_data['ic_scholarships'],
                    key=lambda x: x.get('year', 0),
                    reverse=True
                ),
                'knowledge_areas': line_data['knowledge_areas']
            })
        
        # Generate summary statistics
        total_lines = len(research_lines_list)
        total_projects = sum(line['statistics']['total_projects'] for line in research_lines_list)
        total_supervisors = len(set(
            sup for line in research_lines_list for sup in line['supervisors']
        ))
        total_students = len(set(
            student for line in research_lines_list for student in line['students']
        ))
        total_scholarships = sum(
            line['statistics']['total_ic_scholarships'] for line in research_lines_list
        )
        
        output = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'campus': 'Serra',
                'total_research_lines': total_lines,
                'total_projects': total_projects,
                'total_supervisors': total_supervisors,
                'total_students': total_students,
                'total_ic_scholarships': total_scholarships
            },
            'research_lines': research_lines_list
        }
        
        return output


class ResearchLineExporter:
    """Exports research line data to JSON file."""
    
    def __init__(self, output_file: Path):
        """
        Initialize exporter with output file path.
        
        Args:
            output_file: Path to output JSON file
        """
        self.output_file = output_file
    
    def export(self, data: Dict[str, Any]) -> None:
        """
        Export data to JSON file.
        
        Args:
            data: Research lines data to export
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Data exported to: {self.output_file}")
    
    def print_summary(self, data: Dict[str, Any]) -> None:
        """
        Print summary of exported data.
        
        Args:
            data: Research lines data
        """
        metadata = data['metadata']
        
        print("\n" + "=" * 80)
        print("RESEARCH LINES AGGREGATION SUMMARY")
        print("=" * 80)
        print(f"Campus: {metadata['campus']}")
        print(f"Total Research Lines: {metadata['total_research_lines']}")
        print(f"Total Projects: {metadata['total_projects']}")
        print(f"Total Supervisors: {metadata['total_supervisors']}")
        print(f"Total Students: {metadata['total_students']}")
        print(f"Total IC Scholarships: {metadata['total_ic_scholarships']}")
        
        print("\nTop 10 Research Lines by Projects:")
        for i, line in enumerate(data['research_lines'][:10], 1):
            print(f"  {i}. {line['name']}: {line['statistics']['total_projects']} projects")
        
        print("=" * 80)


def main():
    """Main execution function."""
    print("=" * 80)
    print("GROUP BY RESEARCH LINE - Projects, Supervisors, Students & IC")
    print("=" * 80)
    
    # Configuration
    projects_file = Path('data/research_projects.json')
    supervisors_file = Path('data/supervisors.json')
    students_file = Path('data/students.json')
    scholarships_file = Path('data/scholarships.json')
    output_file = Path('data/research_lines.json')
    
    # Check input files
    for file_path in [projects_file, supervisors_file, students_file, scholarships_file]:
        if not file_path.exists():
            print(f"\n✗ Error: {file_path} not found")
            return
    
    # Process data
    aggregator = ResearchLineAggregator(
        projects_file,
        supervisors_file,
        students_file,
        scholarships_file
    )
    
    aggregator.load_data()
    aggregator.process_projects()
    aggregator.process_scholarships()
    aggregator.finalize_statistics()
    
    output_data = aggregator.generate_output()
    
    # Export data
    exporter = ResearchLineExporter(output_file)
    exporter.export(output_data)
    exporter.print_summary(output_data)
    
    print(f"\n✓ Research lines data saved to: {output_file}")


if __name__ == '__main__':
    main()
