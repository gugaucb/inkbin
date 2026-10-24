# Release and Versioning Guide

This guide describes how versioning, Git tags, Docker Hub publishing, and GitHub Releases are automated in **Inkbin**.

---

## 1. Versioning Strategy (SemVer)

Inkbin follows [Semantic Versioning 2.0.0](https://semver.org/):
- **Major (`v1.0.0`)**: Incompatible API or breaking changes.
- **Minor (`v0.2.0`)**: Backwards-compatible new features (e.g. new encryption modes, options bar, UI components).
- **Patch (`v0.1.1`)**: Backwards-compatible bug fixes or minor documentation adjustments.

---

## 2. Release Automation Flow

When a Git tag matching `v*.*.*` (e.g., `v0.1.0`) is pushed to GitHub, two workflows run in parallel:

1. **Docker Publish & Push (`.github/workflows/docker-publish.yml`)**:
   - Builds multi-architecture container images (`linux/amd64`, `linux/arm64`).
   - Automatically tags and publishes to Docker Hub (`gugaucb/inkbin`):
     - `gugaucb/inkbin:latest`
     - `gugaucb/inkbin:0.1.0`
     - `gugaucb/inkbin:v0.1.0`
     - `gugaucb/inkbin:0.1`

2. **GitHub Release (`.github/workflows/release.yml`)**:
   - Creates an official GitHub Release linked to tag `v0.1.0`.
   - Automatically generates release notes and changelog from commit messages.

---

## 3. How to Release a New Version

### Step 1: Ensure Main is Clean and CI Passes
```bash
git checkout main
git pull origin main
pytest tests/ -v
ruff check .
ruff format --check .
```

### Step 2: Create and Push an Annotated Git Tag
```bash
# Example: Creating release v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0: Editorial Pastebin with client-side encryption and multi-arch Docker"
git push origin v0.1.0
```

### Step 3: Triggering via GitHub Actions (Manual Alternative)
You can also trigger a release manually without local Git CLI:
1. Go to the repository **Actions** tab on GitHub.
2. Select **GitHub Release**.
3. Click **Run workflow**, type the tag name (e.g. `v0.1.0`), and submit.
