#!/usr/bin/env python3
"""
Scholarship Data Processor
Processes scholarship CSV files and generates consolidated JSON output.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Scholarship:
    """Represents a scholarship record."""
    id: str
    year: int
    management: str
    modality: str
    program: str
    value: Optional[float]
    start_date: str
    end_date: str
    funding_agency: str
    advisor_accepted: str
    advisor_accepted_date: str
    student_accepted: str
    student_accepted_date: str
    cancelled: str
    cancelled_by: str
    aware: str
    report_evaluation: str
    execution_campus: str
    advisor: str
    advisor_email: str
    advisor_campus: str
    student: str
    student_email: str
    course: str
    campus: str
    notice: str
    project_code: str
    project_title: str
    research_project_code: str
    research_project_title: str
    knowledge_area: str
    grade_area: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class ScholarshipCSVReader:
    """Reads scholarship data from CSV files."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.year = self._extract_year_from_filename()
    
    def _extract_year_from_filename(self) -> int:
        """Extract year from filename."""
        filename = self.file_path.name
        # Extract year from pattern: Relatorio_orientacoes_YYYY.xlsx
        try:
            year_str = filename.split('_')[2].split('.')[0]
            return int(year_str)
        except (IndexError, ValueError):
            return 0
    
    def _parse_value(self, value_str: str) -> Optional[float]:
        """Parse monetary value from string."""
        if not value_str or value_str.strip() == '':
            return None
        try:
            # Remove currency symbols and convert
            cleaned = value_str.replace('R$', '').replace(',', '.').strip()
            return float(cleaned)
        except ValueError:
            return None
    
    def read(self) -> List[Scholarship]:
        """Read scholarships from CSV file."""
        scholarships = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        scholarship = Scholarship(
                            id=row.get('Id', ''),
                            year=int(row.get('Ano', self.year)),
                            management=row.get('Gerenciamento', ''),
                            modality=row.get('Modalidade', ''),
                            program=row.get('Programa', ''),
                            value=self._parse_value(row.get('Valor', '')),
                            start_date=row.get('Inicio', ''),
                            end_date=row.get('Fim', ''),
                            funding_agency=row.get('AgFinanciadora', ''),
                            advisor_accepted=row.get('AceiteOrientador', ''),
                            advisor_accepted_date=row.get('AceiteOrientadorData', ''),
                            student_accepted=row.get('AceiteOrientado', ''),
                            student_accepted_date=row.get('AceiteOrientadoData', ''),
                            cancelled=row.get('Cancelado', ''),
                            cancelled_by=row.get('CanceladoPor', ''),
                            aware=row.get('Ciente', ''),
                            report_evaluation=row.get('AvaliacaoRelatorio', ''),
                            execution_campus=row.get('CampusExecucao', ''),
                            advisor=row.get('Orientador', ''),
                            advisor_email=row.get('OrientadorEmail', ''),
                            advisor_campus=row.get('CampusOrientador', ''),
                            student=row.get('Orientado', ''),
                            student_email=row.get('OrientadoEmail', ''),
                            course=row.get('Curso', ''),
                            campus=row.get('Campus', ''),
                            notice=row.get('Edital', ''),
                            project_code=row.get('CodPT', ''),
                            project_title=row.get('TituloPT', ''),
                            research_project_code=row.get('CodPJ', ''),
                            research_project_title=row.get('TituloPJ', ''),
                            knowledge_area=row.get('AreaConhecimento', ''),
                            grade_area=row.get('GradeArea', '')
                        )
                        scholarships.append(scholarship)
                    except Exception as e:
                        print(f"  ⚠ Error parsing row in {self.file_path.name}: {e}")
                        continue
        
        except Exception as e:
            print(f"  ✗ Error reading {self.file_path.name}: {e}")
            return []
        
        return scholarships


class ScholarshipProcessor:
    """Processes multiple scholarship CSV files."""
    
    def __init__(self, source_directory: Path):
        self.source_directory = source_directory
        self.scholarships: List[Scholarship] = []
    
    def process_all_files(self) -> None:
        """Process all CSV files in the source directory."""
        csv_files = sorted(self.source_directory.glob("*.csv"))
        
        if not csv_files:
            print(f"No CSV files found in {self.source_directory}")
            return
        
        print(f"\nFound {len(csv_files)} CSV file(s) to process\n")
        
        seen_ids = set()
        
        for csv_file in csv_files:
            print(f"Processing: {csv_file.name}")
            reader = ScholarshipCSVReader(csv_file)
            scholarships = reader.read()
            
            if scholarships:
                # Remove duplicates by ID
                unique_scholarships = []
                duplicates = 0
                
                for s in scholarships:
                    if s.id not in seen_ids:
                        seen_ids.add(s.id)
                        unique_scholarships.append(s)
                    else:
                        duplicates += 1
                
                self.scholarships.extend(unique_scholarships)
                print(f"  ✓ Loaded {len(unique_scholarships)} scholarship(s)")
                if duplicates > 0:
                    print(f"  ⚠ Skipped {duplicates} duplicate(s)")
            else:
                print(f"  ℹ No scholarships loaded")
            print()
    
    def get_statistics(self) -> Dict:
        """Generate statistics about the scholarships."""
        if not self.scholarships:
            return {}
        
        # Count by year
        by_year = {}
        for s in self.scholarships:
            year = s.year
            by_year[year] = by_year.get(year, 0) + 1
        
        # Count by campus
        by_campus = {}
        for s in self.scholarships:
            campus = s.campus
            if campus:
                by_campus[campus] = by_campus.get(campus, 0) + 1
        
        # Count by modality
        by_modality = {}
        for s in self.scholarships:
            modality = s.modality
            if modality:
                by_modality[modality] = by_modality.get(modality, 0) + 1
        
        # Count by program
        by_program = {}
        for s in self.scholarships:
            program = s.program
            if program:
                by_program[program] = by_program.get(program, 0) + 1
        
        # Calculate total value
        total_value = sum(s.value for s in self.scholarships if s.value is not None)
        
        return {
            'total_scholarships': len(self.scholarships),
            'by_year': dict(sorted(by_year.items())),
            'by_campus': dict(sorted(by_campus.items())),
            'by_modality': dict(sorted(by_modality.items())),
            'by_program': dict(sorted(by_program.items())),
            'total_value': round(total_value, 2),
            'years_range': {
                'min': min(by_year.keys()) if by_year else None,
                'max': max(by_year.keys()) if by_year else None
            }
        }


class ScholarshipJSONExporter:
    """Exports scholarship data to JSON file."""
    
    def __init__(self, output_path: Path):
        self.output_path = output_path
    
    def export(self, scholarships: List[Scholarship], statistics: Dict) -> None:
        """Export scholarships and statistics to JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_records': len(scholarships),
                'source': 'SIGPESQ - Sistema de Gestão de Pesquisa do IFES'
            },
            'statistics': statistics,
            'scholarships': [s.to_dict() for s in scholarships]
        }
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Data exported to: {self.output_path}")
        print(f"  • Total scholarships: {len(scholarships)}")
        print(f"  • File size: {self.output_path.stat().st_size / 1024:.2f} KB")


def main():
    """Main execution function."""
    print("=" * 80)
    print("SCHOLARSHIP DATA PROCESSOR")
    print("=" * 80)
    
    # Configuration
    SOURCE_DIR = Path("source/scholarships")
    OUTPUT_FILE = Path("data/scholarships.json")
    
    print(f"\nSource directory: {SOURCE_DIR}")
    print(f"Output file: {OUTPUT_FILE}")
    
    if not SOURCE_DIR.exists():
        print(f"\n✗ Error: Source directory {SOURCE_DIR} does not exist")
        return
    
    # Process files
    print("\n" + "=" * 80)
    print("STEP 1: PROCESSING CSV FILES")
    print("=" * 80)
    
    processor = ScholarshipProcessor(SOURCE_DIR)
    processor.process_all_files()
    
    if not processor.scholarships:
        print("\n✗ No scholarships were loaded. Exiting.")
        return
    
    # Generate statistics
    print("=" * 80)
    print("STEP 2: GENERATING STATISTICS")
    print("=" * 80)
    
    statistics = processor.get_statistics()
    
    print(f"\n📊 Statistics Summary:")
    print(f"  • Total scholarships: {statistics['total_scholarships']}")
    print(f"  • Years: {statistics['years_range']['min']} - {statistics['years_range']['max']}")
    print(f"  • Campuses: {len(statistics['by_campus'])}")
    print(f"  • Modalities: {len(statistics['by_modality'])}")
    print(f"  • Programs: {len(statistics['by_program'])}")
    print(f"  • Total value: R$ {statistics['total_value']:,.2f}")
    
    print(f"\n📅 Scholarships by Year:")
    for year, count in statistics['by_year'].items():
        print(f"  • {year}: {count}")
    
    # Export to JSON
    print("\n" + "=" * 80)
    print("STEP 3: EXPORTING TO JSON")
    print("=" * 80)
    print()
    
    exporter = ScholarshipJSONExporter(OUTPUT_FILE)
    exporter.export(processor.scholarships, statistics)
    
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
