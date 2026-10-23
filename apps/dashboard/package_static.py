"""Package the dashboard and public evidence as a self-contained static site."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "out"


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)


def main() -> None:
    public = ROOT / "artifacts/public"
    if not (public / "dryad_benchmark.json").exists() or not (public / "figshare_benchmark.json").exists():
        raise FileNotFoundError("Run `python -m bantengpanel.cli run` before packaging the static dashboard")
    dashboard = OUT / "apps/dashboard"
    dashboard.mkdir(parents=True, exist_ok=True)
    for filename in ("index.html", "app.js", "style.css"):
        shutil.copy2(ROOT / "apps/dashboard" / filename, dashboard / filename)
    copy_tree(public, OUT / "artifacts/public")
    docs_out = OUT / "docs"
    docs_out.mkdir(parents=True, exist_ok=True)
    for filename in ("SCIENTIFIC_PROTOCOL.md", "DATA_PROVENANCE.md", "RUNBOOK.md"):
        shutil.copy2(ROOT / "docs" / filename, docs_out / filename)
    (OUT / "index.html").write_text('<!doctype html><meta http-equiv="refresh" content="0; url=/apps/dashboard/">', encoding="utf-8")
    print(f"Static site ready: {OUT}")


if __name__ == "__main__":
    main()
