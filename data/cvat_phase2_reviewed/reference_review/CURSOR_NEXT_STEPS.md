# Next Cursor instructions after external review

Read `REVIEW_FINDINGS.md`, `dataset_review_queue.csv`, `specific_correction_issues.csv`, `baseline_contact_sheet_ai_review.csv`, and `technical_dataset_qc.csv`.

## Important
- **Original data is unchanged.** All external observations are AI-assisted review proposals, not human verified GT.
- **DO NOT start Phase 3** or mark P2 PASS.
- Integrate review queue into a simple annotation checklist without discarding all original labels.
- First correct the 24 known wrong empty labels. Then resolve special duplicate/floor errors and inspect every remaining partial label.
- Do not mark any image approved without actual reviewer confirmation, and do not treat this ZIP as a human sign-off.
- Preserve E1 inference artifacts, configs, and model weights as frozen.
- Track status by reviewed/rejected/pending and preserve visual corrections as a new version of dataset.
- When complete, run data QC, temporal split validation, and independently reviewed pilot bounce annotation.
- Record final correction statistics from actual reviewer actions.

## Minimal next prompt
"Integrate the external review findings as a read-only issue queue. Guide me to review and correct the 111 images in a human annotation tool, starting with 24 zero-label frames and five known candidate errors. Do not automatically approve proposals or overwrite data. Confirm user sign-off before changing P2 to PASS. Do not start training." 
