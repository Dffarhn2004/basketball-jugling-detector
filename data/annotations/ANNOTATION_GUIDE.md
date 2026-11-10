# Manual annotation guide

## Detection boxes
Class `0` is `basketball`. Draw a tight box around each identifiable ball, including separately identifiable overlapping balls. Do not label reflections or non-balls. Record uncertain/occluded cases for review.

## Bounce events
One event is one physical contact between one ball and the floor. Catching, throwing, or hand redirection is not a bounce. Simultaneous contacts from different balls are separate events. Mark the clearest contact frame, absolute timestamp, contact coordinates, confidence (`certain`, `probable`, `uncertain`), and review status (`approved`, `excluded`, `unresolved`). Review each segment twice and do not use model predictions as the sole labeling reference.
