# Deployment Checklist

Use this checklist before deploying to ensure everything is ready.

## 📋 Pre-Deployment Checklist

### 1. Code Quality

- [ ] All code changes are committed
- [ ] No debug code or console.logs left in files
- [ ] No sensitive data (passwords, tokens) in code
- [ ] Code follows project conventions
- [ ] Comments are clear and up-to-date

### 2. Data Files

- [ ] All JSON files in `data/` directory are present
- [ ] JSON files are valid (no syntax errors)
- [ ] Data is up-to-date
- [ ] No test/dummy data in production files
- [ ] File sizes are reasonable (not too large)

**Verify JSON:**
```bash
for file in data/*.json; do
    python3 -m json.tool "$file" > /dev/null && echo "✓ $file" || echo "✗ $file INVALID"
done
```

### 3. Documentation Files

- [ ] All markdown files are present in `onestep-static/docs/`
- [ ] Both English (.md) and Portuguese (.pt.md) versions exist
- [ ] No broken internal links
- [ ] Images/assets are included and referenced correctly
- [ ] Navigation structure is correct in `mkdocs.yml`

### 4. Configuration

- [ ] `mkdocs.yml` is properly configured
- [ ] Site name and description are correct
- [ ] Navigation structure is complete
- [ ] Theme settings are correct
- [ ] Plugins are properly configured
- [ ] i18n settings are correct

### 5. Dependencies

- [ ] `requirements.txt` is up-to-date
- [ ] All required packages are listed
- [ ] Package versions are specified
- [ ] No conflicting dependencies

**Update requirements:**
```bash
pip freeze > requirements.txt
```

### 6. Local Testing

- [ ] Site builds successfully locally
- [ ] No build warnings or errors
- [ ] All pages render correctly
- [ ] Navigation works properly
- [ ] Search functionality works
- [ ] Language switcher works
- [ ] All data loads correctly
- [ ] Charts and visualizations display
- [ ] Mobile responsive design works

**Test build:**
```bash
cd onestep-static
mkdocs build --strict --verbose
```

**Test serve:**
```bash
cd onestep-static
mkdocs serve
# Visit http://localhost:8000
```

### 7. GitLab CI/CD

- [ ] `.gitlab-ci.yml` is present and correct
- [ ] Pipeline stages are properly defined
- [ ] Build job is configured correctly
- [ ] Deploy job is configured correctly
- [ ] Artifacts are properly defined
- [ ] Cache is configured for performance

### 8. Git Repository

- [ ] All changes are committed
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up-to-date with main
- [ ] No merge conflicts
- [ ] `.gitignore` is properly configured
- [ ] No unnecessary files in repository

**Check status:**
```bash
git status
git log --oneline -5
```

### 9. GitLab Pages Setup

- [ ] GitLab Pages is enabled in project settings
- [ ] Custom domain configured (if applicable)
- [ ] SSL/TLS certificate configured (if applicable)
- [ ] Access level is set correctly (public/private)

### 10. Performance

- [ ] Site builds in reasonable time (< 5 minutes)
- [ ] Generated site size is reasonable
- [ ] No extremely large files
- [ ] Images are optimized
- [ ] No unnecessary dependencies

**Check sizes:**
```bash
du -sh onestep-static/site/
du -sh data/
```

## 🚀 Deployment Steps

### Step 1: Final Verification

```bash
# Run verification script
bash verify_build.sh
```

- [ ] Verification script passes all checks

### Step 2: Commit Changes

```bash
# Check what will be committed
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Deploy: [description of changes]"
```

- [ ] Changes committed successfully

### Step 3: Push to GitLab

```bash
# Push to main branch
git push origin main
```

- [ ] Push successful
- [ ] No errors during push

### Step 4: Monitor Pipeline

1. Go to GitLab project
2. Navigate to **CI/CD** → **Pipelines**
3. Watch the latest pipeline

- [ ] Pipeline started automatically
- [ ] Build stage completed successfully
- [ ] Deploy stage completed successfully
- [ ] No errors in logs

### Step 5: Verify Deployment

1. Wait 2-3 minutes for GitLab Pages to update
2. Visit your site URL: `https://<namespace>.gitlab.io/<project-name>`

- [ ] Site is accessible
- [ ] Home page loads correctly
- [ ] Navigation works
- [ ] All pages are accessible
- [ ] Data displays correctly
- [ ] Charts and visualizations work
- [ ] Language switcher works
- [ ] Search functionality works
- [ ] Mobile view works

### Step 6: Test All Features

- [ ] Test all navigation links
- [ ] Test search with various queries
- [ ] Test language switching
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices
- [ ] Test all interactive elements
- [ ] Verify all data is current

### Step 7: Performance Check

- [ ] Page load time is acceptable (< 3 seconds)
- [ ] No console errors in browser
- [ ] No broken images or assets
- [ ] No 404 errors

**Check in browser:**
- Open Developer Tools (F12)
- Check Console for errors
- Check Network tab for failed requests

## 🔍 Post-Deployment Verification

### Immediate Checks (0-5 minutes)

- [ ] Site is live and accessible
- [ ] Home page loads
- [ ] No obvious errors

### Short-term Checks (5-30 minutes)

- [ ] All pages are accessible
- [ ] Data is displaying correctly
- [ ] Search works
- [ ] Navigation works
- [ ] Mobile view works

### Long-term Monitoring (1-24 hours)

- [ ] No user-reported issues
- [ ] Analytics show normal traffic (if configured)
- [ ] No error reports
- [ ] Performance is stable

## 🆘 Rollback Plan

If deployment fails or issues are found:

### Option 1: Quick Fix

```bash
# Fix the issue
# Edit files...

# Commit and push
git add .
git commit -m "Fix: [description]"
git push origin main
```

### Option 2: Revert to Previous Version

```bash
# Find last working commit
git log --oneline

# Revert to that commit
git revert <commit-hash>

# Push revert
git push origin main
```

### Option 3: Force Rollback

```bash
# Reset to previous commit (use with caution!)
git reset --hard <commit-hash>

# Force push
git push --force origin main
```

## 📊 Deployment Metrics

Track these metrics for each deployment:

- **Build Time**: _____ minutes
- **Deploy Time**: _____ minutes
- **Total Time**: _____ minutes
- **Site Size**: _____ MB
- **Number of Pages**: _____
- **Pipeline Status**: ✓ Pass / ✗ Fail
- **Issues Found**: _____
- **Rollback Required**: Yes / No

## 📝 Deployment Log Template

```
Date: YYYY-MM-DD HH:MM
Version/Commit: [commit hash]
Deployed By: [name]
Branch: main

Changes:
- [List major changes]
- [...]

Pre-deployment Checks: ✓ Pass / ✗ Fail
Build Status: ✓ Pass / ✗ Fail
Deploy Status: ✓ Pass / ✗ Fail
Post-deployment Verification: ✓ Pass / ✗ Fail

Issues:
- [List any issues found]
- [...]

Resolution:
- [How issues were resolved]
- [...]

Notes:
- [Any additional notes]
```

## 🎯 Best Practices

1. **Always test locally first**
   - Never push untested code
   - Use `mkdocs serve` to preview

2. **Use descriptive commit messages**
   - Clear description of changes
   - Reference issues if applicable

3. **Deploy during low-traffic times**
   - Minimize impact on users
   - Easier to monitor

4. **Monitor the pipeline**
   - Don't push and leave
   - Watch for errors

5. **Keep deployments small**
   - Easier to debug
   - Faster rollback if needed

6. **Document changes**
   - Update changelog
   - Note breaking changes

7. **Test on multiple devices**
   - Desktop and mobile
   - Different browsers

8. **Have a rollback plan**
   - Know how to revert
   - Keep previous version accessible

9. **Communicate with team**
   - Notify about deployments
   - Share any issues

10. **Learn from issues**
    - Document problems
    - Improve process

## ✅ Final Checklist

Before marking deployment as complete:

- [ ] All pre-deployment checks passed
- [ ] Deployment completed successfully
- [ ] Post-deployment verification passed
- [ ] No critical issues found
- [ ] Team notified (if applicable)
- [ ] Documentation updated (if needed)
- [ ] Deployment logged
- [ ] Monitoring in place

## 📞 Emergency Contacts

- **GitLab Support**: [link]
- **Team Lead**: [contact]
- **Technical Support**: [contact]

## 🔗 Useful Links

- GitLab Project: [URL]
- Live Site: [URL]
- Pipeline: [URL]
- Documentation: [URL]

---

**Remember**: It's better to delay deployment and fix issues than to deploy broken code!
