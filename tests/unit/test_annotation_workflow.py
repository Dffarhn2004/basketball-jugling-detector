from pathlib import Path
from bounce_counter.data_qc import validate_event_csv, validate_yolo_label


def test_multiple_events_same_frame_are_allowed(tmp_path: Path) -> None:
    event = tmp_path / 'events.csv'
    event.write_text('event_id,frame_idx,time_s,confidence,review_status\nA,10,1.0,certain,approved\nB,10,1.0,certain,approved\n')
    assert validate_event_csv(event, 10, 100) == []


def test_empty_yolo_label_is_valid_no_object_file(tmp_path: Path) -> None:
    label = tmp_path / 'empty.txt'; label.write_text('')
    assert validate_yolo_label(label) == []
