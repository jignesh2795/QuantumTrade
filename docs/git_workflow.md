# Git Workflow for QuantumTrade

This document outlines the recommended Git workflow for contributing to the QuantumTrade project.

## Branching Strategy

### Main Branches

-   **main**: Production-ready code
-   **develop**: Integration branch for development

### Supporting Branches

-   **feature/\***: New features development
-   **bugfix/\***: Bug fixes
-   **release/\***: Release preparation
-   **hotfix/\***: Emergency production fixes

## Workflow Process

### Feature Development

1. Create a feature branch from `develop`:

    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b feature/your-feature-name
    ```

2. Develop your feature with regular commits:

    ```bash
    git add .
    git commit -m "feat: add new trading strategy"
    ```

3. Push your branch to remote:

    ```bash
    git push origin feature/your-feature-name
    ```

4. Create a Pull Request to merge into `develop`

### Bug Fixes

1. Create a bugfix branch from `develop`:

    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b bugfix/issue-description
    ```

2. Fix the bug and commit:

    ```bash
    git add .
    git commit -m "fix: resolve portfolio calculation error"
    ```

3. Push and create Pull Request

### Release Process

1. Create release branch from `develop`:

    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b release/v1.2.0
    ```

2. Finalize release (version bumps, documentation)
3. Merge to `main` and `develop`
4. Tag the release

### Hotfix Process

1. Create hotfix branch from `main`:

    ```bash
    git checkout main
    git pull origin main
    git checkout -b hotfix/critical-fix
    ```

2. Implement fix and test
3. Merge to `main` and `develop`
4. Tag new patch version

## Commit Message Guidelines

### Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Commit Types

-   **feat**: New feature
-   **fix**: Bug fix
-   **docs**: Documentation changes
-   **style**: Code formatting, missing semicolons, etc.
-   **refactor**: Code refactoring
-   **test**: Adding or updating tests
-   **chore**: Build process, auxiliary tools changes

### Examples

```
feat(trading): add Bollinger Bands strategy

Implement Bollinger Bands trading strategy with configurable parameters

Closes #123
```

```
fix(portfolio): correct PnL calculation

Fix profit and loss calculation for short positions

Fixes #456
```

## Pull Request Process

### Before Creating PR

1. Ensure branch is up to date with target branch
2. Run all tests and ensure they pass
3. Check code quality and formatting
4. Update documentation if needed

### PR Description Template

```
## Description
Brief description of changes

## Related Issue
Closes #issue-number

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project standards
- [ ] Documentation updated
- [ ] Tests pass
```

## Code Review Guidelines

### Reviewer Responsibilities

1. Check code quality and best practices
2. Verify tests are adequate
3. Ensure documentation is updated
4. Confirm security considerations
5. Validate performance implications

### Author Responsibilities

1. Respond to all review comments
2. Make requested changes
3. Re-request review after changes
4. Merge after approval

## Merge Strategies

### Fast-forward Merge

-   Used for simple feature branches
-   Maintains linear history

### Squash and Merge

-   Used for complex feature branches
-   Creates single commit in target branch
-   Recommended for most PRs

### Merge Commit

-   Used for releases and hotfixes
-   Preserves complete history

## Tagging and Versioning

### Semantic Versioning

-   **MAJOR**: Breaking changes
-   **MINOR**: New features (backward compatible)
-   **PATCH**: Bug fixes (backward compatible)

### Tag Format

```
v1.2.3
```

## Best Practices

### General

1. Commit early and often
2. Write descriptive commit messages
3. Keep branches focused on single purpose
4. Delete branches after merging
5. Regularly sync with upstream branches

### Conflict Resolution

1. Pull latest changes from target branch
2. Resolve conflicts locally
3. Test thoroughly after resolution
4. Commit resolution and push

### Security

1. Never commit sensitive information
2. Use .gitignore for secrets
3. Regularly audit commit history
4. Use signed commits for releases

## Troubleshooting

### Common Issues

1. **Merge conflicts**: Pull latest changes and resolve manually
2. **Detached HEAD**: Checkout appropriate branch
3. **Permission denied**: Check repository access rights
4. **Large files**: Use Git LFS for large assets

### Recovery

1. **Accidental commits**: Use `git reset` to undo
2. **Lost commits**: Use `git reflog` to recover
3. **Wrong branch**: Use `git cherry-pick` to move commits
