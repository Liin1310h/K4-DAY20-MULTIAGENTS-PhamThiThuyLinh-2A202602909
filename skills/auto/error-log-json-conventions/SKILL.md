---
name: error-log-json-conventions
description: Use when extracting normalized error records from timestamped text logs.
---
1. Write the output JSON with top-level keys:
   `"schema_version": 2` and `"generated_by": "log-triage"`.
2. Normalize timestamps to UTC as `YYYY-MM-DDTHH:MM:SSZ`.
3. Normalize level values consistently, preserving only the intended error-level records.
4. Normalize service-name values to lowercase and replace `-` with `_`.
5. Attach continuation lines, such as traceback text, to the preceding log record.
6. When repeat markers appear, apply the repeat count to the preceding record.
7. Populate `errors` as an array of normalized error records.
8. Sort `errors` by `service`, then by `timestamp_utc`, both ascending.
9. Recompute any aggregate counts from the normalized `errors` data after repeat handling.
10. Validate the final JSON schema keys and sorting before finishing.
