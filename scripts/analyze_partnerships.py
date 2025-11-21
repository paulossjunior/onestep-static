#!/usr/bin/env python3
"""
Partnership and External Research Group Analyzer
Analyzes research projects to identify top partners and external research groups.
"""

import json
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Dict
from pathlib import Path


@dataclass
class PartnershipStats:
    """Statistics for a partner or external research group."""
    name: str
    project_count: int
    percentage: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PartnershipAnalysis:
    """Complete analysis of partnerships and external collaborations."""
    total_projects: int
    partners: List[PartnershipStats]
    external_research_groups: List[PartnershipStats]
    projects_with_partners: int
    projects_with_external_groups: int
    unique_partners_count: int
    unique_external_groups_count: int
    
    def to_dict(self) -> Dict:
        return {
            'total_projects': self.total_projects,
            'partners': [p.to_dict() for p in self.partners],
            'external_research_groups': [g.to_dict() for g in self.external_research_groups],
            'projects_with_partners': self.projects_with_partners,
            'projects_with_external_groups': self.projects_with_external_groups,
            'unique_partners_count': self.unique_partners_count,
            'unique_external_groups_count': self.unique_external_groups_count,
            'partners_percentage': round(self.projects_with_partners / self.total_projects * 100, 2) if self.total_projects > 0 else 0,
            'external_groups_percentage': round(self.projects_with_external_groups / self.total_projects * 100, 2) if self.total_projects > 0 else 0
        }


class ProjectDataLoader:
    """Loads and filters project data."""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.projects = []
    
    def load(self, campus: str = 'Serra') -> List[Dict]:
        """Load projects from JSON file and filter by campus."""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.projects = [p for p in data if p.get('campus') == campus]
        return self.projects


class PartnershipAnalyzer:
    """Analyzes partnerships and external research groups from project data."""
    
    def __init__(self, projects: List[Dict]):
        self.projects = projects
        self.partners = []
        self.external_groups = []
    
    def extract_partnerships(self) -> None:
        """Extract partners and external research groups from projects."""
        for project in self.projects:
            # Extract partner
            partner = project.get('partner', '').strip()
            if partner:
                self.partners.append(partner)
            
            # Extract external research group
            ext_group = project.get('external_research_group', '').strip()
            if ext_group:
                self.external_groups.append(ext_group)
    
    def analyze(self, top_n: int = 20) -> PartnershipAnalysis:
        """Analyze partnerships and return statistics."""
        self.extract_partnerships()
        
        # Count occurrences
        partner_counts = Counter(self.partners)
        ext_group_counts = Counter(self.external_groups)
        
        total_projects = len(self.projects)
        
        # Create partner stats
        partner_stats = [
            PartnershipStats(
                name=name,
                project_count=count,
                percentage=round(count / total_projects * 100, 2)
            )
            for name, count in partner_counts.most_common(top_n)
        ]
        
        # Create external group stats
        ext_group_stats = [
            PartnershipStats(
                name=name,
                project_count=count,
                percentage=round(count / total_projects * 100, 2)
            )
            for name, count in ext_group_counts.most_common(top_n)
        ]
        
        return PartnershipAnalysis(
            total_projects=total_projects,
            partners=partner_stats,
            external_research_groups=ext_group_stats,
            projects_with_partners=len(self.partners),
            projects_with_external_groups=len(self.external_groups),
            unique_partners_count=len(partner_counts),
            unique_external_groups_count=len(ext_group_counts)
        )


class AnalysisExporter:
    """Exports analysis results to JSON file."""
    
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
    
    def export(self, analysis: PartnershipAnalysis) -> None:
        """Export analysis to JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"✓ Analysis exported to: {self.output_path}")


def main():
    """Main execution function."""
    # Configuration
    DATA_PATH = 'data/research_projects.json'
    OUTPUT_PATH = 'data/partnership_analysis.json'
    CAMPUS = 'Serra'
    TOP_N = 20
    
    print("=" * 80)
    print("PARTNERSHIP AND EXTERNAL RESEARCH GROUP ANALYSIS")
    print("=" * 80)
    
    # Load data
    print(f"\n1. Loading data from {DATA_PATH}...")
    loader = ProjectDataLoader(DATA_PATH)
    projects = loader.load(campus=CAMPUS)
    print(f"   ✓ Loaded {len(projects)} projects from {CAMPUS} campus")
    
    # Analyze
    print(f"\n2. Analyzing partnerships and external research groups...")
    analyzer = PartnershipAnalyzer(projects)
    analysis = analyzer.analyze(top_n=TOP_N)
    
    # Print summary
    print(f"\n3. Analysis Summary:")
    print(f"   • Total projects: {analysis.total_projects}")
    print(f"   • Projects with partners: {analysis.projects_with_partners} ({analysis.to_dict()['partners_percentage']}%)")
    print(f"   • Unique partners: {analysis.unique_partners_count}")
    print(f"   • Projects with external groups: {analysis.projects_with_external_groups} ({analysis.to_dict()['external_groups_percentage']}%)")
    print(f"   • Unique external groups: {analysis.unique_external_groups_count}")
    
    print(f"\n4. Top {min(5, len(analysis.partners))} Partners:")
    for i, partner in enumerate(analysis.partners[:5], 1):
        print(f"   {i}. {partner.name} - {partner.project_count} projects ({partner.percentage}%)")
    
    print(f"\n5. Top {min(5, len(analysis.external_research_groups))} External Research Groups:")
    for i, group in enumerate(analysis.external_research_groups[:5], 1):
        print(f"   {i}. {group.name} - {group.project_count} projects ({group.percentage}%)")
    
    # Export
    print(f"\n6. Exporting results...")
    exporter = AnalysisExporter(OUTPUT_PATH)
    exporter.export(analysis)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
