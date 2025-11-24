# IFES Research Data - Documentation Site

[![GitLab CI/CD](https://img.shields.io/badge/CI%2FCD-GitLab-orange)](https://gitlab.com)
[![MkDocs](https://img.shields.io/badge/docs-MkDocs-blue)](https://www.mkdocs.org/)
[![Material Theme](https://img.shields.io/badge/theme-Material-blue)](https://squidfunk.github.io/mkdocs-material/)

Documentation site for IFES Campus Serra research data, including publications, research lines, scholarships, and more.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- GitLab account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Serve locally**
   ```bash
   cd onestep-static
   mkdocs serve
   ```

5. **Open browser**
   ```
   http://127.0.0.1:8000
   ```

## 📁 Project Structure

```
.
├── data/                      # JSON data files
│   ├── papers.json
│   ├── research_lines.json
│   ├── scholarships.json
│   └── ...
│
├── onestep-static/           # MkDocs site
│   ├── mkdocs.yml           # Configuration
│   ├── main.py              # Custom macros
│   ├── docs/                # Markdown files
│   └── overrides/           # Theme customizations
│
├── .gitlab-ci.yml           # CI/CD configuration
├── requirements.txt         # Python dependencies
└── verify_build.sh          # Build verification script
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed information.

## 🔧 Building the Site

### Build Locally

```bash
cd onestep-static
mkdocs build
```

Output will be in `onestep-static/site/`

### Build with Strict Mode

```bash
cd onestep-static
mkdocs build --strict --verbose
```

This will fail on warnings and show detailed output.

### Verify Before Push

Run the verification script:

```bash
bash verify_build.sh
```

This checks:
- Python installation
- Required files and directories
- JSON file validity
- MkDocs build success

## 🚢 Deployment

### Automatic Deployment (GitLab CI/CD)

The site automatically deploys to GitLab Pages when you push to `main` or `master`:

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Update documentation"
   ```

2. **Push to GitLab**
   ```bash
   git push origin main
   ```

3. **Monitor pipeline**
   - Go to your GitLab project
   - Navigate to **CI/CD** → **Pipelines**
   - Watch the build and deploy stages

4. **Access your site**
   ```
   https://<namespace>.gitlab.io/<project-name>
   ```

### Pipeline Stages

1. **Build Stage**
   - Installs dependencies
   - Verifies data files
   - Builds MkDocs site
   - Creates artifacts

2. **Deploy Stage**
   - Copies built site to `public/`
   - Deploys to GitLab Pages

See [GITLAB_CI_SETUP.md](GITLAB_CI_SETUP.md) for detailed CI/CD information.

## 📊 Data Files

The site loads data from JSON files in the `data/` directory:

- **papers.json** - Research publications and citations
- **research_lines.json** - Research lines with projects
- **scholarships.json** - Scholarship information
- **students.json** - Student data
- **supervisors.json** - Supervisor information
- **partnership_analysis.json** - Partnership data

### Updating Data

1. Update JSON files in `data/` directory
2. Commit and push changes
3. Site rebuilds automatically

### Data Validation

JSON files are validated during build. Invalid JSON will cause build failure.

## 🌍 Internationalization

The site supports multiple languages:

- **English** (default): `filename.md`
- **Portuguese**: `filename.pt.md`

Language selector appears in the navigation bar.

### Adding Translations

1. Create Portuguese version: `docs/newpage.pt.md`
2. Add to navigation in `mkdocs.yml`:
   ```yaml
   nav:
     - New Page:
       - en: newpage.md
       - pt: newpage.pt.md
   ```

## 🎨 Customization

### Theme

The site uses Material for MkDocs theme. Customize in `onestep-static/mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.instant
```

### Custom Macros

Add custom macros in `onestep-static/main.py`:

```python
def define_env(env):
    @env.macro
    def my_custom_macro():
        return "Hello from macro!"
```

Use in markdown:
```markdown
{{ my_custom_macro() }}
```

## 📝 Adding New Pages

1. **Create markdown file**
   ```bash
   # English version
   touch onestep-static/docs/newpage.md
   
   # Portuguese version
   touch onestep-static/docs/newpage.pt.md
   ```

2. **Add to navigation** in `mkdocs.yml`
   ```yaml
   nav:
     - New Page:
       - en: newpage.md
       - pt: newpage.pt.md
   ```

3. **Use data macros**
   ```markdown
   {% set data = load_papers_data() %}
   # My New Page
   Total researchers: {{ data['total_researchers'] }}
   ```

## 🔍 Troubleshooting

### Build Fails

1. Check data files exist and are valid JSON
2. Run `mkdocs build --strict --verbose` for details
3. Check `main.py` for errors
4. Review GitLab CI/CD logs

### Pages Not Updating

1. Clear browser cache
2. Wait a few minutes for GitLab Pages
3. Check pipeline completed successfully
4. Verify `pages` job ran

### Data Not Loading

1. Verify file paths in `main.py`
2. Check JSON structure
3. Ensure files are committed to repository

## 📚 Documentation

### Project Documentation
All project documentation is organized in the [`docs-projeto/`](docs-projeto/) folder:

- **[docs-projeto/README.md](docs-projeto/README.md)** - Documentation index
- **[Project Structure](docs-projeto/PROJECT_STRUCTURE.md)** - Detailed project structure
- **[GitLab CI/CD Setup](docs-projeto/GITLAB_CI_SETUP.md)** - CI/CD configuration guide
- **[Quick Reference](docs-projeto/QUICK_REFERENCE.md)** - Command reference
- **[Deployment Checklist](docs-projeto/DEPLOYMENT_CHECKLIST.md)** - Pre-deployment checklist

### External Documentation
- [MkDocs Documentation](https://www.mkdocs.org/) - Official MkDocs docs
- [Material Theme](https://squidfunk.github.io/mkdocs-material/) - Theme documentation

## 🛠️ Development

### Requirements

See `requirements.txt` for all dependencies. Key packages:

- `mkdocs==1.6.1` - Static site generator
- `mkdocs-material` - Material theme
- `mkdocs-macros-plugin==1.5.0` - Custom macros
- `mkdocs-static-i18n==1.2.3` - Internationalization
- `pandas==2.3.3` - Data manipulation

### Testing

Run verification script before pushing:

```bash
bash verify_build.sh
```

### Code Style

- Python: Follow PEP 8
- Markdown: Use consistent formatting
- YAML: 2-space indentation

## 🤝 Contributing

1. Create a feature branch
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make changes and test locally
   ```bash
   cd onestep-static
   mkdocs serve
   ```

3. Verify build
   ```bash
   bash verify_build.sh
   ```

4. Commit and push
   ```bash
   git add .
   git commit -m "Add my feature"
   git push origin feature/my-feature
   ```

5. Create merge request on GitLab

## 📄 License

[Add your license information here]

## 👥 Authors

- IFES Campus Serra Research Team

## 📧 Support

For issues or questions:
- Open an issue on GitLab
- Check documentation files
- Review MkDocs and Material theme docs

## 🔗 Links

- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)

---

**Note**: Remember to make `verify_build.sh` executable:
```bash
chmod +x verify_build.sh
```
