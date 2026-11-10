"""Tes logika murni alat GT video penuh (tanpa GUI)."""
import importlib.util, sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py"); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod); return mod


cmp = _load("compare_full_count")
ann = _load("annotate_full")


def test_match_one_to_one_and_unmatched() -> None:
    pairs, fn, fp = cmp.match([1.0, 2.0, 3.0], [1.05, 2.9], tol=0.2)
    assert len(pairs) == 2 and fn == [2.0] and fp == []


def test_estimate_offset_recovers_constant_lag() -> None:
    pred = [1.0, 1.5, 2.2, 3.0, 3.4, 4.3, 5.0]; gt = [t + 0.15 for t in pred]
    assert abs(cmp.estimate_offset(gt, pred) - 0.15) < 0.011


def test_estimate_offset_when_lag_exceeds_half_the_spacing() -> None:
    pred = [1.0, 1.45, 2.0, 2.5, 2.9, 3.6, 4.0, 4.55, 5.1]; gt = [t + 0.25 for t in pred]   # jarak ~0,45 s, jeda 0,25 s
    assert abs(cmp.estimate_offset(gt, pred) - 0.25) < 0.011


def test_lag_corrected_match_is_perfect() -> None:
    pred = [1.0, 1.45, 2.0, 2.5, 2.9]; gt = [t + 0.25 for t in pred]
    off = cmp.estimate_offset(gt, pred); pairs, fn, fp = cmp.match([t - off for t in gt], pred, 0.1)
    assert len(pairs) == 5 and not fn and not fp


def test_per_minute_counts() -> None:
    rows = cmp.per_minute([10, 20, 70], [10, 65, 70, 80], 0, 120)
    assert [(r["gt"], r["pred"]) for r in rows] == [(2, 1), (1, 3)]


def test_per_minute_partial_last_minute() -> None:
    rows = cmp.per_minute([10], [10], 0, 90)
    assert len(rows) == 2 and rows[1]["durasi_s"] == 30.0


def test_simultaneous_events_each_counted() -> None:
    pairs, fn, fp = cmp.match([5.0, 5.0], [5.0, 5.0], 0.1)
    assert len(pairs) == 2 and not fn and not fp


def test_lag_adjusted_only_when_playing() -> None:
    assert ann.lag_adjusted(100, 150, 30.0, paused=True) == 100
    assert ann.lag_adjusted(100, 150, 30.0, paused=False) == 100 - round(0.15 * 30)
    assert ann.lag_adjusted(2, 500, 30.0, paused=False) == 0


def test_marked_near_and_minute_stats() -> None:
    assert ann.marked_near([100, 101, 200], 100) == 2
    assert ann.minute_stats([10, 1900, 1910], 1905, 30.0) == (1, 2)


def test_per_minute_total_equals_gt_count_even_after_offset_shift() -> None:
    gt = [10.0, 1199.9]; off = -0.165
    adj = [min(max(g - off, 0.0), 1200.0 - 1e-6) for g in gt]      # 1199.9 + 0.165 > 1200 -> dijepit
    rows = cmp.per_minute(adj, [10.0, 1199.8], 0.0, 1200.0)
    assert sum(r["gt"] for r in rows) == 2
