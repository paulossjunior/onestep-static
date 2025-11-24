# GitLab CI/CD Setup for MkDocs

## Overview

This repository uses GitLab CI/CD to automatically build and deploy the MkDocs documentation site to GitLab Pages.

## Pipeline Stages

### 1. Build Stage
- **Job: `build`**
  - Runs on: `main`, `master`, `develop` branches
  - Installs Python dependencies from `requirements.txt`
  - Builds the MkDocs site with strict mode
  - Creates artifacts that expire in 1 hour
  - Output: `onestep-static/site/` directory

- **Job: `test_build`**
  - Runs on: merge requests (except main/master)
  - Tests that the documentation builds successfully
  - Does not deploy

### 2. Deploy Stage
- **Job: `pages`**
  - Runs on: `main`, `master` branches only
  - Copies built site to `public/` directory
  - Deploys to GitLab Pages
  - Creates production environment

## GitLab Pages URL

After the first successful deployment, your site will be available at:

```
https://<namespace>.gitlab.io/<project-name>
```

Where:
- `<namespace>` is your GitLab username or group name
- `<project-name>` is your repository name

## Configuration

### Enable GitLab Pages

1. Go to your GitLab project
2. Navigate to **Settings** → **Pages**
3. Ensure Pages is enabled
4. After the first pipeline runs, your site URL will appear here

### Pipeline Variables

The pipeline uses these GitLab CI variables:
- `CI_PROJECT_NAMESPACE` - Your GitLab namespace
- `CI_PROJECT_NAME` - Your project name
- `CI_PROJECT_DIR` - Project directory path

### Cache Configuration

The pipeline caches:
- `.cache/pip` - Python package cache
- `venv/` - Virtual environment

This speeds up subsequent pipeline runs.

## Local Testing

Before pushing, you can test the build locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Build the site
cd onestep-static
mkdocs build --strict --verbose

# Serve locally
mkdocs serve
```

Visit `http://127.0.0.1:8000` to preview your site.

## Triggering Deployments

### Automatic Deployment
- Push to `main` or `master` branch
- Pipeline will automatically build and deploy

### Manual Deployment
1. Go to **CI/CD** → **Pipelines**
2. Click **Run Pipeline**
3. Select the branch (main/master)
4. Click **Run Pipeline**

## Monitoring

### View Pipeline Status
- Go to **CI/CD** → **Pipelines**
- Click on a pipeline to see job details
- View logs for each job

### View Deployment Status
- Go to **Deployments** → **Environments**
- Click on **production** to see deployment history
- Access the live site from the environment page

## Troubleshooting

### Build Fails
1. Check the build job logs
2. Verify all files referenced in `mkdocs.yml` exist
3. Test locally with `mkdocs build --strict`

### Pages Not Updating
1. Ensure the pipeline completed successfully
2. Check that the `pages` job ran
3. Clear browser cache
4. Wait a few minutes for GitLab Pages to update

### Missing Dependencies
1. Verify `requirements.txt` includes all needed packages
2. Check Python version compatibility (using 3.11)
3. Review job logs for import errors

## Customization

### Change Python Version
Edit `.gitlab-ci.yml`:
```yaml
image: python:3.12-slim  # Change version here
```

### Add Build Steps
Add to the `build` job script:
```yaml
script:
  - pip install -r requirements.txt
  - python scripts/generate_data.py  # Custom script
  - cd onestep-static
  - mkdocs build --strict --verbose
```

### Deploy to Custom Domain
1. Configure custom domain in GitLab Pages settings
2. Add DNS records as instructed by GitLab
3. Update the `url` in the `pages` job environment

## Security

### Protected Branches
Consider protecting your main branch:
1. Go to **Settings** → **Repository** → **Protected Branches**
2. Protect `main` or `master`
3. Set allowed to merge/push permissions

### Pipeline Permissions
The pipeline runs with the permissions of the user who triggered it.

## Performance

### Build Time
- First build: ~2-3 minutes (installing dependencies)
- Subsequent builds: ~1-2 minutes (using cache)

### Optimization Tips
1. Cache is enabled for pip packages
2. Artifacts expire after 1 hour to save storage
3. Test builds on MRs don't create artifacts

## Additional Resources

- [GitLab Pages Documentation](https://docs.gitlab.com/ee/user/project/pages/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/)

## Support

For issues with:
- **GitLab CI/CD**: Check GitLab documentation or project issues
- **MkDocs**: Check MkDocs documentation
- **This project**: Open an issue in this repository
