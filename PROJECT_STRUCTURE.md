# Project Structure

## Overview

This project contains a MkDocs documentation site with dynamic data loading capabilities.

## Directory Structure

```
.
├── .gitlab-ci.yml              # GitLab CI/CD configuration
├── requirements.txt            # Python dependencies
├── data/                       # JSON data files
│   ├── papers.json            # Research papers data
│   ├── research_lines.json    # Research lines data
│   ├── scholarships.json      # Scholarship data
│   ├── students.json          # Students data
│   ├── supervisors.json       # Supervisors data
│   └── partnership_analysis.json
│
└── onestep-static/            # MkDocs site directory
    ├── mkdocs.yml             # MkDocs configuration
    ├── main.py                # Custom macros for data loading
    ├── docs/                  # Markdown documentation files
    │   ├── index.md
    │   ├── index.pt.md
    │   ├── papers.md
    │   ├── papers.pt.md
    │   ├── research_lines.md
    │   ├── research_lines.pt.md
    │   └── ...
    ├── overrides/             # Theme customizations
    └── site/                  # Generated site (not in git)
```

## Key Components

### 1. Data Files (`data/`)

JSON files containing research data:
- **papers.json**: Publications and citations from Google Scholar
- **research_lines.json**: Research lines with projects and statistics
- **scholarships.json**: Scholarship information
- **students.json**: Student data and participation
- **supervisors.json**: Supervisor information
- **partnership_analysis.json**: Partnership and collaboration data

### 2. MkDocs Site (`onestep-static/`)

The documentation site built with MkDocs:

#### Configuration
- **mkdocs.yml**: Main configuration file
  - Site metadata
  - Navigation structure
  - Theme settings (Material theme)
  - Plugins configuration
  - Internationalization (i18n) settings

#### Custom Macros (`main.py`)
Python module providing custom macros for dynamic content:
- `load_papers_data()`: Load research papers
- `load_research_lines_data()`: Load research lines
- `load_scholarship_data()`: Load scholarships
- `load_students_data()`: Load students
- `load_supervisors_data()`: Load supervisors
- `load_partnership_data()`: Load partnerships
- `get_current_date()`: Get current date

#### Documentation Files (`docs/`)
Markdown files with Jinja2 templates:
- English versions: `*.md`
- Portuguese versions: `*.pt.md`
- Use macros to load and display data dynamically

Example usage in markdown:
```markdown
{% set data = load_papers_data() %}
{% set researchers = data['researchers'] %}

Total Researchers: {{ researchers|length }}
```

### 3. CI/CD Configuration

#### `.gitlab-ci.yml`
Defines the build and deployment pipeline:

**Build Stage:**
1. Install Python dependencies
2. Verify data files exist
3. Build MkDocs site from `onestep-static/`
4. Create artifacts

**Deploy Stage:**
1. Copy built site to `public/` directory
2. Deploy to GitLab Pages

## Data Flow

```
data/*.json
    ↓
main.py (loads data)
    ↓
docs/*.md (uses macros)
    ↓
mkdocs build
    ↓
onestep-static/site/
    ↓
GitLab Pages (public/)
```

## Building Locally

### Prerequisites
```bash
pip install -r requirements.txt
```

### Build Site
```bash
cd onestep-static
mkdocs build
```

### Serve Locally
```bash
cd onestep-static
mkdocs serve
```

Visit: http://127.0.0.1:8000

### Build with Verbose Output
```bash
cd onestep-static
mkdocs build --strict --verbose
```

## Updating Data

1. Update JSON files in `data/` directory
2. Commit changes
3. Push to GitLab
4. CI/CD pipeline automatically rebuilds site

## Adding New Pages

1. Create markdown file in `onestep-static/docs/`
   - English: `newpage.md`
   - Portuguese: `newpage.pt.md`

2. Add to navigation in `onestep-static/mkdocs.yml`:
```yaml
nav:
  - Home:
    - en: index.md
    - pt: index.pt.md
  - New Page:
    - en: newpage.md
    - pt: newpage.pt.md
```

3. Use macros to load data:
```markdown
{% set data = load_papers_data() %}
# My New Page
Total items: {{ data['total_researchers'] }}
```

## Internationalization (i18n)

The site supports multiple languages using `mkdocs-static-i18n`:

- **Default language**: English (`en`)
- **Available languages**: English (`en`), Portuguese (`pt`)
- **Language selector**: Appears in navigation bar

### File Naming Convention
- English: `filename.md`
- Portuguese: `filename.pt.md`

## Theme Customization

The site uses Material for MkDocs theme with customizations:

- **Primary color**: Indigo
- **Accent color**: Indigo
- **Features**: Navigation tabs, instant loading, search
- **Custom overrides**: Located in `onestep-static/overrides/`

## Plugins

Configured in `mkdocs.yml`:

1. **search**: Full-text search functionality
2. **macros**: Custom Python macros (main.py)
3. **i18n**: Internationalization support
4. **table-reader**: Read data from CSV/Excel files

## Troubleshooting

### Build Fails
- Check that all data files exist in `data/`
- Verify JSON files are valid
- Check `main.py` for errors
- Run `mkdocs build --strict --verbose` for detailed errors

### Data Not Loading
- Verify file paths in `main.py`
- Check JSON structure matches expected format
- Ensure files are committed to repository

### Pages Not Updating
- Clear browser cache
- Wait for GitLab Pages to update (can take a few minutes)
- Check pipeline logs for errors

## Performance

### Build Time
- Local build: ~5-10 seconds
- CI/CD build: ~1-2 minutes (with cache)

### Optimization
- Data files are loaded once during build
- Static site generation (no runtime data loading)
- Cached pip packages speed up CI/CD

## Dependencies

Key Python packages:
- `mkdocs==1.6.1`: Static site generator
- `mkdocs-material`: Material theme
- `mkdocs-macros-plugin==1.5.0`: Custom macros
- `mkdocs-static-i18n==1.2.3`: Internationalization
- `mkdocs-table-reader-plugin==3.1.0`: Table reading
- `pandas==2.3.3`: Data manipulation
- `jinja2==3.1.6`: Template engine

See `requirements.txt` for complete list.

## Contributing

1. Create a feature branch
2. Make changes
3. Test locally with `mkdocs serve`
4. Create merge request
5. CI/CD will test build automatically
6. After merge to main, site deploys automatically

## License

[Add your license information here]

## Support

For issues or questions:
- Check this documentation
- Review GitLab CI/CD logs
- Check MkDocs documentation: https://www.mkdocs.org/
- Check Material theme docs: https://squidfunk.github.io/mkdocs-material/
