import io
import json
import zipfile

import numpy as np
import pandas as pd
import pytest

from bantengpanel import analysis, ancestry
from bantengpanel.data import encode_alleles, safe_extract


def test_encode_missing_and_dosage():
    assert encode_alleles(np.array([0, 1, 1, 2]), np.array([0, 1, 2, 2])).tolist() == [-1, 2, 1, 0]
    with pytest.raises(ValueError, match="Partial missing"):
        encode_alleles(np.array([0]), np.array([1]))
    with pytest.raises(ValueError, match="Unsupported"):
        encode_alleles(np.array([3]), np.array([1]))


def test_extract_rejects_parent_traversal(tmp_path):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as z:
        z.writestr("../escaped.txt", "no")
    with zipfile.ZipFile(stream) as z, pytest.raises(ValueError, match="Unsafe"):
        safe_extract(z, tmp_path / "inside")
    assert not (tmp_path / "escaped.txt").exists()


def test_panel_selection_ignores_heldout_values():
    x = np.array([[2, 0, 2, 0], [2, 0, 1, 1], [0, 2, 1, 1], [0, 2, 0, 2], [0, 0, 0, 0]], dtype=np.int8)
    y = np.array([1, 1, 0, 0, 1])
    markers = pd.DataFrame({"markerId": list("abcd"), "chromosome": [1]*4, "position": [0, 300000, 600000, 900000]})
    first = analysis.select_training_panels(x, y, markers, np.arange(4), 2, 250000, .9, .01)
    x[4] = [2, 2, 2, 2]
    y[4] = 0
    second = analysis.select_training_panels(x, y, markers, np.arange(4), 2, 250000, .9, .01)
    for a, b in zip(first, second):
        np.testing.assert_array_equal(a, b)


def test_random_panel_enforces_spacing():
    m = pd.DataFrame({"markerId": list("abcde"), "chromosome": [1]*5, "position": [0, 100, 300000, 300100, 600000]})
    panel = analysis.random_spaced_panel(np.arange(5), m, 3, 250000, np.random.default_rng(1))
    assert len(panel) == 3
    assert np.diff(np.sort(m.iloc[panel].position.to_numpy())).min() >= 250000


def test_absent_bali_genotypes_do_not_become_zero_allele_frequency():
    # A very small minority can have no calls even though pooled call rate passes.
    x = np.array([[-1, 2]] + [[1, 0]]*19, dtype=np.int8)
    y = np.array([1] + [0]*19)
    call, maf, delta = analysis._scores(x, y)
    assert call[0] >= .9 and maf[0] >= .01
    assert np.isnan(delta[0]) and np.isfinite(delta[1])


def test_q_estimator_identifies_reference_endpoints_and_missing():
    p = np.full(200, .99)
    other = np.full(200, .01)
    g = np.array([np.full(200, 2), np.zeros(200), np.ones(200), np.full(200, -1)])
    q = ancestry.estimate_q(g, p, other)
    np.testing.assert_allclose(q[:3], [1, 0, .5], atol=.01)
    assert np.isnan(q[3])


def test_mendelian_generations_have_expected_dosage():
    rng = np.random.default_rng(3)
    bali, donor = np.full((4, 2000), 2, dtype=np.int8), np.zeros((3, 2000), dtype=np.int8)
    children = ancestry.simulate_generations(bali, donor, np.ones(2000), np.zeros(2000), 200, rng)
    assert np.all(children["F1"] == 1)
    assert children["BC1"].mean()/2 == pytest.approx(.75, abs=.005)
    assert children["BC2"].mean()/2 == pytest.approx(.875, abs=.005)


def test_run_identity_is_captured_before_outputs(monkeypatch, tmp_path):
    for folder in ["bantengpanel", "configs", "data/raw", "data/processed"]:
        (tmp_path / folder).mkdir(parents=True, exist_ok=True)
    (tmp_path / "configs/mvp.yaml").write_text("seed: 1")
    (tmp_path / "pyproject.toml").write_text("# fixture")
    (tmp_path / "data/raw/manifest.json").write_text("{}")
    (tmp_path / "data/processed/summary.json").write_text("{}")
    monkeypatch.setattr(analysis, "ROOT", tmp_path)
    monkeypatch.setattr(analysis, "PROCESSED", tmp_path / "data/processed")
    dirty = {"value": False}
    monkeypatch.setattr(analysis, "_git_dirty", lambda: dirty["value"])
    monkeypatch.setattr(analysis, "_git_commit", lambda: "source-before-write")
    def fake_benchmark(*args, **kwargs):
        dirty["value"] = True
        return {"dataset": args[0]}
    monkeypatch.setattr(analysis, "benchmark", fake_benchmark)
    monkeypatch.setattr(analysis, "OUT", tmp_path)
    result = analysis.run_all(include_extensions=False)
    assert result["gitDirty"] is False
    assert result["gitCommit"] == "source-before-write"
    assert json.loads((tmp_path / "benchmark.json").read_text())["gitDirty"] is False
