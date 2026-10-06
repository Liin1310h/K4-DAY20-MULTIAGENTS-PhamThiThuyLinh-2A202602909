---
name: log-triage-json-conventions
description: Use when parsing application logs into an errors JSON triage report.
---
1. Normalize every output service name to lowercase and replace hyphens with underscores.
2. Normalize error timestamps to UTC as `YYYY-MM-DDTHH:MM:SSZ`.
3. Include the required top-level fields `"schema_version": 2` and `"generated_by": "log-triage"`.
4. Parse log levels case-insensitively, but write normalized levels consistently if the schema includes them.
5. Attach traceback or continuation lines to the preceding log entry; if extracting an exception, use the final exception line.
6. Apply `-- last message repeated N times --` markers to the preceding entry’s repeat count or aggregates.
7. Include only the requested error-severity entries, typically ERROR and CRITICAL, not informational messages merely containing the word “ERROR”.
8. Sort the `errors` array by normalized service name, then by `timestamp_utc`, ascending.
9. Compute service aggregates using the normalized service names and repeat counts.
10. Before finishing, reopen the JSON and verify the header fields, service normalization, sort order, timestamps, and aggregate consistency.
