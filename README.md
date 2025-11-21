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

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── deploy-pages.yml      # GitHub Actions deployment
│       └── README.md             # Workflow documentation
│
├── source/                       # Source CSV files from SIGPESQ
│   ├── research_groups/
│   │   └── research_group.csv
│   └── research_project/
│       └── *.csv                 # Multiple CSV files by year
│
├── src/                          # Python processing scripts
│   ├── process_research_groups.py      # Convert groups CSV to JSON
│   ├── process_research_projects.py    # Convert projects CSV to JSON
│   ├── generate_network_stats.py       # Generate collaboration networks
│   ├── REFACTORING_SUMMARY.md          # Code refactoring details
│   └── REFACTORING_COMPLETE_SUMMARY.md # Complete refactoring overview
│
├── data/                         # Generated JSON files
│   ├── research_group.json       # Processed research groups
│   ├── research_projects.json    # Processed research projects
│   └── network_stats.json        # Collaboration network statistics
│
├── onestep-static/              # MkDocs documentation
│   └── docs/
│       ├── index.md             # Landing page
│       ├── research_groups.md   # Research groups documentation
│       └── research_projects.md # Research projects documentation
│
├── mkdocs.yml                   # MkDocs configuration
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
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

### Process Data

Run the processing scripts in order:

```bash
# 1. Process research groups
python src/process_research_groups.py

# 2. Process research projects
python src/process_research_projects.py

# 3. Generate network statistics
python src/generate_network_stats.py
```

Or run all at once:
```bash
python src/process_research_groups.py && \
python src/process_research_projects.py && \
python src/generate_network_stats.py
```

### Build Documentation

```bash
# Build static site
mkdocs build --clean --strict

# Preview locally
mkdocs serve
# Open http://127.0.0.1:8000
```

### Deploy to GitHub Pages

**Automatic deployment:**
- Push changes to `main` branch
- GitHub Actions will automatically build and deploy

**Manual deployment:**
- Go to Actions tab in GitHub
- Select "Deploy to GitHub Pages"
- Click "Run workflow"

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
- **Landing Page**: Overview and navigation guide
- **Research Groups**: Group-centric view with networks
- **Research Projects**: Project-centric view with analytics

### For Developers
- **Code Documentation**: Docstrings in all Python files
- **Refactoring Summary**: `src/REFACTORING_COMPLETE_SUMMARY.md`
- **Workflow Guide**: `.github/workflows/README.md`
- **This README**: Project overview and setup

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
