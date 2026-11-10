# E1 vs E2 test evaluation

Metrics are computed on the identical 18-image test split with E1 COCO class 32 remapped to canonical basketball and E2 class 0. Matching IoU=0.5, prediction confidence floor=0.001, imgsz=640, CPU. AP is the 101-point interpolated AP over confidence-ranked detections. No threshold tuning was performed on test.

Note: three reviewed frames contain four boxes; counts alone do not prove errors, and no annotations were deleted automatically.
