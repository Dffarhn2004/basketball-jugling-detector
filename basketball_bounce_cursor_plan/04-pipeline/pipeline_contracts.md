# Pipeline Data Contract & Boundary Cases

## Functional interfaces yang diharapkan
```python
read_frames(video_path) -> Iterable[FrameRecord]
detect_balls(model, FrameRecord) -> list[Detection]
track_detections(tracker, detections, FrameRecord) -> list[TrackObs]
build_trajectory_features(history) -> TrajectoryFeatures
update_bounce_state(track_state, features, floor_cfg) -> list[EventCandidate]
deduplicate_events(candidates) -> list[BounceEvent]
render_video(frames, tracks, events, output_path) -> RenderSummary
```

## Dataclasses (panduan, Cursor boleh implementasi typed objects)
- `FrameRecord(frame_idx:int, time_s:float, image:np.ndarray)`
- `Detection(bbox_xyxy:tuple, conf:float, class_name:str)`
- `TrackObs(track_id:int, time_s:float, bbox_xyxy:tuple, conf:float)`
- `BounceEvent(event_id:str, time_s:float, position_xy:tuple, track_id:int|None, reason:str)`

## Side effects
- Detektor wrapper boleh load weights.
- Domain functions `motion`, `fsm`, `dedup`, `matching`, `metrics` harus bisa diuji tanpa video/GPU.
- Renderer hanya membaca events; **tidak** mengubah count.

## Missing value rules
- Frame corrupt -> error/report; jangan silently skip lalu gunakan FPS salah.
- Missing box -> `None`, bukan bbox palsu.
- Missing track ID -> reason + optional event, bukan ID = 0 jika itu juga valid.
- Event candidate yang uncertainty tinggi -> rejected/needs_review, tidak termasuk count final sampai aturan jelas.

## Boundary
- Video start dapat memuat bola sudah di tengah gerakan: jangan menghitung bounce sebelum frame pertama.
- Video end: candidate belum dikonfirmasi rising -> jangan mengada-ada bounce.
- Dua event frame sama -> dua event ID sah.
- Contact spanning segment split boundary -> gunakan margins untuk processing, tetapi evaluasi hanya event di interval inti, supaya tidak double-count.
