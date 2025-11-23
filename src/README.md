# Source Code Directory

This directory contains all Python scripts for processing and analyzing research data from Campus Serra.

## Architecture

All Python code follows Object-Oriented Programming (OOP) principles with comprehensive documentation:
- Classes for data models and business logic
- Separation of concerns (data loading, processing, analysis, output)
- Type hints for better code clarity
- Docstrings for all classes, methods, and functions

## Scripts Overview

### Data Processing Scripts

#### `process_research_projects.py`
Converts research project CSV files to structured JSON format.

**Classes:**
- `ResearchProject`: Data model for a research project
- `TextNormalizer`: Text normalization utilities
- `FieldParser`: CSV field parsing logic
- `ResearchGroupManager`: Manages research groups
- `CSVProjectParser`: Parses CSV rows into project objects
- `ResearchProjectProcessor`: Main orchestrator

**Input:** `source/research_project/*.csv`  
**Output:** `data/research_projects.json`  
**Updates:** `data/research_group.json` (adds missing groups)

#### `process_scholarships.py`
Processes IC scholarship CSV files and generates consolidated JSON output.

**Classes:**
- `Scholarship`: Data model for a scholarship record
- `ScholarshipCSVReader`: Reads and parses CSV files
- `ScholarshipProcessor`: Processes multiple CSV files
- `ScholarshipJSONExporter`: Exports to JSON format

**Input:** `source/scholarships/*.csv`  
**Output:** `data/scholarships.json`

#### `process_research_groups.py`
Converts research groups CSV to JSON format with leader parsing.

**Classes:**
- `Leader`: Data model for a group leader
- `ResearchGroup`: Data model for a research group
- `TextNormalizer`: Text normalization utilities
- `LeaderParser`: Parses leader information from CSV
- `ShortNameGenerator`: Generates acronyms from full names
- `ResearchGroupProcessor`: Main orchestrator

**Input:** `source/research_groups/research_group.csv`  
**Output:** `data/research_group.json`

### Data Aggregation Scripts

#### `group_by_student.py`
Aggregates research projects and IC scholarships by student.

**Classes:**
- `StudentDataAggregator`: Main aggregation logic
  - Processes research projects
  - Processes IC scholarships
  - Calculates collaborations
  - Generates statistics

**Input:** `data/research_projects.json`, `data/scholarships.json`  
**Output:** `data/students.json`

**Features:**
- Tracks all projects and scholarships per student
- Identifies advisor relationships
- Calculates student collaboration networks
- Generates comprehensive statistics

#### `group_by_supervisor.py`
Aggregates research projects and IC supervisions by supervisor/advisor.

**Classes:**
- `SupervisorDataAggregator`: Main aggregation logic
  - Processes research projects (coordinators + researchers)
  - Processes IC supervisions
  - Calculates collaborations
  - Generates statistics

**Input:** `data/research_projects.json`, `data/scholarships.json`  
**Output:** `data/supervisors.json`

**Features:**
- Tracks projects coordinated and participated in
- Tracks IC supervisions
- Calculates researcher collaboration networks
- Generates comprehensive statistics

### Analysis Scripts

#### `analyze_partnerships.py`
Analyzes research projects to identify top partners and external research groups.

**Classes:**
- `PartnershipStats`: Statistics for a partner or external group
- `PartnershipAnalysis`: Complete analysis results
- `ProjectDataLoader`: Loads and filters project data
- `PartnershipAnalyzer`: Analyzes partnerships
- `AnalysisExporter`: Exports results to JSON

**Input:** `data/research_projects.json`  
**Output:** `data/partnership_analysis.json`

#### `generate_network_stats.py`
Generates network statistics for research group collaborations.

**Classes:**
- `Person`: Represents a person in the network
- `Edge`: Represents a collaboration edge
- `CollaborationNetwork`: Manages the collaboration network
- `NetworkStatsGenerator`: Main orchestrator

**Input:** `data/research_projects.json`, `data/research_group.json`  
**Output:** `data/network_stats.json`

**Features:**
- Builds collaboration networks for each research group
- Calculates network metrics (centrality, connections)
- Generates graph representations for visualization
- Identifies most connected people and strongest collaborations

#### `calculate_student_recurrence.py`
Calculates student participation recurrence in IC scholarship programs.

**Classes:**
- `StudentParticipation`: Tracks individual student participation
- `ScholarshipFilter`: Filters and deduplicates scholarships
- `RecurrenceAnalyzer`: Analyzes recurrence patterns
- `StatisticsPrinter`: Formats output
- `RecurrenceStatisticsCalculator`: Main orchestrator

**Input:** `data/scholarships.json`  
**Output:** Updates `data/scholarships.json` with statistics

**Features:**
- Tracks how many times each student participated
- Distinguishes between scholarship holder and volunteer
- Calculates participation distributions
- Identifies student profiles (only bolsista, only volunteer, mixed)

### Utility Scripts

#### `translate_docs.py`
Translates English documentation to Portuguese.

**Classes:**
- `TranslationDictionary`: Manages translation mappings
- `DocumentTranslator`: Handles file translation
- `TranslationOrchestrator`: Coordinates translation process

**Input:** `onestep-static/docs/*.pt.md` (Portuguese templates)  
**Output:** Updates Portuguese documentation files

#### `remove_pii_columns.py`
Removes Personally Identifiable Information from CSV files.

**Purpose:** Data privacy and GDPR compliance

#### `remove_cpf_from_json.py`
Removes CPF (Brazilian ID) numbers from JSON files.

**Purpose:** Data privacy and GDPR compliance

### Build Script

#### `build.sh`
Bash script to execute the complete data processing pipeline in the correct order.

**Execution Order:**
1. Process research groups
2. Process research projects
3. Process scholarships
4. Calculate student recurrence
5. Group by student
6. Group by supervisor
7. Analyze partnerships
8. Generate network statistics

## Usage

### Running Individual Scripts

```bash
# Process research projects
python src/process_research_projects.py

# Process scholarships
python src/process_scholarships.py

# Group by student
python src/group_by_student.py

# Group by supervisor
python src/group_by_supervisor.py

# Analyze partnerships
python src/analyze_partnerships.py

# Generate network stats
python src/generate_network_stats.py

# Calculate student recurrence
python src/calculate_student_recurrence.py

# Translate documentation
python src/translate_docs.py
```

### Running Complete Pipeline

```bash
# Execute all scripts in correct order
bash src/build.sh
```

## Code Standards

### Object-Oriented Design
- All functionality encapsulated in classes
- Single Responsibility Principle
- Clear separation of concerns
- Dependency injection where appropriate

### Documentation
- Module-level docstrings explaining purpose
- Class docstrings with attributes and purpose
- Method/function docstrings with Args, Returns, Raises
- Type hints for all parameters and return values

### Data Flow
```
CSV Files (source/)
    ↓
Processing Scripts
    ↓
JSON Files (data/)
    ↓
Aggregation Scripts
    ↓
Enhanced JSON Files (data/)
    ↓
MkDocs Documentation (onestep-static/docs/)
```

## Dependencies

- Python 3.8+
- pandas (for data processing)
- Standard library modules: json, csv, pathlib, collections, dataclasses

## Contributing

When adding new scripts:
1. Follow OOP principles
2. Add comprehensive docstrings
3. Use type hints
4. Update this README
5. Add to build.sh if part of pipeline
