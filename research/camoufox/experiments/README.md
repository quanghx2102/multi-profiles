# Experiment Layout

Each authorized experiment receives `EXP-AUD-NNN-NNN/` with a pre-registration, environment record, command/config manifest, evidence manifest, redacted results, confounders, and cleanup record. Do not create a run directory until exact upstream and environment inputs are selected.

Experiments must define stop conditions for secret exposure, uncontrolled external traffic, process escape/orphaning, destructive profile effects, or invalid provenance. Failed and inconclusive runs are retained in the results index rather than overwritten.

