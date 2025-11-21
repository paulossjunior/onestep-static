#!/usr/bin/env python3
"""
Group research projects and IC supervisions by supervisor/advisor.
Creates a JSON file with all projects and supervisions for each researcher.

COLLABORATION CALCULATION:
--------------------------
Collaborations are calculated based on the research_projects.json structure:
- Each project has a 'coordinator' (project leader)
- Each project has a 'researchers' array (team members)

A collaboration exists when two people work together on the same project:
1. Coordinator ↔ Researcher: When a coordinator leads a project with researchers
2. Researcher ↔ Coordinator: When a researcher participates in a coordinator's project
3. Researcher ↔ Researcher: When multiple researchers work on the same project

For each collaboration, we track:
- count: Number of shared projects
- projects: List of projects worked on together (with title, id, and role)
- role: The person's role in that specific project (coordinator, researcher, or co-researcher)

Example:
If Project A has:
  coordinator: "Alice"
  researchers: ["Bob", "Charlie"]

Then:
- Alice collaborates with Bob (1 project, Alice as coordinator)
- Alice collaborates with Charlie (1 project, Alice as coordinator)
- Bob collaborates with Alice (1 project, Bob as researcher)
- Bob collaborates with Charlie (1 project, Bob as co-researcher)
- Charlie collaborates with Alice (1 project, Charlie as researcher)
- Charlie collaborates with Bob (1 project, Charlie as co-researcher)
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any


class SupervisorDataAggregator:
    """Aggregates research projects and IC supervisions by supervisor."""
    
    def __init__(self, projects_file: Path, scholarships_file: Path):
        self.projects_file = projects_file
        self.scholarships_file = scholarships_file
        self.supervisors = defaultdict(lambda: {
            'name': '',
            'email': '',
            'campus': '',
            'research_projects': [],
            'ic_supervisions': [],
            'collaborations': {},
            'statistics': {
                'total_projects': 0,
                'total_supervisions': 0,
                'total_scholarship_holders': 0,
                'total_volunteers': 0,
                'years_active': set(),
                'programs': set(),
                'funding_agencies': set()
            }
        })
    
    def load_data(self):
        """Load projects and scholarships data."""
        print("Loading research projects...")
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both list and dict formats
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
        """Process research projects and group by coordinator."""
        print("\nProcessing research projects...")
        
        projects = self.projects_data.get('projects', [])
        
        for project in projects:
            coordinator = project.get('coordinator', '').strip()
            if not coordinator:
                continue
            
            # Initialize supervisor data
            if not self.supervisors[coordinator]['name']:
                self.supervisors[coordinator]['name'] = coordinator
            
            # Update email if available
            if not self.supervisors[coordinator]['email'] and project.get('coordinator_email'):
                self.supervisors[coordinator]['email'] = project.get('coordinator_email')
            
            # Get researchers list
            researchers = project.get('researchers', [])
            if isinstance(researchers, list):
                researchers = [r.strip() for r in researchers if r and r.strip()]
            else:
                researchers = []
            
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
                'researchers': researchers,
                'nature': project.get('nature', ''),
                'partner': project.get('partner', ''),
                'publications_count': project.get('publications_count', '0'),
                'funding_count': project.get('funding_count', '0')
            }
            
            # Check for duplicates by id or title
            is_duplicate = False
            for existing_project in self.supervisors[coordinator]['research_projects']:
                # Check by id if both have ids
                if project_info['id'] and existing_project['id']:
                    if existing_project['id'] == project_info['id']:
                        is_duplicate = True
                        break
                # Check by title if no id or ids don't match
                elif project_info['title'] == existing_project['title']:
                    # Same title - check if dates are similar (likely duplicate)
                    if project_info['start_date'] == existing_project['start_date']:
                        is_duplicate = True
                        break
            
            # Only add if not duplicate
            if not is_duplicate:
                self.supervisors[coordinator]['research_projects'].append(project_info)
                self.supervisors[coordinator]['statistics']['total_projects'] += 1
            
            # Update campus if not set
            if not self.supervisors[coordinator]['campus'] and project.get('campus'):
                self.supervisors[coordinator]['campus'] = project.get('campus')
        
        print(f"✓ Processed projects for {len(self.supervisors)} coordinators")
    
    def process_ic_supervisions(self):
        """Process IC supervisions and group by advisor."""
        print("\nProcessing IC supervisions...")
        
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
            advisor = scholarship.get('advisor', '').strip()
            if not advisor:
                continue
            
            # Initialize supervisor data
            if not self.supervisors[advisor]['name']:
                self.supervisors[advisor]['name'] = advisor
            
            if not self.supervisors[advisor]['email'] and scholarship.get('advisor_email'):
                self.supervisors[advisor]['email'] = scholarship.get('advisor_email')
            
            if not self.supervisors[advisor]['campus'] and scholarship.get('advisor_campus'):
                self.supervisors[advisor]['campus'] = scholarship.get('advisor_campus')
            
            # Add supervision
            supervision_info = {
                'id': scholarship.get('id', ''),
                'year': scholarship.get('year'),
                'student': scholarship.get('student', ''),
                'student_email': scholarship.get('student_email', ''),
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
            
            self.supervisors[advisor]['ic_supervisions'].append(supervision_info)
            self.supervisors[advisor]['statistics']['total_supervisions'] += 1
            
            # Update statistics
            if scholarship.get('modality') == 'Bolsista':
                self.supervisors[advisor]['statistics']['total_scholarship_holders'] += 1
            elif scholarship.get('modality') == 'Voluntário':
                self.supervisors[advisor]['statistics']['total_volunteers'] += 1
            
            if scholarship.get('year'):
                self.supervisors[advisor]['statistics']['years_active'].add(scholarship.get('year'))
            
            if scholarship.get('program'):
                self.supervisors[advisor]['statistics']['programs'].add(scholarship.get('program'))
            
            if scholarship.get('funding_agency'):
                self.supervisors[advisor]['statistics']['funding_agencies'].add(scholarship.get('funding_agency'))
        
        print(f"✓ Processed supervisions for {len([s for s in self.supervisors.values() if s['ic_supervisions']])} advisors")
    
    def calculate_collaborations(self):
        """
        Calculate collaborations between researchers based on shared projects.
        
        Collaboration is defined as:
        - Coordinator working with researchers on their coordinated projects
        - Researcher working with coordinator on projects they participate in
        - Researchers working together on the same project
        
        For each person, we track:
        - Who they collaborated with
        - How many projects they shared
        - Which projects they worked on together
        - Their role in each collaboration (coordinator or researcher)
        """
        print("\nCalculating collaborations...")
        
        projects = self.projects_data.get('projects', [])
        
        # For each supervisor, find collaborators
        for supervisor_name in self.supervisors.keys():
            collaborators = {}
            
            # Find projects where this supervisor is coordinator
            for project in projects:
                coordinator = project.get('coordinator', '').strip()
                if coordinator == supervisor_name:
                    # Get all researchers on this project
                    researchers = project.get('researchers', [])
                    if isinstance(researchers, list):
                        researchers = [r.strip() for r in researchers if r and r.strip()]
                    else:
                        researchers = []
                    
                    project_id = project.get('id', '')
                    
                    # Add each researcher as a collaborator
                    for researcher in researchers:
                        if researcher and researcher != supervisor_name:
                            if researcher not in collaborators:
                                collaborators[researcher] = {
                                    'count': 0,
                                    'projects': [],
                                    'project_ids': set()  # Track unique project IDs
                                }
                            
                            # Only add if not already added (check by project ID)
                            if project_id not in collaborators[researcher]['project_ids']:
                                collaborators[researcher]['count'] += 1
                                collaborators[researcher]['projects'].append({
                                    'title': project.get('title', ''),
                                    'id': project_id,
                                    'role': 'coordinator'  # supervisor was coordinator
                                })
                                collaborators[researcher]['project_ids'].add(project_id)
            
            # Find projects where this supervisor is a researcher
            for project in projects:
                researchers = project.get('researchers', [])
                if isinstance(researchers, list):
                    researcher_names = [r.strip() for r in researchers if r and r.strip()]
                else:
                    researcher_names = []
                
                if supervisor_name in researcher_names:
                    project_id = project.get('id', '')
                    
                    # Get coordinator
                    coordinator = project.get('coordinator', '').strip()
                    if coordinator and coordinator != supervisor_name:
                        if coordinator not in collaborators:
                            collaborators[coordinator] = {
                                'count': 0,
                                'projects': [],
                                'project_ids': set()
                            }
                        
                        # Only add if not already added
                        if project_id not in collaborators[coordinator]['project_ids']:
                            collaborators[coordinator]['count'] += 1
                            collaborators[coordinator]['projects'].append({
                                'title': project.get('title', ''),
                                'id': project_id,
                                'role': 'researcher'  # supervisor was researcher
                            })
                            collaborators[coordinator]['project_ids'].add(project_id)
                    
                    # Get other researchers on the same project
                    for researcher in researcher_names:
                        if researcher and researcher != supervisor_name:
                            if researcher not in collaborators:
                                collaborators[researcher] = {
                                    'count': 0,
                                    'projects': [],
                                    'project_ids': set()
                                }
                            
                            # Only add if not already added
                            if project_id not in collaborators[researcher]['project_ids']:
                                collaborators[researcher]['count'] += 1
                                collaborators[researcher]['projects'].append({
                                    'title': project.get('title', ''),
                                    'id': project_id,
                                    'role': 'co-researcher'  # both were researchers
                                })
                                collaborators[researcher]['project_ids'].add(project_id)
            
            # Remove project_ids set before storing (not JSON serializable)
            for collab_data in collaborators.values():
                del collab_data['project_ids']
            
            # Store collaborations sorted by count
            self.supervisors[supervisor_name]['collaborations'] = dict(
                sorted(collaborators.items(), key=lambda x: x[1]['count'], reverse=True)
            )
        
        # Count supervisors with collaborations
        with_collabs = len([s for s in self.supervisors.values() if s['collaborations']])
        print(f"✓ Calculated collaborations for {with_collabs} supervisors with collaborators")
    
    def finalize_statistics(self):
        """Convert sets to sorted lists in statistics."""
        for supervisor_data in self.supervisors.values():
            stats = supervisor_data['statistics']
            stats['years_active'] = sorted(list(stats['years_active']))
            stats['programs'] = sorted(list(stats['programs']))
            stats['funding_agencies'] = sorted(list(stats['funding_agencies']))
            
            # Calculate year range
            if stats['years_active']:
                stats['year_range'] = {
                    'min': min(stats['years_active']),
                    'max': max(stats['years_active'])
                }
            else:
                stats['year_range'] = None
            
            # Add collaboration statistics
            if 'collaborations' in supervisor_data:
                stats['total_collaborators'] = len(supervisor_data['collaborations'])
                if supervisor_data['collaborations']:
                    total_collab_projects = sum(c['count'] for c in supervisor_data['collaborations'].values())
                    stats['total_collaborations'] = total_collab_projects
                else:
                    stats['total_collaborations'] = 0
            else:
                stats['total_collaborators'] = 0
                stats['total_collaborations'] = 0
    
    def generate_output(self) -> Dict[str, Any]:
        """Generate output data structure."""
        # Convert defaultdict to regular dict and sort by name
        supervisors_list = []
        
        for name, data in sorted(self.supervisors.items()):
            supervisor_entry = {
                'name': data['name'],
                'email': data['email'],
                'campus': data['campus'],
                'statistics': data['statistics'],
                'research_projects': sorted(data['research_projects'], 
                                           key=lambda x: x.get('start_date', ''), 
                                           reverse=True),
                'ic_supervisions': sorted(data['ic_supervisions'], 
                                         key=lambda x: x.get('year', 0), 
                                         reverse=True),
                'collaborations': data.get('collaborations', {})
            }
            supervisors_list.append(supervisor_entry)
        
        # Generate summary statistics
        total_supervisors = len(supervisors_list)
        supervisors_with_projects = len([s for s in supervisors_list if s['research_projects']])
        supervisors_with_supervisions = len([s for s in supervisors_list if s['ic_supervisions']])
        supervisors_with_both = len([s for s in supervisors_list 
                                    if s['research_projects'] and s['ic_supervisions']])
        supervisors_with_collaborations = len([s for s in supervisors_list if s['collaborations']])
        
        # Calculate collaboration network statistics
        total_collaborations = sum(len(s['collaborations']) for s in supervisors_list)
        total_collaboration_instances = sum(
            sum(c['count'] for c in s['collaborations'].values()) 
            for s in supervisors_list
        )
        
        output = {
            'metadata': {
                'generated_at': self._get_timestamp(),
                'total_supervisors': total_supervisors,
                'supervisors_with_projects': supervisors_with_projects,
                'supervisors_with_supervisions': supervisors_with_supervisions,
                'supervisors_with_both': supervisors_with_both,
                'supervisors_with_collaborations': supervisors_with_collaborations,
                'total_unique_collaborations': total_collaborations,
                'total_collaboration_instances': total_collaboration_instances,
                'sources': {
                    'projects': str(self.projects_file),
                    'scholarships': str(self.scholarships_file)
                }
            },
            'supervisors': supervisors_list
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
        print("SUPERVISOR DATA AGGREGATION SUMMARY")
        print("=" * 80)
        print(f"Total supervisors: {metadata['total_supervisors']}")
        print(f"  With research projects: {metadata['supervisors_with_projects']}")
        print(f"  With IC supervisions: {metadata['supervisors_with_supervisions']}")
        print(f"  With both: {metadata['supervisors_with_both']}")
        print(f"  With collaborations: {metadata['supervisors_with_collaborations']}")
        
        print(f"\nCollaboration Network:")
        print(f"  Total unique collaborations: {metadata['total_unique_collaborations']}")
        print(f"  Total collaboration instances: {metadata['total_collaboration_instances']}")
        
        # Top supervisors by projects
        top_by_projects = sorted(data['supervisors'], 
                                key=lambda x: x['statistics']['total_projects'], 
                                reverse=True)[:5]
        
        print("\nTop 5 supervisors by research projects:")
        for i, sup in enumerate(top_by_projects, 1):
            print(f"  {i}. {sup['name']}: {sup['statistics']['total_projects']} projects")
        
        # Top supervisors by supervisions
        top_by_supervisions = sorted(data['supervisors'], 
                                     key=lambda x: x['statistics']['total_supervisions'], 
                                     reverse=True)[:5]
        
        print("\nTop 5 supervisors by IC supervisions:")
        for i, sup in enumerate(top_by_supervisions, 1):
            print(f"  {i}. {sup['name']}: {sup['statistics']['total_supervisions']} supervisions")
        
        # Top supervisors by collaborations
        top_by_collaborations = sorted(data['supervisors'], 
                                      key=lambda x: x['statistics'].get('total_collaborators', 0), 
                                      reverse=True)[:5]
        
        print("\nTop 5 supervisors by number of collaborators:")
        for i, sup in enumerate(top_by_collaborations, 1):
            collab_count = sup['statistics'].get('total_collaborators', 0)
            collab_instances = sup['statistics'].get('total_collaborations', 0)
            print(f"  {i}. {sup['name']}: {collab_count} collaborators ({collab_instances} projects)")
        
        print("=" * 80)


def main():
    """Main execution function."""
    print("=" * 80)
    print("GROUP BY SUPERVISOR - Research Projects & IC Supervisions")
    print("=" * 80)
    
    # Configuration
    projects_file = Path('data/research_projects.json')
    scholarships_file = Path('data/scholarships.json')
    output_file = Path('data/supervisors.json')
    
    # Check input files
    if not projects_file.exists():
        print(f"\n✗ Error: {projects_file} not found")
        return
    
    if not scholarships_file.exists():
        print(f"\n✗ Error: {scholarships_file} not found")
        return
    
    # Process data
    aggregator = SupervisorDataAggregator(projects_file, scholarships_file)
    
    aggregator.load_data()
    aggregator.process_research_projects()
    aggregator.process_ic_supervisions()
    aggregator.calculate_collaborations()
    aggregator.finalize_statistics()
    
    output_data = aggregator.generate_output()
    
    aggregator.save_output(output_file, output_data)
    aggregator.print_summary(output_data)
    
    print(f"\n✓ Supervisor data saved to: {output_file}")


if __name__ == '__main__':
    main()
