"""Pure validation helpers for Phase 2 manifests and annotations."""
from __future__ import annotations
from pathlib import Path
import csv


def validate_yolo_label(path: Path) -> list[str]:
    errors: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split()
        if len(fields) != 5:
            errors.append(f"{path}:{line_no}: expected 5 fields")
            continue
        try:
            cls, *values = map(float, fields)
        except ValueError:
            errors.append(f"{path}:{line_no}: non-numeric value")
            continue
        if cls != 0 or any(value < 0 or value > 1 for value in values) or values[2] <= 0 or values[3] <= 0:
            errors.append(f"{path}:{line_no}: invalid class or normalized box")
    return errors


def validate_event_csv(path: Path, duration_s: float, frame_count: int) -> list[str]:
    errors: list[str] = []
    required = {"event_id", "frame_idx", "time_s", "confidence", "review_status"}
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not required.issubset(rows[0].keys() if rows else set()):
        return ["event CSV missing required columns"]
    allowed_statuses = {"approved", "excluded", "unresolved", "unreviewed"}
    allowed_confidences = {"certain", "probable", "uncertain"}
    for row in rows:
        if row["review_status"] not in allowed_statuses:
            errors.append(f"invalid review_status: {row['event_id']}")
        if row["confidence"] not in allowed_confidences:
            errors.append(f"invalid confidence: {row['event_id']}")
    ids: set[str] = set()
    for row in rows:
        if row["event_id"] in ids:
            errors.append(f"duplicate event_id: {row['event_id']}")
        ids.add(row["event_id"])
        try:
            frame = int(row["frame_idx"]); time_s = float(row["time_s"])
            if not 0 <= frame < frame_count or not 0 <= time_s <= duration_s:
                errors.append(f"out-of-range event: {row['event_id']}")
        except ValueError:
            errors.append(f"invalid timestamp: {row['event_id']}")
    return errors
