#!/usr/bin/env python3
"""
Object-Oriented script to generate network statistics for research groups.

This module analyzes collaboration networks within research groups by:
- Tracking people (coordinators, researchers, students) and their connections
- Calculating network metrics (centrality, collaboration strength)
- Generating graph representations for visualization

Input: data/research_projects.json, data/research_group.json
Output: data/network_stats.json
"""

import json
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Person:
    """Represents a person in the research network."""
    
    name: str
    role: str  # 'coordinator', 'researcher', or 'student'
    connections: Set[str] = field(default_factory=set)
    projects: List[str] = field(default_factory=list)
    
    def add_connection(self, other_person: str) -> None:
        """Add a connection to another person."""
        self.connections.add(other_person)
    
    def add_project(self, project_title: str) -> None:
        """Add a project this person is involved in."""
        if project_title not in self.projects:
            self.projects.append(project_title)
    
    @property
    def connection_count(self) -> int:
        """Get the number of connections this person has."""
        return len(self.connections)


@dataclass
class Edge:
    """Represents a collaboration edge between two people."""
    
    person1: str
    person2: str
    collaboration_count: int = 0
    projects: List[str] = field(default_factory=list)
    
    def add_collaboration(self, project_title: str) -> None:
        """Record a collaboration on a project."""
        self.collaboration_count += 1
        if project_title not in self.projects:
            self.projects.append(project_title)
    
    @property
    def edge_key(self) -> Tuple[str, str]:
        """Get a sorted tuple key for this edge."""
        return tuple(sorted([self.person1, self.person2]))


class CollaborationNetwork:
    """Manages the collaboration network for a research group."""
    
    def __init__(self):
        """Initialize an empty collaboration network."""
        self.people: Dict[str, Person] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
    
    def add_person(self, name: str, role: str) -> Person:
        """
        Add a person to the network or return existing person.
        
        Args:
            name: Person's name
            role: Person's role (coordinator, researcher, student)
            
        Returns:
            Person object
        """
        if name not in self.people:
            self.people[name] = Person(name=name, role=role)
        return self.people[name]
    
    def add_edge(self, person1: str, person2: str, project_title: str) -> None:
        """
        Add or update an edge between two people.
        
        Args:
            person1: First person's name
            person2: Second person's name
            project_title: Project they collaborated on
        """
        edge_key = tuple(sorted([person1, person2]))
        
        if edge_key not in self.edges:
            self.edges[edge_key] = Edge(person1=person1, person2=person2)
        
        self.edges[edge_key].add_collaboration(project_title)
        
        # Update connections for both people
        self.people[person1].add_connection(person2)
        self.people[person2].add_connection(person1)
    
    def process_project(self, project: Dict) -> None:
        """
        Process a project and add all people and connections to the network.
        
        Args:
            project: Project dictionary with coordinator, researchers, students
        """
        project_title = project.get('title', '').strip()
        coordinator = project.get('coordinator', '').strip()
        researchers = [r.strip() for r in project.get('researchers', []) if r.strip()]
        students = [s.strip() for s in project.get('students', []) if s.strip()]
        
        # Add coordinator
        if coordinator:
            person = self.add_person(coordinator, 'coordinator')
            person.add_project(project_title)
        
        # Add researchers
        for researcher in researchers:
            person = self.add_person(researcher, 'researcher')
            person.add_project(project_title)
        
        # Add students
        for student in students:
            person = self.add_person(student, 'student')
            person.add_project(project_title)
        
        # Create edges: coordinator <-> researchers
        if coordinator:
            for researcher in researchers:
                self.add_edge(coordinator, researcher, project_title)
        
        # Create edges: coordinator <-> students
        if coordinator:
            for student in students:
                self.add_edge(coordinator, student, project_title)
        
        # Create edges: researchers <-> students
        for researcher in researchers:
            for student in students:
                self.add_edge(researcher, student, project_title)
    
    def get_most_connected_person(self) -> Optional[Tuple[str, int]]:
        """
        Find the person with the most connections.
        
        Returns:
            Tuple of (person_name, connection_count) or None if network is empty
        """
        if not self.people:
            return None
        
        most_connected = max(
            self.people.items(),
            key=lambda item: item[1].connection_count
        )
        return (most_connected[0], most_connected[1].connection_count)
    
    def get_strongest_collaboration(self) -> Optional[Tuple[List[str], int]]:
        """
        Find the strongest collaboration (most projects together).
        
        Returns:
            Tuple of ([person1, person2], project_count) or None if no edges
        """
        if not self.edges:
            return None
        
        strongest = max(
            self.edges.items(),
            key=lambda item: item[1].collaboration_count
        )
        return (list(strongest[0]), strongest[1].collaboration_count)
    
    def get_statistics(self) -> Dict:
        """
        Calculate and return network statistics.
        
        Returns:
            Dictionary with network metrics and graph representation
        """
        total_people = len(self.people)
        total_edges = len(self.edges)
        
        # Count by role
        role_counts = defaultdict(int)
        for person in self.people.values():
            role_counts[person.role] += 1
        
        # Calculate average connections
        total_connections = sum(p.connection_count for p in self.people.values())
        avg_connections = total_connections / total_people if total_people > 0 else 0
        
        # Get most connected person
        most_connected = self.get_most_connected_person()
        
        # Get strongest collaboration
        strongest_collab = self.get_strongest_collaboration()
        
        # Build graph representation
        graph = self._build_graph_representation()
        
        return {
            'total_people': total_people,
            'total_connections': total_edges,
            'coordinators': role_counts['coordinator'],
            'researchers': role_counts['researcher'],
            'students': role_counts['student'],
            'avg_connections_per_person': round(avg_connections, 2),
            'most_connected_person': {
                'name': most_connected[0],
                'connections': most_connected[1]
            } if most_connected else None,
            'strongest_collaboration': {
                'people': strongest_collab[0],
                'projects_together': strongest_collab[1]
            } if strongest_collab else None,
            'graph': graph
        }
    
    def _build_graph_representation(self) -> Dict:
        """
        Build a graph representation suitable for visualization.
        
        Returns:
            Dictionary with 'nodes' and 'edges' lists
        """
        # Build nodes
        nodes = []
        person_to_id = {}
        
        for node_id, (name, person) in enumerate(self.people.items()):
            person_to_id[name] = node_id
            nodes.append({
                'id': node_id,
                'label': name,
                'group': person.role,
                'value': person.connection_count + 1,
                'title': f"{person.role.title()}: {name}",
                'projects': person.projects
            })
        
        # Build edges
        graph_edges = []
        for (person1, person2), edge in self.edges.items():
            graph_edges.append({
                'from': person_to_id[person1],
                'to': person_to_id[person2],
                'value': edge.collaboration_count,
                'title': f"Collaborations: {edge.collaboration_count}",
                'width': min(edge.collaboration_count * 2, 10),
                'projects': edge.projects
            })
        
        return {
            'nodes': nodes,
            'edges': graph_edges
        }


class NetworkStatsGenerator:
    """Main class for generating network statistics from research data."""
    
    def __init__(self, projects_file: str, groups_file: str, output_file: str):
        """
        Initialize the generator with file paths.
        
        Args:
            projects_file: Path to research projects JSON file
            groups_file: Path to research groups JSON file
            output_file: Path to output network statistics JSON file
        """
        self.projects_file = projects_file
        self.groups_file = groups_file
        self.output_file = output_file
        self.all_projects: List[Dict] = []
        self.groups: List[Dict] = []
    
    def load_data(self) -> None:
        """Load research projects and groups from JSON files."""
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            self.all_projects = json.load(f)
        
        with open(self.groups_file, 'r', encoding='utf-8') as f:
            self.groups = json.load(f)
    
    def filter_serra_groups(self) -> List[Dict]:
        """
        Filter groups for Serra campus only.
        
        Returns:
            List of Serra campus groups
        """
        return [g for g in self.groups if g.get('campus', '').lower() == 'serra']
    
    def get_group_projects(self, group_name: str) -> List[Dict]:
        """
        Get unique projects for a specific research group.
        
        Args:
            group_name: Name of the research group
            
        Returns:
            List of unique projects for the group
        """
        # Filter projects for this group
        group_projects = [
            p for p in self.all_projects
            if p.get('campus', '').lower() == 'serra'
            and p.get('research_group', '') == group_name
        ]
        
        # Remove duplicates by ID
        seen_ids = set()
        unique_projects = []
        for project in group_projects:
            proj_id = project.get('id', '')
            if proj_id and proj_id not in seen_ids:
                seen_ids.add(proj_id)
                unique_projects.append(project)
        
        return unique_projects
    
    def generate_statistics(self) -> Dict[str, Dict]:
        """
        Generate network statistics for all Serra campus research groups.
        
        Returns:
            Dictionary mapping group names to their network statistics
        """
        serra_groups = self.filter_serra_groups()
        network_stats = {}
        
        for group in serra_groups:
            group_name = group.get('name', '')
            if not group_name:
                continue
            
            print(f"Processing: {group_name}")
            
            # Get projects for this group
            group_projects = self.get_group_projects(group_name)
            
            if group_projects:
                # Create network and process projects
                network = CollaborationNetwork()
                for project in group_projects:
                    network.process_project(project)
                
                # Get statistics
                stats = network.get_statistics()
                network_stats[group_name] = stats
                
                print(f"  - {stats['total_people']} people, "
                      f"{stats['total_connections']} connections")
        
        return network_stats
    
    def save_statistics(self, network_stats: Dict[str, Dict]) -> None:
        """
        Save network statistics to JSON file.
        
        Args:
            network_stats: Dictionary of network statistics by group
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(network_stats, f, ensure_ascii=False, indent=2)
        
        print(f"\nSuccessfully generated network statistics for "
              f"{len(network_stats)} groups")
        print(f"Output written to: {self.output_file}")
    
    def run(self) -> None:
        """Execute the complete network statistics generation process."""
        self.load_data()
        network_stats = self.generate_statistics()
        self.save_statistics(network_stats)


def main():
    """Main entry point for the script."""
    generator = NetworkStatsGenerator(
        projects_file='data/research_projects.json',
        groups_file='data/research_group.json',
        output_file='data/network_stats.json'
    )
    generator.run()


if __name__ == '__main__':
    main()
