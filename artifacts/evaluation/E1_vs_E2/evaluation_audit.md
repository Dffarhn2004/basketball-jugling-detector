# Phase 3B Evaluation Audit

The earlier diagnostic used confidence floor 0.001, explaining E2 high recall and low operating precision: AP integrates the ranked precision-recall curve, while fixed-threshold precision counts every retained prediction. Final thresholds were selected only on validation by F1 grid and then frozen for test. E1 class 32 and E2 class 0 were remapped to canonical basketball. Matching is one-to-one greedy by descending confidence at IoU 0.5. Test was not used for threshold selection.
