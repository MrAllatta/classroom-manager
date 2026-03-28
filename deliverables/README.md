# Deliverables

Generated outputs, exports, and **snapshots** — not the system’s canonical store.

**Canonical structured data** lives under `data/` (e.g. course scope: `data/courses/algebra_1/scope.yaml`). When a deliverable becomes authoritative, **merge into `data/`** and keep the file here as a dated or provenance record if useful.

Files in this folder may duplicate `data/` on purpose (same content, snapshot semantics). Example: `scope_ALG1_fullyear.json` / `.md` remain as snapshots alongside the YAML scope in `data/`.

As this folder grows, prefer light structure (subfolders by course, type, or date) rather than one flat list of everything.
