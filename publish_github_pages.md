# Publishing the Quarto case study to GitHub Pages (local workflow)

This repository publishes the **case study website** from a locally rendered Quarto build to the `gh-pages` branch.

The rendered site is built from curated wrapper pages (`*.qmd`) that include selected markdown files (e.g. `public_artifact.md`, `docs/architecture_and_workflows.md`). This is intentional: it prevents accidental publication of runtime artifacts or sensitive data directories.

---

## One-time setup (GitHub)

1. In GitHub repo settings, configure Pages to serve from:\n+   - **Branch:** `gh-pages`\n+   - **Folder:** `/ (root)`\n+
2. Ensure your `gh-pages` branch exists (you can create it during first publish).

---

## Local publish steps

### 1) Render the site

From the repo root:

```bash
quarto render
```

This produces `_site/` locally.

### 2) Publish `_site/` to `gh-pages`

This workflow commits only the rendered output to the `gh-pages` branch root.

```bash
# from main (or your working branch)
# create gh-pages once (first time only)
git show-ref --verify --quiet refs/heads/gh-pages || git checkout --orphan gh-pages
git show-ref --verify --quiet refs/heads/gh-pages || (git reset --hard && git commit --allow-empty -m "Initialize gh-pages" && git push origin gh-pages)
git checkout -

# create a worktree for gh-pages
git worktree add /tmp/classroom-manager-gh-pages gh-pages

# Render on your working tree (main)
quarto render

# Copy rendered output into the gh-pages worktree
rsync -a --delete _site/ /tmp/classroom-manager-gh-pages/

# Ensure GitHub Pages serves files without Jekyll processing
touch /tmp/classroom-manager-gh-pages/.nojekyll

cd /tmp/classroom-manager-gh-pages
git add -A
git commit -m "Publish site" || true
git push origin gh-pages
```

After push, GitHub Pages will update at `https://<username>.github.io/<repo>/`.

---

## Safety rules (do not publish)

Do not include these directories in the Quarto project output or navigation:

- `data/students/`
- `deliverables/`
- `results/`

The Quarto site is curated to avoid them; keep it that way.

