"""Independent release checks: rederive metrics, trace source and inspect deliverables."""
import argparse
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "artifacts/public"


def verify(science_only=False):
    m = json.loads((PUBLIC / "benchmark.json").read_text())
    assert m["protocolVersion"] == "2.0.0"
    assert m["gitDirty"] is False and m["identityCapturedBeforeWrites"] is True
    for relative, expected in m["sourceFilesSha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode()).hexdigest()
        assert actual == expected, f"Scientific source changed: {relative}"
    for d in m["datasets"]:
        name = d["dataset"]
        assert json.loads((PUBLIC / f"{name}_benchmark.json").read_text()) == d
        folds = pd.read_csv(PUBLIC / f"{name}_fold_results.csv")
        for r in d["results"]:
            group = folds[(folds["size"] == r["size"]) & (folds.method == r["method"])]
            assert len(group) == m["folds"]*m["repeats"]
            np.testing.assert_allclose(group.balancedAccuracy.mean(), r["balancedAccuracyMean"], atol=1e-12)
            np.testing.assert_allclose(group.baliRecall.mean(), r["baliRecallMean"], atol=1e-12)
        panels = pd.read_csv(PUBLIC / f"{name}_panel_candidates.csv")
        for size, group in panels.groupby("panelSize"):
            assert len(group) == size and group.markerId.is_unique
            for _, chrom in group.groupby("chromosome"):
                assert (np.diff(np.sort(chrom.position)) >= m["parameters"]["minDistanceBp"]).all()
        pred = pd.read_csv(PUBLIC / f"{name}_heldout_predictions.csv", dtype={"sampleId": str})
        assert len(pred) == d["nSamples"]*m["repeats"]
        assert (pred.groupby("sampleId").size() == m["repeats"]).all()
        for r in d["atypicalSamples"]:
            p = pred[pred.sampleId == r["sampleId"]]
            assert int((p.observedBali != p.predictedBali).sum()) == r["misclassifiedRepeats"]
        af = pd.read_csv(PUBLIC / f"{name}_ancestry_folds.csv")
        ap = pd.read_csv(PUBLIC / f"{name}_ancestry_simulated_predictions.csv")
        for r in d["ancestry"]["results"]:
            g = af[(af.donorBreed == r["donorBreed"]) & (af["size"] == r["size"]) & (af.method == r["method"])]
            np.testing.assert_allclose(g.mae.mean(), r["maeMean"], atol=1e-12)
            assert r["achievedSpecificityMean"] >= .95
            if r["method"] != "Random-mean" and r["size"] in [8, 48, 200]:
                p = ap[(ap.donorBreed == r["donorBreed"]) & (ap["size"] == r["size"]) & (ap.method == r["method"]) & (ap.generation != "BALI-control")]
                means = p.assign(error=(p.estimatedQ-p.pedigreeQ).abs()).groupby("fold").error.mean()
                np.testing.assert_allclose(means.mean(), r["maeMean"], atol=1e-12)
        assert len(d["population"]["points"]) == d["population"]["nAnimals"]
        assert d["population"]["predictiveValidation"] is False
    for path in PUBLIC.glob("*.json"):
        json.loads(path.read_text(), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"Nonfinite JSON {path}: {value}")))
    # The source snapshot should not redistribute organizer materials/operational secrets.
    assert sorted(p.name for p in (ROOT / "DriveKit").iterdir()) == ["README.md"]
    assert not re.search(r"url\s*=\s*/apps/dashboard", (ROOT / "apps/dashboard/package_static.py").read_text())
    if not science_only:
        from pypdf import PdfReader
        pptx = ROOT / "artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pptx"
        pdf = ROOT / "artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pdf"
        with zipfile.ZipFile(pptx) as z:
            slides = [p for p in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", p)]
            assert len(slides) == 11
            text = " ".join(z.read(p).decode() for p in slides)
            assert not re.search(r"\b(?:undefined|NaN|Infinity)\b", text)
            ns = {"c": "http://schemas.openxmlformats.org/drawingml/2006/chart"}
            chart_name = next(p for p in z.namelist() if p.endswith("/chart1.xml"))
            chart = ET.fromstring(z.read(chart_name))
            source = next(d for d in m["datasets"] if d["dataset"] == "dryad")["ancestry"]["results"]
            for series in chart.findall(".//c:ser", ns):
                method = series.find("c:tx//c:v", ns).text
                actual = [float(p.text) for p in series.findall("c:val//c:numCache/c:pt/c:v", ns)]
                expected = [round(r["maeMean"], 3) for r in sorted(source, key=lambda x: x["size"]) if r["method"] == method and r["donorBreed"] == "ONG"]
                np.testing.assert_allclose(actual, expected, atol=1e-12)
        pages = PdfReader(pdf).pages
        assert len(pages) == 11
        assert not re.search(r"\b(?:undefined|NaN|Infinity)\b", " ".join(p.extract_text() for p in pages))
        pdf_manifest = json.loads((PUBLIC / "pitch_pdf_render_manifest.json").read_text())
        assert hashlib.sha256(pdf.read_bytes()).hexdigest() == pdf_manifest["pdfSha256"]
        assert hashlib.sha256(pptx.read_bytes()).hexdigest() == pdf_manifest["pptxSha256"]
        assert (ROOT / "artifacts/demo/BantengPanel_demo_2min.mp4").stat().st_size > 100000
        import imageio_ffmpeg
        reader = imageio_ffmpeg.read_frames(str(ROOT / "artifacts/demo/BantengPanel_demo_2min.mp4"))
        video_info = next(reader)
        reader.close()
        assert abs(video_info["duration"]-120) < .1
        with zipfile.ZipFile(ROOT / "artifacts/demo/BantengPanel_offline.zip") as z:
            assert z.testzip() is None
            assert "apps/dashboard/index.html" in z.namelist()
            assert "artifacts/demo/BantengPanel_demo_2min.mp4" in z.namelist()
            assert json.loads(z.read("artifacts/public/benchmark.json"))["gitCommit"] == m["gitCommit"]
        facts = json.loads((PUBLIC / "pitch_facts.json").read_text())
        assert facts["sourceCommit"] == m["gitCommit"] and sum(facts["timingsSeconds"]) == 340
        assert facts["business"]["customerEvidence"]["customerInterviews"] == 0
    return {"status": "passed", "scope": "science" if science_only else "full_release", "sourceCommit": m["gitCommit"],
            "datasets": [d["dataset"] for d in m["datasets"]], "humanValidation": "pending_interviews_roles_rehearsal_submission"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--science-only", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.science_only), indent=2))
