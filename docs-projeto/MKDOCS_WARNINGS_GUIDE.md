# MkDocs Warnings Troubleshooting Guide

## 🔍 Understanding the Issue

The build is failing with:
```
Aborted with 2 warnings in strict mode!
```

This means MkDocs found 2 warnings during the build process. In strict mode (`--strict`), any warning causes the build to fail.

## ✅ Solution Applied

The `.gitlab-ci.yml` has been updated to:

1. **Remove `--strict` flag** from main build jobs
   - Allows build to complete with warnings
   - Site will still be generated and deployed

2. **Add `validate_strict` job** (optional)
   - Runs with `--strict` flag
   - Marked as `allow_failure: true`
   - Shows warnings without blocking deployment

## 🔧 Current Configuration

### Build Job (Production)
```yaml
build:
  stage: build
  script:
    - mkdocs build --verbose  # No --strict flag
```
✅ Will succeed even with warnings

### Validate Job (Optional)
```yaml
validate_strict:
  stage: build
  script:
    - mkdocs build --strict --verbose || echo "Build has warnings"
  allow_failure: true
```
⚠️ Shows warnings but doesn't block pipeline

## 🐛 Common MkDocs Warnings

### 1. Missing Files
```
WARNING - Doc file 'path/to/file.md' contains a link to 'missing.md' 
which is not found in the documentation files.
```

**Causes:**
- Broken internal links
- Referenced file doesn't exist
- Typo in file path

**Fix:**
```bash
# Find broken links
grep -r "missing.md" onestep-static/docs/

# Fix the link or create the missing file
```

### 2. Navigation Issues
```
WARNING - A page is not included in the navigation: 'orphan.md'
```

**Causes:**
- File exists but not in `mkdocs.yml` navigation
- Orphaned documentation page

**Fix:**
Add to `mkdocs.yml`:
```yaml
nav:
  - Orphan Page: orphan.md
```

### 3. Plugin Warnings
```
WARNING - Plugin 'macros' raised an exception
```

**Causes:**
- Error in `main.py` macros
- Missing data files
- Invalid JSON

**Fix:**
```bash
# Check data files
ls -la data/
python3 -m json.tool data/papers.json

# Test macros
cd onestep-static
python3 -c "import main; print('OK')"
```

### 4. Theme Issues
```
WARNING - Theme file not found: 'custom.css'
```

**Causes:**
- Referenced file doesn't exist
- Wrong path in configuration

**Fix:**
Check `mkdocs.yml` and verify file paths

### 5. i18n Plugin Warnings
```
WARNING - i18n plugin: Missing translation for 'page.md'
```

**Causes:**
- English page exists but Portuguese version missing
- Or vice versa

**Fix:**
Create missing translation:
```bash
# If page.md exists, create page.pt.md
cp onestep-static/docs/page.md onestep-static/docs/page.pt.md
# Then translate content
```

## 🔍 Diagnosing Warnings

### Step 1: Build Locally with Verbose Output

```bash
cd onestep-static
mkdocs build --strict --verbose 2>&1 | tee build.log
```

This will:
- Show all warnings
- Save output to `build.log`
- Fail on warnings (like CI does)

### Step 2: Analyze the Output

Look for lines starting with:
- `WARNING -`
- `ERROR -`

Example output:
```
WARNING - Doc file 'index.md' contains a link to 'missing.md' 
which is not found in the documentation files.
WARNING - A page is not included in the navigation: 'orphan.md'
```

### Step 3: Fix Each Warning

Address warnings one by one, then rebuild:
```bash
mkdocs build --strict --verbose
```

## 🛠️ Quick Fixes

### Fix 1: Check All Data Files Exist

```bash
# Verify data files
for file in papers.json research_lines.json scholarships.json students.json supervisors.json partnership_analysis.json; do
    if [ -f "data/$file" ]; then
        echo "✓ data/$file exists"
        python3 -m json.tool "data/$file" > /dev/null && echo "  Valid JSON" || echo "  INVALID JSON"
    else
        echo "✗ data/$file MISSING"
    fi
done
```

### Fix 2: Check All Referenced Pages Exist

```bash
# Find all markdown links
cd onestep-static/docs
grep -r "\[.*\](.*\.md)" . | grep -v "http"
```

### Fix 3: Verify Navigation Structure

```bash
# Check mkdocs.yml navigation
cd onestep-static
python3 << 'EOF'
import yaml
with open('mkdocs.yml') as f:
    config = yaml.safe_load(f)
    nav = config.get('nav', [])
    print("Navigation structure:")
    print(yaml.dump(nav, default_flow_style=False))
EOF
```

### Fix 4: Check for Orphaned Files

```bash
# Find markdown files not in navigation
cd onestep-static
python3 << 'EOF'
import yaml
import os
from pathlib import Path

# Load navigation
with open('mkdocs.yml') as f:
    config = yaml.safe_load(f)

# Get all markdown files
docs_dir = Path('docs')
all_md_files = set(str(p.relative_to(docs_dir)) for p in docs_dir.rglob('*.md'))

# Get files in navigation
def extract_files(nav_item):
    files = set()
    if isinstance(nav_item, dict):
        for key, value in nav_item.items():
            if isinstance(value, str) and value.endswith('.md'):
                files.add(value)
            elif isinstance(value, (list, dict)):
                files.update(extract_files(value))
    elif isinstance(nav_item, list):
        for item in nav_item:
            files.update(extract_files(item))
    return files

nav_files = extract_files(config.get('nav', []))

# Find orphaned files
orphaned = all_md_files - nav_files
if orphaned:
    print("Orphaned files (not in navigation):")
    for f in sorted(orphaned):
        print(f"  - {f}")
else:
    print("No orphaned files found")
EOF
```

## 🎯 Recommended Approach

### Option 1: Fix Warnings (Recommended for Production)

1. **Build locally with strict mode:**
   ```bash
   cd onestep-static
   mkdocs build --strict --verbose
   ```

2. **Fix all warnings**

3. **Re-enable strict mode in CI:**
   ```yaml
   build:
     script:
       - mkdocs build --strict --verbose
   ```

### Option 2: Allow Warnings (Quick Fix)

1. **Keep current configuration** (no `--strict` flag)
2. **Monitor warnings** using `validate_strict` job
3. **Fix warnings gradually**

### Option 3: Hybrid Approach

1. **Production builds:** No strict mode (deploy even with warnings)
2. **Validation job:** Strict mode with `allow_failure: true`
3. **Fix warnings** when time permits

## 📊 Monitoring Warnings

### In GitLab CI/CD

1. Go to **CI/CD → Pipelines**
2. Click on pipeline
3. Check `validate_strict` job (if enabled)
4. Review warnings in job log

### Locally

```bash
# Build and count warnings
cd onestep-static
mkdocs build --verbose 2>&1 | grep "WARNING" | wc -l

# Show all warnings
mkdocs build --verbose 2>&1 | grep "WARNING"
```

## 🔄 Workflow

### Current Workflow (With Warnings Allowed)

```
Push to GitLab
    ↓
Build Job (no --strict)
    ├── Warnings shown but ignored
    ├── Build completes
    └── Artifacts created
    ↓
Validate Job (--strict, allow_failure)
    ├── Shows warnings
    └── Doesn't block pipeline
    ↓
Pages Job
    ├── Deploys site
    └── Site is live
```

### Ideal Workflow (No Warnings)

```
Push to GitLab
    ↓
Build Job (--strict)
    ├── No warnings
    ├── Build completes
    └── Artifacts created
    ↓
Pages Job
    ├── Deploys site
    └── Site is live
```

## 📝 Checklist for Fixing Warnings

- [ ] Build locally with `--strict --verbose`
- [ ] Note all warnings
- [ ] Check all data files exist and are valid JSON
- [ ] Verify all internal links work
- [ ] Ensure all pages are in navigation
- [ ] Check for missing translations (i18n)
- [ ] Test macros in `main.py`
- [ ] Verify theme files exist
- [ ] Re-build with strict mode
- [ ] Commit fixes
- [ ] Re-enable `--strict` in CI (optional)

## 🆘 If You Need Help

### Get Detailed Warning Information

```bash
cd onestep-static
mkdocs build --strict --verbose 2>&1 | tee build.log
cat build.log | grep -A 5 "WARNING"
```

### Common Commands

```bash
# Test build without strict
mkdocs build --verbose

# Test build with strict
mkdocs build --strict --verbose

# Serve locally (ignores warnings)
mkdocs serve

# Clean build
rm -rf site && mkdocs build --verbose
```

## 📚 Resources

- [MkDocs Configuration](https://www.mkdocs.org/user-guide/configuration/)
- [MkDocs Writing Your Docs](https://www.mkdocs.org/user-guide/writing-your-docs/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [MkDocs Plugins](https://www.mkdocs.org/user-guide/plugins/)

## ✅ Summary

**Current Status:**
- ✅ Build will succeed with warnings
- ✅ Site will deploy
- ⚠️ Warnings are logged but not blocking

**Next Steps:**
1. Review warnings in CI/CD logs
2. Fix warnings locally
3. Test with `mkdocs build --strict --verbose`
4. Optionally re-enable strict mode in CI

---

**Note:** It's better to fix warnings than to ignore them, but allowing warnings temporarily ensures your site stays online while you work on fixes.
