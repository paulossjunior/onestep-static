# Quick Reference Guide

## 🚀 Common Commands

### Setup

```bash
# Clone repository
git clone <repo-url>
cd <repo-name>

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Local Development

```bash
# Serve site locally (with auto-reload)
cd onestep-static
mkdocs serve

# Serve on different port
mkdocs serve -a localhost:8080

# Serve and allow external access
mkdocs serve -a 0.0.0.0:8000
```

### Building

```bash
# Build site
cd onestep-static
mkdocs build

# Build with strict mode (fail on warnings)
mkdocs build --strict

# Build with verbose output
mkdocs build --strict --verbose

# Clean build (remove site directory first)
rm -rf site && mkdocs build
```

### Verification

```bash
# Run verification script
bash verify_build.sh

# Check Python version
python3 --version

# Verify data files
ls -la data/

# Validate JSON files
python3 -m json.tool data/papers.json > /dev/null && echo "Valid JSON"
```

### Git Operations

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitLab
git push origin main

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes
git pull origin main
```

### GitLab CI/CD

```bash
# View pipeline status (in GitLab web interface)
# Go to: CI/CD → Pipelines

# Trigger manual pipeline
# Go to: CI/CD → Pipelines → Run Pipeline

# View job logs
# Go to: CI/CD → Pipelines → Click pipeline → Click job
```

## 📁 File Locations

```bash
# MkDocs configuration
onestep-static/mkdocs.yml

# Custom macros
onestep-static/main.py

# Documentation files
onestep-static/docs/

# Data files
data/

# CI/CD configuration
.gitlab-ci.yml

# Python dependencies
requirements.txt

# Built site (generated)
onestep-static/site/
```

## 🔧 Useful MkDocs Commands

```bash
# Get MkDocs version
mkdocs --version

# Get help
mkdocs --help
mkdocs build --help
mkdocs serve --help

# Create new MkDocs project (don't use in existing project!)
mkdocs new my-project

# Deploy to GitHub Pages (if using GitHub)
mkdocs gh-deploy
```

## 🐍 Python Commands

```bash
# Check Python version
python3 --version

# Install specific package
pip install mkdocs==1.6.1

# Upgrade package
pip install --upgrade mkdocs

# List installed packages
pip list

# Show package info
pip show mkdocs

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Uninstall package
pip uninstall mkdocs
```

## 📊 Data Operations

```bash
# View JSON file
cat data/papers.json

# Pretty print JSON
python3 -m json.tool data/papers.json

# Validate JSON
python3 -c "import json; json.load(open('data/papers.json'))"

# Count lines in JSON
wc -l data/papers.json

# Search in JSON
grep "researcher" data/papers.json

# Check file size
du -h data/papers.json
```

## 🔍 Debugging

```bash
# Check if port is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process on port
kill -9 $(lsof -t -i:8000)  # Linux/Mac

# View MkDocs build log
cd onestep-static
mkdocs build --strict --verbose 2>&1 | tee build.log

# Check Python path
which python3

# Check pip path
which pip

# List Python packages location
python3 -m site
```

## 🌐 Browser Commands

```bash
# Open local site
# Linux
xdg-open http://localhost:8000

# Mac
open http://localhost:8000

# Windows
start http://localhost:8000
```

## 📝 Editing Files

```bash
# Edit with nano
nano onestep-static/mkdocs.yml

# Edit with vim
vim onestep-static/mkdocs.yml

# Edit with VS Code
code onestep-static/mkdocs.yml

# Edit with default editor
$EDITOR onestep-static/mkdocs.yml
```

## 🧹 Cleanup

```bash
# Remove built site
rm -rf onestep-static/site/

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove virtual environment
rm -rf venv/

# Remove pip cache
rm -rf .cache/

# Clean everything (be careful!)
git clean -fdx  # Removes all untracked files
```

## 📦 Package Management

```bash
# Update pip
pip install --upgrade pip

# Install development dependencies
pip install -r requirements.txt

# Create requirements file
pip freeze > requirements.txt

# Install from requirements with specific Python
python3.11 -m pip install -r requirements.txt
```

## 🔐 GitLab Specific

```bash
# Clone with SSH
git clone git@gitlab.com:username/repo.git

# Clone with HTTPS
git clone https://gitlab.com/username/repo.git

# Add GitLab remote
git remote add origin git@gitlab.com:username/repo.git

# View remotes
git remote -v

# Push to specific remote
git push origin main

# Set upstream branch
git push -u origin main
```

## 📊 Statistics

```bash
# Count markdown files
find onestep-static/docs -name "*.md" | wc -l

# Count lines of code
find . -name "*.py" -exec wc -l {} + | tail -1

# Count JSON files
ls -1 data/*.json | wc -l

# Size of data directory
du -sh data/

# Size of built site
du -sh onestep-static/site/
```

## 🎨 Theme Customization

```bash
# View Material theme version
pip show mkdocs-material

# Update Material theme
pip install --upgrade mkdocs-material

# View available themes
mkdocs --help | grep -A 10 "theme"

# Copy Material theme for customization
# (Advanced - not usually needed)
```

## 🔄 Update Workflow

```bash
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
pip install -r requirements.txt --upgrade

# 3. Make changes
# Edit files...

# 4. Test locally
cd onestep-static && mkdocs serve

# 5. Verify build
bash verify_build.sh

# 6. Commit and push
git add .
git commit -m "Update: description"
git push origin main

# 7. Check pipeline
# Visit GitLab → CI/CD → Pipelines
```

## 🆘 Emergency Commands

```bash
# Revert last commit (not pushed)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# Restore specific file
git checkout -- filename

# Force push (use with caution!)
git push --force origin main

# Abort merge
git merge --abort

# Clean working directory
git clean -fd
```

## 📱 Mobile Testing

```bash
# Serve with external access
cd onestep-static
mkdocs serve -a 0.0.0.0:8000

# Find your IP address
# Linux/Mac
ifconfig | grep "inet "
ip addr show

# Windows
ipconfig

# Access from mobile
# http://<your-ip>:8000
```

## 🔗 Useful Links

- MkDocs: https://www.mkdocs.org/
- Material: https://squidfunk.github.io/mkdocs-material/
- GitLab Pages: https://docs.gitlab.com/ee/user/project/pages/
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Python: https://www.python.org/
- Jinja2: https://jinja.palletsprojects.com/

## 💡 Tips

1. **Always test locally before pushing**
   ```bash
   mkdocs serve
   ```

2. **Use strict mode to catch errors**
   ```bash
   mkdocs build --strict
   ```

3. **Verify JSON before committing**
   ```bash
   python3 -m json.tool data/file.json
   ```

4. **Keep virtual environment active**
   ```bash
   source venv/bin/activate
   ```

5. **Check pipeline before leaving**
   - Visit GitLab after pushing
   - Ensure pipeline passes

6. **Use verification script**
   ```bash
   bash verify_build.sh
   ```

7. **Clear browser cache if changes don't appear**
   - Ctrl+Shift+R (hard refresh)
   - Or clear cache manually

8. **Monitor build time**
   - First build: ~2-3 minutes
   - Cached builds: ~1-2 minutes

9. **Use branches for features**
   ```bash
   git checkout -b feature/name
   ```

10. **Document your changes**
    - Write clear commit messages
    - Update documentation if needed
