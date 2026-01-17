# Setting up PyPI API Token in GitHub Repository Secrets

To enable automated publishing, you need to add your PyPI API token to the GitHub repository secrets.

## Steps:

### 1. Go to Repository Settings
Navigate to: https://github.com/jqueguiner/num2words/settings/secrets/actions

### 2. Add New Repository Secret
- Click "New repository secret"
- Name: `PYPI_API_TOKEN`
- Value: Your PyPI API token (starts with `pypi-AgEIc...`)

### 3. Verify Secret is Added
The secret should appear in the list as `PYPI_API_TOKEN` with a green checkmark.

## How the Automation Works:

### Automatic Publishing (python-publish.yml)
- **Trigger**: When CI tests pass on master branch
- **Process**: 
  1. Waits for CI workflow to complete successfully
  2. Checks if current version exists on PyPI
  3. If version exists, auto-increments patch version
  4. Builds and publishes package to PyPI
  5. Commits version bump back to repository

### Manual Publishing (manual-publish.yml)
- **Trigger**: Manual workflow dispatch from GitHub Actions tab
- **Options**: Choose version increment (patch/minor/major)
- **Use Case**: For immediate releases or when automation needs override

## Testing the Setup:
1. Make any small change to the codebase
2. Create a PR and merge it to master
3. Watch the GitHub Actions tab for automatic workflows
4. Check https://pypi.org/project/num2words2/ for the new package version

## Security Notes:
- The API token is stored securely in GitHub Secrets
- Only repository maintainers can view/edit secrets
- Workflows run in isolated environments
- Token is never exposed in logs