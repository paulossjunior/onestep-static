# Research Documentation Portal - Campus Serra

A comprehensive documentation portal for research activities at IFES Campus Serra, featuring interactive visualizations, collaboration networks, and detailed project analytics.

## 🎯 Overview

This project automatically generates a static documentation website from research data extracted from SIGPESQ (Sistema de Gestão de Pesquisa do IFES). It provides:

- **Research Groups**: Group-centric view with collaboration networks
- **Research Projects**: Project-centric view with timeline analytics
- **Interactive Visualizations**: Charts, graphs, and network diagrams
- **Collaboration Analysis**: Network metrics and partnership insights
- **Student Engagement**: Participation patterns and highly engaged students

## 🚀 Features

### Data Processing
- ✅ CSV to JSON conversion with validation
- ✅ Automatic duplicate removal
- ✅ Missing research group detection
- ✅ Network statistics generation
- ✅ Object-oriented, well-documented code

### Visualizations
- 📊 **Timeline Charts**: Projects and students over time
- 🔗 **Network Graphs**: Collaboration relationships
- 📈 **Bar Charts**: Student participation distribution
- 🎯 **Status Tracking**: Ongoing vs completed projects
- 📉 **Trend Analysis**: Funding and partnership patterns

### Documentation
- 📚 Organized by research groups and projects
- 🔍 Searchable and filterable content
- 📱 Responsive design
- 🌐 Interactive charts with Plotly and vis-network
- 📋 Expandable detailed tables
- 🌍 Multilingual support (English and Portuguese)

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy-pages.yml      # GitHub Actions CI/CD
│
├── source/                       # Source CSV files from SIGPESQ
│   ├── research_groups/
│   │   └── research_group.csv
│   ├── research_project/
│   │   └── *.csv                 # Multiple CSV files by year
│   └── scholarships/
│       └── *.csv                 # Scholarship data by year
│
├── src/                          # Python processing scripts (OOP)
│   ├── process_research_groups.py      # Convert groups CSV to JSON
│   ├── process_research_projects.py    # Convert projects CSV to JSON
│   ├── process_scholarships.py         # Convert scholarships CSV to JSON
│   ├── calculate_student_recurrence.py # Calculate student statistics
│   ├── group_by_student.py             # Aggregate by student
│   ├── group_by_supervisor.py          # Aggregate by supervisor
│   ├── analyze_partnerships.py         # Analyze partnerships
│   ├── generate_network_stats.py       # Generate collaboration networks
│   ├── translate_docs.py               # Translate documentation
│   ├── remove_pii_columns.py           # Remove PII from CSV
│   ├── remove_cpf_from_json.py         # Remove CPF from JSON
│   ├── build.sh                        # Build script
│   └── README.md                       # Scripts documentation
│
├── data/                         # Generated JSON files
│   ├── research_group.json       # Processed research groups
│   ├── research_projects.json    # Processed research projects
│   ├── scholarships.json         # Processed scholarships
│   ├── students.json             # Student aggregated data
│   ├── supervisors.json          # Supervisor aggregated data
│   ├── partnership_analysis.json # Partnership analysis
│   └── network_stats.json        # Collaboration network statistics
│
├── onestep-static/              # MkDocs documentation
│   ├── mkdocs.yml               # MkDocs configuration
│   ├── main.py                  # MkDocs macros (OOP)
│   ├── overrides/               # Custom templates
│   └── docs/
│       ├── index.md             # Landing page (English)
│       ├── index.pt.md          # Landing page (Portuguese)
│       ├── research_groups.md   # Research groups (English)
│       ├── research_groups.pt.md # Research groups (Portuguese)
│       ├── research_projects.md # Research projects (English)
│       ├── research_projects.pt.md # Research projects (Portuguese)
│       ├── students.md          # Students (English)
│       ├── students.pt.md       # Students (Portuguese)
│       ├── supervisors.md       # Supervisors (English)
│       ├── supervisors.pt.md    # Supervisors (Portuguese)
│       ├── scholarship.md       # Scholarships (English)
│       ├── scholarship.pt.md    # Scholarships (Portuguese)
│       ├── downloads.md         # Data downloads (English)
│       └── downloads.pt.md      # Data downloads (Portuguese)
│
├── docs-projeto/                # Technical documentation
│   ├── MAKEFILE_GUIDE.md        # Makefile usage guide
│   └── *.md                     # Other guides and references
│
├── Makefile                     # Build automation
├── requirements.txt             # Python dependencies
├── main.py                      # MkDocs entry point
├── GUIA_RAPIDO_PT.md           # Quick start guide (Portuguese)
├── GUIA_PUBLICACAO_GITHUB.md   # GitHub Pages deployment guide
├── PUBLICAR_AGORA.md           # Quick publish guide
└── README.md                    # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd onestep-static
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Usage

### Quick Start with Makefile

The project includes a comprehensive Makefile for easy management:

```bash
# Show all available commands
make help

# Install dependencies
make install

# Process all data (complete pipeline)
make process-all

# Build documentation
make build-docs

# Serve documentation locally
make serve-docs
```

### Complete Workflow

```bash
# 1. Install dependencies
make install

# 2. Process all data
make process-all

# 3. Build and serve documentation
make serve-docs
# Open http://127.0.0.1:8000
```

### Individual Processing Steps

```bash
# Process research groups
make process-groups

# Process research projects
make process-projects

# Process scholarships
make process-scholarships

# Calculate student recurrence
make calculate-recurrence

# Aggregate data by student
make aggregate-students

# Aggregate data by supervisor
make aggregate-supervisors

# Analyze partnerships
make analyze-partnerships

# Generate network statistics
make analyze-networks
```

### Documentation Commands

```bash
# Copy data files to docs
make copy-data

# Build static site
make build-docs

# Preview locally (with auto-reload)
make serve-docs
# Open http://127.0.0.1:8000
# The site will be available in both English and Portuguese
# Use the language selector in the top navigation bar

# Translate documentation to Portuguese
make translate-docs
```

### Utility Commands

```bash
# Check status of data files
make status

# Show project information
make info

# Clean generated files
make clean

# Clean data files (⚠️ WARNING: removes processed data)
make clean-data
```

### Code Quality

```bash
# Format code with black
make format

# Run linter
make lint

# Type checking
make type-check

# Run tests
make test
```

### Deploy to GitHub Pages

**Automatic deployment:**
- Push changes to `main` branch
- GitHub Actions will automatically build and deploy

**Manual deployment:**
```bash
# Prepare for deployment
make deploy

# Then follow the git commands shown
git add .
git commit -m "Update data and documentation"
git push origin main
```

**Manual workflow trigger:**
- Go to Actions tab in GitHub
- Select "Deploy to GitHub Pages"
- Click "Run workflow"

### Alternative: Direct Python Commands

If you prefer not to use Make:

```bash
# Process data
python src/process_research_groups.py
python src/process_research_projects.py
python src/process_scholarships.py
python src/calculate_student_recurrence.py
python src/group_by_student.py
python src/group_by_supervisor.py
python src/analyze_partnerships.py
python src/generate_network_stats.py

# Build documentation
cd onestep-static
mkdocs build --clean --strict
mkdocs serve
```

## 🏗️ Architecture

### Data Flow

```
CSV Files (SIGPESQ)
    ↓
Python Scripts (OOP)
    ↓
JSON Files (Structured Data)
    ↓
MkDocs + Jinja2 Templates
    ↓
Static HTML Site
    ↓
GitHub Pages (Published)
```

### Key Components

#### 1. Data Processing Layer
- **Object-Oriented Design**: Classes for Person, Edge, Network, etc.
- **Type Safety**: Comprehensive type hints
- **Validation**: Duplicate removal, data normalization
- **Documentation**: Full docstrings and comments

#### 2. Visualization Layer
- **Plotly**: Interactive charts and graphs
- **vis-network**: Collaboration network diagrams
- **Jinja2**: Dynamic content generation
- **Responsive**: Mobile-friendly layouts

#### 3. Deployment Layer
- **GitHub Actions**: Automated CI/CD
- **MkDocs**: Static site generation
- **GitHub Pages**: Free hosting

## 📈 Data Sources

All data is extracted from **SIGPESQ** (Sistema de Gestão de Pesquisa do IFES), the official research management system of the Federal Institute of Espírito Santo.

### Data Scope
- **Campus**: Serra only
- **Time Period**: 2014 - 2025
- **Total Projects**: 579+
- **Research Groups**: 14 active groups
- **Students**: 400+ unique students

## 🔧 Development

### Code Quality

The codebase follows best practices:
- ✅ Object-Oriented Programming
- ✅ Type hints throughout
- ✅ Comprehensive documentation
- ✅ Single Responsibility Principle
- ✅ DRY (Don't Repeat Yourself)

### Testing

```bash
# Test data processing
python src/process_research_groups.py
python src/process_research_projects.py
python src/generate_network_stats.py

# Test documentation build
mkdocs build --strict

# Test locally
mkdocs serve
```

### Adding New Features

1. **New visualization**: Edit markdown files in `onestep-static/docs/`
2. **New metric**: Modify Python scripts in `src/`
3. **New data source**: Add CSV files to `source/`
4. **New page**: Add markdown file and update `mkdocs.yml`

## 📚 Documentation

### For Users
- **Landing Page**: Overview and navigation guide (English and Portuguese)
- **Research Groups**: Group-centric view with networks
- **Research Projects**: Project-centric view with analytics
- **Students**: Student participation and collaboration
- **Supervisors**: Supervisor profiles and statistics
- **Scholarships**: IC scholarship data and analysis
- **Downloads**: Access to all data files in JSON format
- **Language Selector**: Switch between English and Portuguese

### For Developers
- **Makefile Guide**: `docs-projeto/MAKEFILE_GUIDE.md` - Complete Makefile documentation
- **Quick Start**: `GUIA_RAPIDO_PT.md` - Quick start guide in Portuguese
- **Deployment**: `GUIA_PUBLICACAO_GITHUB.md` - Complete GitHub Pages guide
- **Quick Publish**: `PUBLICAR_AGORA.md` - Fast deployment guide
- **Scripts Documentation**: `src/README.md` - All Python scripts documented
- **Technical Docs**: `docs-projeto/` - Detailed technical documentation
- **Code Documentation**: Comprehensive docstrings in all Python files

## 🤝 Contributing

### Workflow

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** locally
5. **Commit** with clear messages
6. **Push** to your fork
7. **Create** a Pull Request

### Guidelines

- Follow existing code style
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting
- Keep commits focused and atomic

## 📝 License

[Add your license information here]

## 👥 Authors

- IFES Campus Serra Research Team

## 🙏 Acknowledgments

- **SIGPESQ**: Data source
- **IFES**: Federal Institute of Espírito Santo
- **MkDocs**: Documentation framework
- **Plotly**: Visualization library
- **vis-network**: Network visualization

## 📞 Contact

For questions or support, contact the research coordination at IFES Campus Serra.

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: ✅ Active
