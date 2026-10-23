"""Acquisition and strict source-specific genotype parsers. No allele harmonization."""
from __future__ import annotations

import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
PROCESSED = ROOT / "data/processed"
FIGSHARE_URL = "https://ndownloader.figshare.com/files/25037732"
FIGSHARE_MD5 = "13f07b9bf8a0cb1e61d689cce08b30ec"
DRYAD_MD5 = "0377a330590e4e8af07c1ebe416c975a"
# The source's codebook identifies the five breeds. Keep source codes and
# labels together so downstream reports can show the exact mapping.
BREEDS = {"1": "MAD", "2": "JABRES", "3": "BALI", "4": "ONG", "5": "KBO"}


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(z: zipfile.ZipFile, target: Path) -> None:
    target = target.resolve()
    for info in z.infolist():
        dest = (target / info.filename).resolve()
        if not dest.is_relative_to(target):
            raise ValueError(f"Unsafe archive path: {info.filename}")
        if info.filename.startswith("__MACOSX/") or info.is_dir():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        with z.open(info) as source, dest.open("wb") as out:
            shutil.copyfileobj(source, out)


def fetch(dryad_archive: Path | None = None) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    fig = RAW / "figshare/data_package.zip"
    fig.parent.mkdir(parents=True, exist_ok=True)
    if fig.exists() and digest(fig, "md5") != FIGSHARE_MD5:
        fig.unlink()
    if not fig.exists():
        partial = fig.with_suffix(".part")
        with urllib.request.urlopen(FIGSHARE_URL, timeout=60) as r, partial.open("wb") as f:
            shutil.copyfileobj(r, f)
        if digest(partial, "md5") != FIGSHARE_MD5:
            partial.unlink()
            raise ValueError("Figshare checksum mismatch")
        partial.replace(fig)
    if digest(fig, "md5") != FIGSHARE_MD5:
        raise ValueError("Figshare checksum mismatch after download")
    with zipfile.ZipFile(fig) as z:
        safe_extract(z, fig.parent)
    dryad_archive = dryad_archive or ROOT / "doi_10_5061_dryad_th092__v20150214.zip"
    dry = RAW / "dryad/WorldWideCattleDryad.zip"
    dry.parent.mkdir(parents=True, exist_ok=True)
    if dry.exists() and digest(dry, "md5") != DRYAD_MD5:
        dry.unlink()
    if not dry.exists():
        if not dryad_archive.exists():
            raise FileNotFoundError(f"Dryad archive not found: {dryad_archive}")
        with zipfile.ZipFile(dryad_archive) as z:
            nested = next((n for n in z.namelist() if n.endswith("WorldWideCattleDryad.zip")), None)
            if nested:
                with z.open(nested) as src, dry.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
            else:
                shutil.copy2(dryad_archive, dry)
    if digest(dry, "md5") != DRYAD_MD5:
        raise ValueError("Dryad checksum mismatch")
    with zipfile.ZipFile(dry) as z:
        safe_extract(z, dry.parent)
    manifest = {
        "figshare": {"doi": "10.6084/m9.figshare.13083587.v1", "url": FIGSHARE_URL, "license": "CC-BY-4.0", "sha256": digest(fig), "md5": FIGSHARE_MD5},
        "dryad": {"doi": "10.5061/dryad.th092", "license": "CC0-1.0", "sha256": digest(dry), "md5": DRYAD_MD5},
    }
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def encode_alleles(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if not np.isin(a, [0, 1, 2]).all() or not np.isin(b, [0, 1, 2]).all():
        raise ValueError("Unsupported allele code")
    partial = (a == 0) != (b == 0)
    if partial.any():
        raise ValueError("Partial missing genotype is unsupported")
    return np.where((a == 0) | (b == 0), -1, (a == 1).astype(np.int8) + (b == 1)).astype(np.int8)


def parse_figshare() -> tuple[np.ndarray, pd.DataFrame, pd.DataFrame]:
    base = RAW / "figshare"
    samples = pd.read_csv(base / "indiv_info.txt", sep=r"\s+", names=["sampleId", "breedCode"], dtype=str)
    samples["breed"] = samples.breedCode.map(BREEDS)
    if samples.breed.isna().any() or samples.sampleId.duplicated().any():
        raise ValueError("Ambiguous sample metadata")
    markers = pd.read_csv(base / "marker_info.txt", sep=r"\s+", names=["sourceId", "markerId", "chromosome", "position"])
    if markers.sourceId.duplicated().any() or markers.markerId.duplicated().any():
        raise ValueError("Duplicate marker metadata")
    sample_map = {v: i for i, v in enumerate(samples.sampleId)}
    marker_map = {v: i for i, v in enumerate(markers.sourceId)}
    x = np.full((len(samples), len(markers)), -9, dtype=np.int8)
    for chunk in pd.read_csv(base / "genotype.txt", sep=r"\s+", names=["snp", "sample", "a", "b"], chunksize=300000):
        si, mi = chunk["sample"].map(sample_map), chunk.snp.map(marker_map)
        if si.isna().any() or mi.isna().any():
            raise ValueError("Genotype refers to unknown sample or marker")
        si, mi = si.to_numpy(dtype=int), mi.to_numpy(dtype=int)
        keys = si * len(markers) + mi
        if len(np.unique(keys)) != len(keys) or (x[si, mi] != -9).any():
            raise ValueError("Duplicate sample-marker genotype")
        x[si, mi] = encode_alleles(chunk.a.to_numpy(), chunk.b.to_numpy())
    if (x == -9).any():
        raise ValueError("Incomplete rectangular genotype matrix")
    return x, samples, markers


def parse_dryad() -> tuple[np.ndarray, pd.DataFrame, pd.DataFrame]:
    base = RAW / "dryad/DataDryad"
    stem = "ww_cattle_dryad_20Sept2013"
    samples = pd.read_csv(base / f"{stem}.pedind", sep=r"\s+", names=["family", "sampleId", "father", "mother", "sex", "breed"], dtype=str)
    markers = pd.read_csv(base / f"{stem}.map", sep=r"\s+", names=["chromosome", "markerId", "cm", "position"])
    x = np.full((len(samples), len(markers)), -1, dtype=np.int8)
    row_count = 0
    with (base / f"{stem}.ped").open() as f:
        for i, line in enumerate(f):
            if i >= len(samples):
                raise ValueError("PED has more rows than population metadata")
            fields = line.split(maxsplit=6)
            if i >= len(samples) or fields[1] != samples.iloc[i].sampleId or fields[0] != samples.iloc[i].family:
                raise ValueError("PED and population metadata order differ")
            alleles = np.fromstring(fields[6], sep=" ", dtype=np.int8)
            if len(alleles) != 2 * len(markers):
                raise ValueError("PED marker count mismatch")
            x[i] = encode_alleles(alleles[::2], alleles[1::2])
            row_count += 1
    if row_count != len(samples):
        raise ValueError("PED sample count mismatch")
    # Composite IDs avoid collisions across families.
    samples["sampleId"] = samples.family + ":" + samples.sampleId
    if samples.sampleId.duplicated().any():
        raise ValueError("Duplicate Dryad sample identifiers")
    # Dryad repeats 25 marker IDs at the same coordinates, and their genotype
    # calls can disagree. Preserve every source column and make IDs explicit;
    # the same-position spacing rule prevents selecting duplicate loci together.
    markers["sourceMarkerId"] = markers["markerId"]
    copy_number = markers.groupby(["chromosome", "markerId", "position"], sort=False).cumcount()
    duplicated = markers.duplicated(["chromosome", "markerId", "position"], keep=False)
    markers.loc[duplicated, "markerId"] = markers.loc[duplicated, "markerId"] + "__copy" + (copy_number[duplicated] + 1).astype(str)
    return x, samples, markers


def prepare(sample_missing_max: float = 0.10) -> dict:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name, parser in [("figshare", parse_figshare), ("dryad", parse_dryad)]:
        print(f"Parsing {name}...", flush=True)
        x, samples, markers = parser()
        autosomal = pd.to_numeric(markers.chromosome, errors="coerce").between(1, 29).to_numpy()
        excluded_markers = int((~autosomal).sum())
        x, markers = x[:, autosomal], markers.loc[autosomal].reset_index(drop=True)
        sample_missing = (x < 0).mean(axis=1)
        keep = sample_missing <= sample_missing_max
        excluded = int((~keep).sum())
        x, samples = x[keep], samples.loc[keep].reset_index(drop=True)
        np.save(PROCESSED / f"{name}.npy", x)
        samples.to_csv(PROCESSED / f"{name}_samples.csv", index=False)
        markers.to_csv(PROCESSED / f"{name}_markers.csv", index=False)
        summary[name] = {"samples": len(samples), "excludedSamplesAboveMissingThreshold": excluded, "sampleMissingThreshold": sample_missing_max, "markers": len(markers), "excludedNonAutosomalMarkers": excluded_markers, "breeds": samples.breed.value_counts().to_dict(), "missingRate": float((x < 0).mean()), "sampleMissingMax": float((x < 0).mean(axis=1).max()), "assembly": "UMD3.1", "alleleCoding": "source minor/major" if name == "figshare" else "Illumina A/B"}
        print(json.dumps(summary[name]), flush=True)
    (PROCESSED / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def load(name: str = "figshare") -> tuple[np.ndarray, pd.DataFrame, pd.DataFrame]:
    return (np.load(PROCESSED / f"{name}.npy"), pd.read_csv(PROCESSED / f"{name}_samples.csv"), pd.read_csv(PROCESSED / f"{name}_markers.csv"))
