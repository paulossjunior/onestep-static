# OneStep Scripts

This directory contains scripts for data processing and analysis for the OneStep research observatory.

## Scripts

### `analyze_partnerships.py`

Analyzes research projects to identify and rank partner organizations and external research groups.

**Features:**
- Object-oriented design with clear separation of concerns
- Extracts partnership data from research projects
- Generates statistics and rankings
- Exports results to JSON for consumption by documentation

**Usage:**
```bash
python3 scripts/analyze_partnerships.py
```

**Output:**
- `data/partnership_analysis.json` - Contains:
  - Top 20 partner organizations
  - Top 20 external research groups
  - Statistics (total projects, percentages, unique counts)

**Classes:**
- `ProjectDataLoader` - Loads and filters project data
- `PartnershipAnalyzer` - Analyzes partnerships and external groups
- `AnalysisExporter` - Exports results to JSON
- `PartnershipStats` - Data class for partnership statistics
- `PartnershipAnalysis` - Data class for complete analysis results

### `remove_pii_columns.py`

Removes PII (Personally Identifiable Information) columns from scholarship CSV files for privacy compliance.

**Features:**
- Object-oriented design with CSVColumnRemover class
- Removes phone numbers, CPF, RG, and other personal documents
- Processes all CSV files in scholarships directory
- Preserves all other data and formatting

**Usage:**
```bash
python3 scripts/remove_pii_columns.py
```

**Target Directory:**
- `source/scholarships/` - All CSV files

**Columns Removed:**
- Phone numbers: `CelularOrientado`, `CelularOrientador`, `Celular`, `Telefone`, etc.
- CPF: `CPF`, `CpfOrientado`, `CpfOrientador`, `CPFOrientado`, `CPFOrientador`
- RG: `RG`, `RGOrientado`, `RGOrientador`
- Documents: `Documento`, `DocumentoOrientado`, `DocumentoOrientador`

**Classes:**
- `CSVColumnRemover` - Removes specified columns from CSV files

### `remove_cpf_from_json.py`

Removes CPF and other PII fields from the scholarships JSON file.

**Features:**
- Removes PII fields from all scholarship records
- Preserves all other data
- Updates JSON file in place

**Usage:**
```bash
python3 scripts/remove_cpf_from_json.py
```

**Target File:**
- `data/scholarships.json`

**Fields Removed:**
- `student_cpf`, `advisor_cpf`, `cpf`
- `student_phone`, `advisor_phone`, `phone`
- `student_rg`, `advisor_rg`, `rg`

### `calculate_student_recurrence.py`

Calculates student participation recurrence statistics for IC scholarships.

**Features:**
- Analyzes how many times each student participated in IC programs
- Separates statistics by modality (Bolsista vs Voluntário)
- Identifies student profiles (only bolsista, only voluntário, or mixed)
- Adds statistics to existing JSON file

**Usage:**
```bash
python3 scripts/calculate_student_recurrence.py
```

**Input:**
- `data/scholarships.json`

**Output:**
- Updates `data/scholarships.json` with statistics under `statistics.student_recurrence_serra`

**Statistics Generated:**
- Total unique students
- Student profiles (only bolsista, only voluntário, mixed)
- Participation distribution (1 IC, 2 ICs, 3 ICs, etc.)
- Bolsista distribution
- Voluntário distribution

### `group_by_supervisor.py`

Groups research projects and IC supervisions by supervisor/advisor, creating a comprehensive profile for each researcher.

**Features:**
- Aggregates all research projects coordinated by each researcher
- Aggregates all IC supervisions by each advisor
- Calculates statistics per supervisor (total projects, supervisions, years active, etc.)
- Identifies supervisors with both projects and supervisions
- Sorts data by relevance

**Usage:**
```bash
python3 scripts/group_by_supervisor.py
```

**Input:**
- `data/research_projects.json`
- `data/scholarships.json`

**Output:**
- `data/supervisors.json` - Contains:
  - Metadata (total supervisors, counts by category)
  - Array of supervisors with:
    - Name, email, campus
    - All research projects coordinated
    - All IC supervisions
    - Statistics (totals, years active, programs, funding agencies)

**Statistics Generated per Supervisor:**
- Total research projects
- Total IC supervisions
- Total scholarship holders vs volunteers
- Years active (range and list)
- Programs involved
- Funding agencies

**Use Cases:**
- Generate individual researcher profiles
- Analyze research productivity
- Identify active researchers
- Create supervisor dashboards

### `process_scholarships.py`

Processes scholarship CSV files and generates consolidated JSON output with statistics.

**Features:**
- Object-oriented design with clear separation of concerns
- Reads all scholarship CSV files from source directory
- Parses and validates scholarship data
- Generates comprehensive statistics
- Exports consolidated JSON with metadata
- **Automatically excludes PII fields (CPF, phone numbers, etc.)**

**Usage:**
```bash
python3 scripts/process_scholarships.py
```

**Input:**
- `source/scholarships/*.csv` - Scholarship CSV files (2016-2025)

**Output:**
- `data/scholarships.json` - Contains:
  - Metadata (generation date, total records, source)
  - Statistics (by year, campus, modality, program, total value)
  - Complete scholarship records array (without PII)

**Classes:**
- `Scholarship` - Data class representing a scholarship record
- `ScholarshipCSVReader` - Reads and parses CSV files
- `ScholarshipProcessor` - Processes multiple files and generates statistics
- `ScholarshipJSONExporter` - Exports data to JSON format

**Statistics Generated:**
- Total scholarships count
- Distribution by year (2015-2025)
- Distribution by campus (15 campuses)
- Distribution by modality (2 types)
- Distribution by program (9 programs)
- Total monetary value
- Year range (min/max)

**Privacy Note:**
This script does NOT include PII fields like `student_cpf` in the output JSON.

### `build.sh`

Main build script that orchestrates all data processing and documentation building.

**Usage:**
```bash
./scripts/build.sh
```

**Steps:**
1. Runs partnership analysis
2. Builds MkDocs documentation (if configured)

## Data Flow

```
research_projects.json
        ↓
analyze_partnerships.py
        ↓
partnership_analysis.json
        ↓
research_projects.md / research_projects.pt.md
```

## Adding New Analysis Scripts

When creating new analysis scripts, follow this pattern:

1. Use object-oriented design
2. Load data from `data/` directory
3. Export results to JSON in `data/` directory
4. Update `build.sh` to include your script
5. Consume the JSON in the `.md` files using Jinja2 templates

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
