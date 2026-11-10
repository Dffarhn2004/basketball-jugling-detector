from pathlib import Path
from bounce_counter.data_qc import validate_event_csv, validate_yolo_label


def test_yolo_validation(tmp_path: Path) -> None:
    label = tmp_path / "x.txt"
    label.write_text("0 0.5 0.5 0.2 0.2\n")
    assert validate_yolo_label(label) == []


def test_event_duplicate_and_range(tmp_path: Path) -> None:
    event = tmp_path / "events.csv"
    event.write_text("event_id,frame_idx,time_s,confidence,review_status\nA,1,1.0,certain,approved\nA,99,99,bad,approved\n")
    errors = validate_event_csv(event, 10, 100)
    assert any("duplicate" in error for error in errors)
    assert any("out-of-range" in error for error in errors)
