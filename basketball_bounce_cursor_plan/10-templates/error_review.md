# Bounce Error Review — TEMPLATE

| Field | Value |
|---|---|
| record_id | TBD |
| class | FP / FN / timing_mismatch |
| video_time_sec | TBD |
| frame_index | TBD |
| ground_truth_event_id | TBD |
| predicted_event_id | TBD |
| related_track_id | TBD |
| clip_path | TBD |
| detector_status | visible/missed/occluded/other |
| tracking_status | stable/fragmented/id_switch/other |
| floor_contact_status | confirmed/no/uncertain |
| primary_root_cause | TBD |
| secondary_causes | TBD |
| fix_hypothesis | TBD |
| fix_tested | yes/no |
| reviewer | TBD |
| verified_at | TBD |

## Required reviewer notes
- Jelaskan kontak fisik yang terlihat/tidak terlihat.
- Periksa frame sebelum dan sesudah untuk disambiguation.
- Tandai tidak pasti bila video tidak cukup informatif; jangan paksakan jawaban.
- Pastikan event tidak duplikat dengan error di waktu yang sama.
