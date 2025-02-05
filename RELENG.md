# Chainlit Community Release Engineering Guide

## Version Management Strategy

### Monorepo Versioning with Hatch
- **Hatch-managed versions** using dynamic source from `__init__.py`
- Configure per-package in `pyproject.toml`:
  ```toml
  [tool.hatch.version]
  source = "regex"
  path = "src/chainlit_<package>/__init__.py"
  pattern = '^__version__ = "(.+)"$'
  ```

### Version Bumping Protocol
For each package (e.g. `chainlit-sqlalchemy`):
```bash
# Bump specific version
hatch version 1.2.3

# Semantic increments
hatch version minor  # 0.1.0 → 0.2.0
hatch version micro  # 0.1.0 → 0.1.1 
hatch version major,rc  # 1.0.0 → 2.0.0rc0
hatch version release  # 2.0.0rc0 → 2.0.0
```

## Package Release Process

### Pre-Release Validation
1. Verify workspace integrity:
   ```bash
   uv sync --all-packages
   uv run pip check
   ```

2. Run full test matrix:
   ```bash
   ./scripts/ci.sh
   ```

### Build Process Updates
```bash
# Ensure Hatch recognizes dynamic version
uv pip install hatch

# Build with version from Hatch
uv build --no-sources --strict \
  --exclude-extras all \
  --build-constraint ../../constraints.txt
```

Key flags:
- `--no-sources`: Ignore workspace sources
- `--strict`: Fail on dependency resolution issues
- `--exclude-extras`: Build base package only

### Publishing Workflow
1. Configure credentials:
   ```bash
   export UV_PUBLISH_TOKEN="pypi-xxxxxxxx"
   ```

2. Dry run validation:
   ```bash
   uv publish --dry-run --strict \
     --index-url https://upload.pypi.org/legacy/
   ```

3. Publish package:
   ```bash
   uv publish --no-sources --strict \
     --index-url https://upload.pypi.org/legacy/
   ```

4. Verify publication:
   ```bash
   uv pip install --force-reinstall chainlit-sqlalchemy==1.2.3
   uv run python -c "from chainlit_sqlalchemy import __version__; print(__version__)"
   ```

## Workspace Management

### Cross-Package Dependencies
When package A (e.g. `pytest`) depends on package B (e.g. `sqlalchemy`):
1. Release dependency first:
   ```bash
   uv publish -p packages/data_layers/sqlalchemy
   ```

2. Update dependent package constraints:
   ```toml
   # packages/pytest/pyproject.toml
   dependencies = [
     "chainlit-sqlalchemy>=1.2.3,<2.0.0"
   ]
   ```

### Batch Publishing
Publish all modified packages:
```bash
uv publish --workspace \
  --index-url https://upload.pypi.org/legacy/ \
  --strict
```

## Security & Compliance

### PyPI Configuration
```toml
# Single token in root .env
UV_PUBLISH_TOKEN="pypi-xxxxxxxx"
```

### Dependency Pinning
Maintain `constraints.txt` in root:
```bash
uv pip compile requirements.txt --output-file constraints.txt \
  --generate-hashes --no-sources
```

## Post-Release Actions

1. Tag releases with package prefixes:
   ```bash
   git tag sqlalchemy/v1.2.3 -m "chainlit-sqlalchemy 1.2.3"
   git push origin sqlalchemy/v1.2.3
   ```

## Troubleshooting

Common Issues | Resolution 
---|---
`BuildError: Missing build dependency` | `uv pip install "setuptools>=65" --resolution=lowest-direct`
`PublishError: Invalid API token` | Verify token has `pypi-` prefix and package scope
`VersionConflict` | Run `uv sync --all-packages --upgrade`
`FileExistsError` | Remove `dist/` and `build/` directories before rebuilding

---

[uv Publishing Reference](https://docs.astral.sh/uv/guides/publish/) | 
[PEP 440 Spec](https://peps.python.org/pep-0440/)
