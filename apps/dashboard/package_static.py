"""Package the dashboard and public evidence as a self-contained static site."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "out"


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)


def main() -> None:
    public = ROOT / "artifacts/public"
    if not (public / "dryad_benchmark.json").exists() or not (public / "figshare_benchmark.json").exists():
        raise FileNotFoundError("Run `python -m bantengpanel.cli run` before packaging the static dashboard")
    # Both are generated outputs at exact verified workspace paths, never arbitrary CLI paths.
    assert OUT.resolve() == ROOT.resolve() / "out"
    stale = (ROOT / "apps/dashboard/out").resolve()
    assert stale == ROOT.resolve() / "apps/dashboard/out"
    for target in (OUT, stale):
        if target.exists():
            shutil.rmtree(target)
    dashboard = OUT / "apps/dashboard"
    dashboard.mkdir(parents=True, exist_ok=True)
    for filename in ("index.html", "app.js", "style.css"):
        shutil.copy2(ROOT / "apps/dashboard" / filename, dashboard / filename)
    copy_tree(public, OUT / "artifacts/public")
    docs_out = OUT / "docs"
    docs_out.mkdir(parents=True, exist_ok=True)
    for filename in ("SCIENTIFIC_PROTOCOL.md", "DATA_PROVENANCE.md", "RUNBOOK.md", "BUSINESS_MODEL.md", "CONTRIBUTIONS.md", "AUDIT_IMPLEMENTATION_STATUS.md"):
        shutil.copy2(ROOT / "docs" / filename, docs_out / filename)
    (OUT / "index.html").write_text('<!doctype html><html lang="id"><title>BantengPanel</title><meta http-equiv="refresh" content="0; url=apps/dashboard/"><a href="apps/dashboard/">Buka BantengPanel</a></html>', encoding="utf-8")
    for filename in ("BantengPanel_GENOHACK_2026_Audited.pdf", "BantengPanel_GENOHACK_2026_Audited.pptx"):
        source = ROOT / "artifacts/pitch" / filename
        if source.exists():
            dest = OUT / "artifacts/pitch" / filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    video = ROOT / "artifacts/demo/BantengPanel_demo_2min.mp4"
    if video.exists():
        destination = OUT / "artifacts/demo" / video.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, destination)
    (OUT / "README_OFFLINE.md").write_text("# BantengPanel offline\n\nJalankan `python -m http.server 8000` dari folder ini, lalu buka http://localhost:8000/apps/dashboard/ . Tidak perlu data mentah atau internet. Diagram, metrik, PDF dan video adalah artefak riset; tidak memverifikasi kemurnian ternak.\n", encoding="utf-8")
    (OUT / "launch_offline.cmd").write_text('@echo off\ncd /d "%~dp0"\nstart "" "http://localhost:8000/apps/dashboard/"\npython -m http.server 8000\n', encoding="utf-8")
    if (ROOT / "apps/rehearsal").exists():
        copy_tree(ROOT / "apps/rehearsal", OUT / "rehearsal")
    # Build the offline archive before adding it to the served bundle, avoiding recursion.
    offline = ROOT / "artifacts/demo/BantengPanel_offline.zip"
    offline.parent.mkdir(parents=True, exist_ok=True)
    if video.exists() and (OUT / "artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pdf").exists():
        with zipfile.ZipFile(offline, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(OUT.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(OUT).as_posix())
        shutil.copy2(offline, OUT / "artifacts/demo" / offline.name)
    print(f"Static site ready: {OUT}")


if __name__ == "__main__":
    main()
