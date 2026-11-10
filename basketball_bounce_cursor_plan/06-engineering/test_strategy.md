# Unit / Integration / End-to-End Testing Plan

## Unit test murni
- `test_timebase`: constant FPS dan timestamps VFR mock.
- `test_box_geometry`: bbox bottom point, source-resolution conversion.
- `test_floor_line`: left/middle/right perspective.
- `test_velocity`: falling >0, rising <0, noise smoothing.
- `test_state_machine`: turun→kontak→naik = exactly one event.
- `test_hand_catch`: reversal tanpa floor contact = zero.
- `test_dedup`: same contact across frames/ID switch = one.
- `test_simultaneous`: 2 locations same timestamp = two.
- `test_multi_bounce`: same ball hits again after cooldown = two.
- `test_matcher`: one-to-one matches; don't double-match GT.
- `test_metrics`: APE 0 with FP/FN 10 example.
- `test_split`: overlaps rejected and exclusion buffers obeyed.

## Integration tests
- 20-frame synthetic input video -> pipeline outputs fields properly.
- Mock detections/tracks -> event CSV -> render overlay -> count consistency.
- One 5–10 second actual sample (if video available) -> no crash, 3-ball data if visible.

## Regression suite
Every discovered failure gets one small synthetic test or saved noncopyrighted feature fixture. Tests should not depend on full downloaded video when possible.

## GPU tests
Mark GPU-dependent tests `@pytest.mark.gpu`, skip gracefully on CPU. No real model download in default unit tests.

## Failure behavior
- Missing file / corrupt video / bad config should exit nonzero.
- Missing `best.pt` may not silently fallback pretrained without recording a warning and changing run label.
- Renderer output mismatch with CSV should cause failed QA.
