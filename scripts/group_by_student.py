#!/usr/bin/env python3
"""
Group research projects and IC scholarships by student.
Creates a JSON file with all projects and scholarships for each student.

STUDENT DATA AGGREGATION:
-------------------------
This script aggregates data from two sources:
1. research_projects.json - Projects where students participated
2. scholarships.json - IC scholarships received by students

For each student, we track:
- Research projects they participated in (from students field)
- IC scholarships they received (as scholarship holder or volunteer)
- Advisors they worked with
- Collaborations with other students on the same projects
- Timeline of activities
- Statistics (total projects, scholarships, years active, etc.)
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any


class StudentDataAggregator:
    """Aggregates research projects and IC scholarships by student."""
    
    def __init__(self, projects_file: Path, scholarships_file: Path):
        self.projects_file = projects_file
        self.scholarships_file = scholarships_file
        self.students = defaultdict(lambda: {
            'name': '',
            'email': '',
            'campus': '',
            'research_projects': [],
            'ic_scholarships': [],
            'advisors': {},
            'collaborations': {},
            'statistics': {
                'total_projects': 0,
                'total_scholarships': 0,
                'total_as_scholarship_holder': 0,
                'total_as_volunteer': 0,
                'years_active': set(),
                'programs': set(),
                'funding_agencies': set(),
                'courses': set()
            }
        })
    
    def load_data(self):
        """Load projects and scholarships data."""
        print("Loading research projects...")
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                self.projects_data = {'projects': data}
            else:
                self.projects_data = data
        
        print("Loading scholarships data...")
        with open(self.scholarships_file, 'r', encoding='utf-8') as f:
            self.scholarships_data = json.load(f)
        
        print(f"✓ Loaded {len(self.projects_data.get('projects', []))} projects")
        print(f"✓ Loaded {len(self.scholarships_data.get('scholarships', []))} scholarships")
    
    def process_research_projects(self):
        """Process research projects and group by student."""
        print("\nProcessing research projects...")
        
        projects = self.projects_data.get('projects', [])
        
        for project in projects:
            students = project.get('students', [])
            if isinstance(students, list):
                students = [s.strip() for s in students if s and s.strip()]
            else:
                students = []
            
            if not students:
                continue
            
            coordinator = project.get('coordinator', '').strip()
            
            # Create project info
            project_info = {
                'id': project.get('id', ''),
                'title': project.get('title', ''),
                'start_date': project.get('start_date', ''),
                'end_date': project.get('end_date', ''),
                'campus': project.get('campus', ''),
                'knowledge_area': project.get('knowledge_area', ''),
                'research_group': project.get('research_group', ''),
                'research_line': project.get('research_line', ''),
                'coordinator': coordinator,
                'researchers': project.get('researchers', []),
                'nature': project.get('nature', ''),
                'partner': project.get('partner', ''),
                'publications_count': project.get('publications_count', '0'),
                'funding_count': project.get('funding_count', '0')
            }
            
            # Process each student in the project
            for student in students:
                if not student:
                    continue
                
                # Initialize student data
                if not self.students[student]['name']:
                    self.students[student]['name'] = student
                
                # Update campus if not set
                if not self.students[student]['campus'] and project.get('campus'):
                    self.students[student]['campus'] = project.get('campus')
                
                # Check for duplicates
                is_duplicate = False
                for existing_project in self.students[student]['research_projects']:
                    if project_info['id'] and existing_project['id']:
                        if existing_project['id'] == project_info['id']:
                            is_duplicate = True
                            break
                    elif project_info['title'] == existing_project['title']:
                        if project_info['start_date'] == existing_project['start_date']:
                            is_duplicate = True
                            break
                
                # Add project if not duplicate
                if not is_duplicate:
                    self.students[student]['research_projects'].append(project_info)
                    self.students[student]['statistics']['total_projects'] += 1
                
                # Track advisor (coordinator)
                if coordinator:
                    if coordinator not in self.students[student]['advisors']:
                        self.students[student]['advisors'][coordinator] = {
                            'count': 0,
                            'projects': []
                        }
                    
                    # Check if this project is already tracked for this advisor
                    advisor_project_ids = [p['id'] for p in self.students[student]['advisors'][coordinator]['projects']]
                    if project_info['id'] not in advisor_project_ids:
                        self.students[student]['advisors'][coordinator]['count'] += 1
                        self.students[student]['advisors'][coordinator]['projects'].append({
                            'title': project_info['title'],
                            'id': project_info['id']
                        })
        
        print(f"✓ Processed projects for {len(self.students)} students")
    
    def process_ic_scholarships(self):
        """Process IC scholarships and group by student."""
        print("\nProcessing IC scholarships...")
        
        scholarships = self.scholarships_data.get('scholarships', [])
        
        # Remove duplicates by ID
        seen_ids = set()
        unique_scholarships = []
        for s in scholarships:
            if s.get('id') not in seen_ids:
                seen_ids.add(s.get('id'))
                unique_scholarships.append(s)
        
        print(f"  Unique scholarships: {len(unique_scholarships)}")
        
        for scholarship in unique_scholarships:
            student = scholarship.get('student', '').strip()
            if not student:
                continue
            
            # Initialize student data
            if not self.students[student]['name']:
                self.students[student]['name'] = student
            
            if not self.students[student]['email'] and scholarship.get('student_email'):
                self.students[student]['email'] = scholarship.get('student_email')
            
            if not self.students[student]['campus'] and scholarship.get('execution_campus'):
                self.students[student]['campus'] = scholarship.get('execution_campus')
            
            # Add scholarship
            scholarship_info = {
                'id': scholarship.get('id', ''),
                'year': scholarship.get('year'),
                'advisor': scholarship.get('advisor', ''),
                'advisor_email': scholarship.get('advisor_email', ''),
                'modality': scholarship.get('modality', ''),
                'program': scholarship.get('program', ''),
                'value': scholarship.get('value'),
                'start_date': scholarship.get('start_date', ''),
                'end_date': scholarship.get('end_date', ''),
                'funding_agency': scholarship.get('funding_agency', ''),
                'execution_campus': scholarship.get('execution_campus', ''),
                'project_title': scholarship.get('project_title', ''),
                'research_project_title': scholarship.get('research_project_title', ''),
                'course': scholarship.get('course', ''),
                'knowledge_area': scholarship.get('knowledge_area', '')
            }
            
            self.students[student]['ic_scholarships'].append(scholarship_info)
            self.students[student]['statistics']['total_scholarships'] += 1
            
            # Update statistics
            if scholarship.get('modality') == 'Bolsista':
                self.students[student]['statistics']['total_as_scholarship_holder'] += 1
            elif scholarship.get('modality') == 'Voluntário':
                self.students[student]['statistics']['total_as_volunteer'] += 1
            
            if scholarship.get('year'):
                self.students[student]['statistics']['years_active'].add(scholarship.get('year'))
            
            if scholarship.get('program'):
                self.students[student]['statistics']['programs'].add(scholarship.get('program'))
            
            if scholarship.get('funding_agency'):
                self.students[student]['statistics']['funding_agencies'].add(scholarship.get('funding_agency'))
            
            if scholarship.get('course'):
                self.students[student]['statistics']['courses'].add(scholarship.get('course'))
            
            # Track advisor
            advisor = scholarship.get('advisor', '').strip()
            if advisor:
                if advisor not in self.students[student]['advisors']:
                    self.students[student]['advisors'][advisor] = {
                        'count': 0,
                        'projects': []
                    }
                
                # Check if this scholarship is already tracked
                advisor_project_ids = [p.get('id') for p in self.students[student]['advisors'][advisor]['projects']]
                if scholarship_info['id'] not in advisor_project_ids:
                    self.students[student]['advisors'][advisor]['count'] += 1
                    self.students[student]['advisors'][advisor]['projects'].append({
                        'title': scholarship_info.get('project_title') or scholarship_info.get('research_project_title', ''),
                        'id': scholarship_info['id'],
                        'type': 'scholarship'
                    })
        
        print(f"✓ Processed scholarships for {len([s for s in self.students.values() if s['ic_scholarships']])} students")
    
    def calculate_collaborations(self):
        """Calculate collaborations between students based on shared projects."""
        print("\nCalculating student collaborations...")
        
        projects = self.projects_data.get('projects', [])
        
        for student_name in self.students.keys():
            collaborators = {}
            
            # Find projects where this student participated
            for project in projects:
                students = project.get('students', [])
                if isinstance(students, list):
                    student_names = [s.strip() for s in students if s and s.strip()]
                else:
                    student_names = []
                
                if student_name in student_names:
                    project_id = project.get('id', '')
                    
                    # Get other students on the same project
                    for other_student in student_names:
                        if other_student and other_student != student_name:
                            if other_student not in collaborators:
                                collaborators[other_student] = {
                                    'count': 0,
                                    'projects': [],
                                    'project_ids': set()
                                }
                            
                            # Only add if not already added
                            if project_id not in collaborators[other_student]['project_ids']:
                                collaborators[other_student]['count'] += 1
                                collaborators[other_student]['projects'].append({
                                    'title': project.get('title', ''),
                                    'id': project_id
                                })
                                collaborators[other_student]['project_ids'].add(project_id)
            
            # Remove project_ids set before storing
            for collab_data in collaborators.values():
                del collab_data['project_ids']
            
            # Store collaborations sorted by count
            self.students[student_name]['collaborations'] = dict(
                sorted(collaborators.items(), key=lambda x: x[1]['count'], reverse=True)
            )
        
        with_collabs = len([s for s in self.students.values() if s['collaborations']])
        print(f"✓ Calculated collaborations for {with_collabs} students with collaborators")
    
    def finalize_statistics(self):
        """Convert sets to sorted lists in statistics."""
        for student_data in self.students.values():
            stats = student_data['statistics']
            stats['years_active'] = sorted(list(stats['years_active']))
            stats['programs'] = sorted(list(stats['programs']))
            stats['funding_agencies'] = sorted(list(stats['funding_agencies']))
            stats['courses'] = sorted(list(stats['courses']))
            
            # Calculate year range
            if stats['years_active']:
                stats['year_range'] = {
                    'min': min(stats['years_active']),
                    'max': max(stats['years_active'])
                }
            else:
                stats['year_range'] = None
            
            # Add collaboration statistics
            if 'collaborations' in student_data:
                stats['total_collaborators'] = len(student_data['collaborations'])
                if student_data['collaborations']:
                    total_collab_projects = sum(c['count'] for c in student_data['collaborations'].values())
                    stats['total_collaborations'] = total_collab_projects
                else:
                    stats['total_collaborations'] = 0
            else:
                stats['total_collaborators'] = 0
                stats['total_collaborations'] = 0
            
            # Add advisor statistics
            stats['total_advisors'] = len(student_data.get('advisors', {}))
    
    def generate_output(self) -> Dict[str, Any]:
        """Generate output data structure."""
        # Convert defaultdict to regular dict and sort by name
        students_list = []
        
        for name, data in sorted(self.students.items()):
            student_entry = {
                'name': data['name'],
                'email': data['email'],
                'campus': data['campus'],
                'statistics': data['statistics'],
                'research_projects': sorted(data['research_projects'], 
                                           key=lambda x: x.get('start_date', ''), 
                                           reverse=True),
                'ic_scholarships': sorted(data['ic_scholarships'], 
                                         key=lambda x: x.get('year', 0), 
                                         reverse=True),
                'advisors': data.get('advisors', {}),
                'collaborations': data.get('collaborations', {})
            }
            students_list.append(student_entry)
        
        # Generate summary statistics
        total_students = len(students_list)
        students_with_projects = len([s for s in students_list if s['research_projects']])
        students_with_scholarships = len([s for s in students_list if s['ic_scholarships']])
        students_with_both = len([s for s in students_list 
                                 if s['research_projects'] and s['ic_scholarships']])
        students_with_collaborations = len([s for s in students_list if s['collaborations']])
        
        # Calculate collaboration network statistics
        total_collaborations = sum(len(s['collaborations']) for s in students_list)
        total_collaboration_instances = sum(
            sum(c['count'] for c in s['collaborations'].values()) 
            for s in students_list
        )
        
        output = {
            'metadata': {
                'generated_at': self._get_timestamp(),
                'total_students': total_students,
                'students_with_projects': students_with_projects,
                'students_with_scholarships': students_with_scholarships,
                'students_with_both': students_with_both,
                'students_with_collaborations': students_with_collaborations,
                'total_unique_collaborations': total_collaborations,
                'total_collaboration_instances': total_collaboration_instances,
                'sources': {
                    'projects': str(self.projects_file),
                    'scholarships': str(self.scholarships_file)
                }
            },
            'students': students_list
        }
        
        return output
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_output(self, output_file: Path, data: Dict[str, Any]):
        """Save output to JSON file."""
        print(f"\nSaving output to {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✓ Output saved successfully!")
    
    def print_summary(self, data: Dict[str, Any]):
        """Print summary statistics."""
        metadata = data['metadata']
        
        print("\n" + "=" * 80)
        print("STUDENT DATA AGGREGATION SUMMARY")
        print("=" * 80)
        print(f"Total students: {metadata['total_students']}")
        print(f"  With research projects: {metadata['students_with_projects']}")
        print(f"  With IC scholarships: {metadata['students_with_scholarships']}")
        print(f"  With both: {metadata['students_with_both']}")
        print(f"  With collaborations: {metadata['students_with_collaborations']}")
        
        print(f"\nCollaboration Network:")
        print(f"  Total unique collaborations: {metadata['total_unique_collaborations']}")
        print(f"  Total collaboration instances: {metadata['total_collaboration_instances']}")
        
        # Top students by projects
        top_by_projects = sorted(data['students'], 
                                key=lambda x: x['statistics']['total_projects'], 
                                reverse=True)[:5]
        
        print("\nTop 5 students by research projects:")
        for i, student in enumerate(top_by_projects, 1):
            print(f"  {i}. {student['name']}: {student['statistics']['total_projects']} projects")
        
        # Top students by scholarships
        top_by_scholarships = sorted(data['students'], 
                                     key=lambda x: x['statistics']['total_scholarships'], 
                                     reverse=True)[:5]
        
        print("\nTop 5 students by IC scholarships:")
        for i, student in enumerate(top_by_scholarships, 1):
            print(f"  {i}. {student['name']}: {student['statistics']['total_scholarships']} scholarships")
        
        # Top students by collaborations
        top_by_collaborations = sorted(data['students'], 
                                      key=lambda x: x['statistics'].get('total_collaborators', 0), 
                                      reverse=True)[:5]
        
        print("\nTop 5 students by number of collaborators:")
        for i, student in enumerate(top_by_collaborations, 1):
            collab_count = student['statistics'].get('total_collaborators', 0)
            collab_instances = student['statistics'].get('total_collaborations', 0)
            print(f"  {i}. {student['name']}: {collab_count} collaborators ({collab_instances} projects)")
        
        print("=" * 80)


def main():
    """Main execution function."""
    print("=" * 80)
    print("GROUP BY STUDENT - Research Projects & IC Scholarships")
    print("=" * 80)
    
    # Configuration
    projects_file = Path('data/research_projects.json')
    scholarships_file = Path('data/scholarships.json')
    output_file = Path('data/students.json')
    
    # Check input files
    if not projects_file.exists():
        print(f"\n✗ Error: {projects_file} not found")
        return
    
    if not scholarships_file.exists():
        print(f"\n✗ Error: {scholarships_file} not found")
        return
    
    # Process data
    aggregator = StudentDataAggregator(projects_file, scholarships_file)
    
    aggregator.load_data()
    aggregator.process_research_projects()
    aggregator.process_ic_scholarships()
    aggregator.calculate_collaborations()
    aggregator.finalize_statistics()
    
    output_data = aggregator.generate_output()
    
    aggregator.save_output(output_file, output_data)
    aggregator.print_summary(output_data)
    
    print(f"\n✓ Student data saved to: {output_file}")


if __name__ == '__main__':
    main()
