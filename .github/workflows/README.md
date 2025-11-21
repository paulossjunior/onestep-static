# GitHub Actions Workflows

## Deploy to GitHub Pages

### Overview
This workflow automatically builds and deploys the research documentation to GitHub Pages whenever changes are made to source data or documentation files.

### Trigger Conditions

The workflow runs automatically when:
1. **Push to main branch** with changes in:
   - `source/**` - Source CSV files with research data
   - `src/**` - Python processing scripts
   - `onestep-static/**` - Documentation markdown files
   - `.github/workflows/deploy-pages.yml` - The workflow itself

2. **Manual trigger** - Can be run manually from GitHub Actions tab

### Workflow Steps

#### Build Job

1. **Checkout repository** - Gets the latest code
2. **Setup Python 3.12** - Installs Python with pip caching
3. **Install dependencies** - Installs packages from requirements.txt
4. **Process research groups** - Converts CSV to JSON
   ```bash
   python src/process_research_groups.py
   ```
5. **Process research projects** - Converts CSV to JSON
   ```bash
   python src/process_research_projects.py
   ```
6. **Generate network statistics** - Creates collaboration network data
   ```bash
   python src/generate_network_stats.py
   ```
7. **Setup Pages** - Configures GitHub Pages
8. **Build with MkDocs** - Generates static HTML site
   ```bash
   mkdocs build --clean --strict
   ```
9. **Upload artifact** - Prepares site for deployment

#### Deploy Job

1. **Deploy to GitHub Pages** - Publishes the built site
2. **Output URL** - Provides the live site URL

### Configuration Requirements

#### Repository Settings

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: GitHub Actions

2. **Permissions**:
   - Settings → Actions → General
   - Workflow permissions: Read and write permissions

#### Branch Protection (Optional)

Consider protecting the main branch to ensure quality:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date

### File Structure

```
.github/
└── workflows/
    ├── deploy-pages.yml    # Main deployment workflow
    └── README.md           # This file

source/                     # Source CSV files (triggers rebuild)
├── research_groups/
│   └── research_group.csv
└── research_project/
    └── *.csv

src/                        # Processing scripts (triggers rebuild)
├── process_research_groups.py
├── process_research_projects.py
└── generate_network_stats.py

onestep-static/            # Documentation (triggers rebuild)
└── docs/
    ├── index.md
    ├── research_groups.md
    └── research_projects.md

data/                      # Generated JSON files
├── research_group.json
├── research_projects.json
└── network_stats.json

site/                      # Built site (generated, not committed)
```

### Monitoring

#### View Workflow Runs
- Go to Actions tab in GitHub
- Click on "Deploy to GitHub Pages"
- View run history and logs

#### Check Deployment Status
- Green checkmark: Successful deployment
- Red X: Failed deployment (check logs)
- Yellow dot: In progress

#### View Live Site
- URL format: `https://<username>.github.io/<repository>/`
- Or check the deployment URL in the workflow output

### Troubleshooting

#### Build Fails

**Python errors:**
- Check that all dependencies are in requirements.txt
- Verify Python scripts run locally first
- Check logs for specific error messages

**MkDocs errors:**
- Verify mkdocs.yml configuration
- Check that all referenced files exist
- Test locally: `mkdocs build --strict`

**Data processing errors:**
- Verify CSV files are properly formatted
- Check that source files exist
- Run scripts locally to debug

#### Deployment Fails

**Permissions error:**
- Verify GitHub Pages is enabled
- Check workflow permissions in repository settings

**Artifact upload error:**
- Check that `site/` directory was created
- Verify MkDocs build completed successfully

### Local Testing

Before pushing, test the complete workflow locally:

```bash
# 1. Process data
python src/process_research_groups.py
python src/process_research_projects.py
python src/generate_network_stats.py

# 2. Build site
mkdocs build --clean --strict

# 3. Preview locally
mkdocs serve
# Open http://127.0.0.1:8000
```

### Maintenance

#### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

#### Modify Workflow
- Edit `.github/workflows/deploy-pages.yml`
- Test changes with manual trigger before merging
- Monitor first automated run after changes

### Performance

**Typical build time:** 2-5 minutes
- Data processing: ~30 seconds
- MkDocs build: ~1-2 minutes
- Deployment: ~1 minute

**Optimization tips:**
- Use caching for pip dependencies (already enabled)
- Consider incremental builds for large datasets
- Monitor workflow run times in Actions tab

### Security

**Best Practices:**
- Never commit sensitive data to source files
- Use repository secrets for API keys if needed
- Review changes before merging to main
- Keep dependencies updated for security patches

### Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review this README
3. Test locally to isolate the problem
4. Check GitHub Pages documentation
