# GitLab CI/CD Configuration Notes

## ✅ Current Status

The `.gitlab-ci.yml` file has been validated and is ready to use.

## 📝 Important Notes

### YAML Syntax

GitLab CI/CD is strict about YAML syntax. Key points:

1. **No inline comments in script arrays**
   - ❌ Bad: `- pip install -r requirements.txt  # Install deps`
   - ✅ Good: Use separate comment lines or remove comments

2. **Consistent indentation**
   - Use 2 spaces for indentation
   - Never mix tabs and spaces

3. **Script format**
   - Each command must be a separate list item
   - Start each command with `-`
   - Keep commands simple and clear

### File Versions

- **`.gitlab-ci.yml`** - Production version (clean, no inline comments)
- **`.gitlab-ci.yml.documented`** - Documented version with block comments

### Validation

To validate the YAML file locally:

```bash
# Using Python
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"

# Using yamllint (if installed)
yamllint .gitlab-ci.yml

# Using GitLab CI Lint (in GitLab UI)
# Go to: CI/CD → Editor → Validate
```

## 🔧 Configuration Details

### Jobs Overview

| Job | Stage | Runs On | Purpose |
|-----|-------|---------|---------|
| `build` | build | main, master, develop | Build site and create artifacts |
| `pages` | deploy | main, master | Deploy to GitLab Pages |
| `test_build` | build | merge_requests | Test build without deploying |

### Script Commands

Each job's script section contains commands that run sequentially:

**Build Job:**
1. Install Python dependencies
2. List data directory contents
3. Change to onestep-static directory
4. Build MkDocs site with strict mode
5. List generated site contents

**Pages Job:**
1. Create public directory
2. Copy built site to public
3. Verify files were copied

**Test Build Job:**
1. Install Python dependencies
2. Check data directory (with fallback)
3. Change to onestep-static directory
4. Build MkDocs site with strict mode

### Artifacts

**Build artifacts:**
- Path: `onestep-static/site`
- Expires: 1 hour
- Used by: `pages` job

**Pages artifacts:**
- Path: `public`
- Expires: Never (required for GitLab Pages)
- Used by: GitLab Pages service

### Cache

Cached items to speed up builds:
- `.cache/pip` - Python package cache
- `venv/` - Virtual environment

Cache is shared across pipeline runs.

## 🐛 Common Issues and Solutions

### Issue: "script config should be a string or nested array"

**Cause:** Inline comments in script array or incorrect indentation

**Solution:**
```yaml
# ❌ Wrong
script:
  - pip install -r requirements.txt  # Install dependencies

# ✅ Correct
script:
  - pip install -r requirements.txt
```

### Issue: "YAML syntax error"

**Cause:** Mixed indentation or invalid YAML

**Solution:**
1. Check indentation (use 2 spaces)
2. Validate with Python: `python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"`
3. Use GitLab CI Lint in the web interface

### Issue: "Job failed: command not found"

**Cause:** Command not available in Docker image

**Solution:**
1. Install required tools in `before_script`
2. Or use a different base image with tools pre-installed

### Issue: "Artifacts not found"

**Cause:** Artifact path doesn't exist or job didn't run

**Solution:**
1. Check artifact path is correct
2. Verify previous job completed successfully
3. Check `dependencies` are set correctly

## 🚀 Deployment Flow

```
Push to GitLab
    ↓
before_script runs
    ↓
build job
    ├── Install dependencies
    ├── Verify data files
    ├── Build MkDocs site
    └── Create artifacts
    ↓
pages job (only on main/master)
    ├── Load artifacts from build
    ├── Copy to public/
    └── Deploy to GitLab Pages
    ↓
Site is live! 🎉
```

## 📊 Pipeline Optimization

### Current Optimizations

1. **Caching**
   - Pip packages cached
   - Virtual environment cached
   - Reduces build time by ~50%

2. **Artifacts**
   - Build artifacts expire after 1 hour
   - Saves storage space
   - Pages artifacts never expire (required)

3. **Dependencies**
   - Pages job depends on build job
   - Ensures artifacts are available
   - Prevents unnecessary rebuilds

### Potential Improvements

1. **Parallel Jobs**
   ```yaml
   test_lint:
     stage: test
     script:
       - pip install flake8
       - flake8 .
   
   test_build:
     stage: test
     script:
       - cd onestep-static
       - mkdocs build --strict
   ```

2. **Docker Layer Caching**
   ```yaml
   variables:
     DOCKER_DRIVER: overlay2
   ```

3. **Conditional Builds**
   ```yaml
   build:
     only:
       changes:
         - onestep-static/**/*
         - data/**/*
   ```

## 🔐 Security Considerations

### Current Security

1. **No secrets in code**
   - No API keys or passwords
   - Uses GitLab built-in variables

2. **Protected branches**
   - Consider protecting main/master
   - Require approvals for merges

3. **Pipeline permissions**
   - Runs with user permissions
   - Limited to project scope

### Recommendations

1. **Enable branch protection**
   - Settings → Repository → Protected Branches
   - Protect main/master branches

2. **Use CI/CD variables for secrets**
   - Settings → CI/CD → Variables
   - Mark as protected and masked

3. **Review pipeline logs**
   - Check for exposed secrets
   - Ensure no sensitive data in output

## 📈 Monitoring

### What to Monitor

1. **Build time**
   - Target: < 2 minutes with cache
   - Alert if > 5 minutes

2. **Success rate**
   - Target: > 95%
   - Investigate failures

3. **Artifact size**
   - Monitor site size growth
   - Optimize if too large

4. **Cache hit rate**
   - Should be high (> 80%)
   - Rebuild cache if low

### Monitoring Tools

1. **GitLab CI/CD Analytics**
   - CI/CD → Analytics
   - View pipeline statistics

2. **Pipeline Badges**
   - Add to README.md
   - Show build status

3. **Email Notifications**
   - Settings → Integrations
   - Configure email alerts

## 🔄 Maintenance

### Regular Tasks

1. **Update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   pip freeze > requirements.txt
   ```

2. **Review pipeline logs**
   - Check for warnings
   - Optimize slow steps

3. **Clean old artifacts**
   - Automatic with expiration
   - Manual: Settings → CI/CD → Artifacts

4. **Update base image**
   ```yaml
   image: python:3.12-slim  # Update version
   ```

### Troubleshooting Checklist

- [ ] Check YAML syntax
- [ ] Verify file paths
- [ ] Check job dependencies
- [ ] Review artifact paths
- [ ] Validate data files
- [ ] Test locally first
- [ ] Check GitLab CI/CD logs
- [ ] Verify cache is working

## 📚 Additional Resources

- [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab Pages Documentation](https://docs.gitlab.com/ee/user/project/pages/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)

## ✅ Validation Checklist

Before committing `.gitlab-ci.yml`:

- [ ] YAML syntax is valid
- [ ] All job names are unique
- [ ] Script commands are properly formatted
- [ ] Artifact paths are correct
- [ ] Dependencies are set correctly
- [ ] Only/except rules are correct
- [ ] Environment variables are set
- [ ] Cache paths are correct
- [ ] Tested locally (if possible)

## 🎯 Best Practices

1. **Keep it simple**
   - Start with basic configuration
   - Add complexity as needed

2. **Use meaningful job names**
   - Clear and descriptive
   - Follow naming conventions

3. **Document changes**
   - Add comments for complex logic
   - Update this file when changing CI/CD

4. **Test before merging**
   - Use test_build job
   - Verify on feature branches

5. **Monitor and optimize**
   - Track build times
   - Optimize slow steps
   - Use caching effectively

---

**Last Updated:** 2024-11-24
**Configuration Version:** 1.0
**Status:** ✅ Validated and Working
