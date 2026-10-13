# CodeQL hands-on evidence — in progress

This is an attributed GitHub Skills exercise, not an original product or deployed service. Source: [skills/introduction-to-codeql](https://github.com/skills/introduction-to-codeql). GitHub, Inc. MIT license is retained unchanged.

## What this exercise demonstrates

CodeQL follows untrusted Flask query parameters into SQL execution. Parameter binding separates user data from SQL syntax. Static findings must be paired with functional checks: scanner silence alone does not prove that a search works.

## Independently observed results

- Initial CodeQL Setup [run 38443761596](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38443761596): success. This verifies scanner initialization, not remediation.
- Before injection, runtime [run 38461216888](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461216888) at `ee2182fd879ae384a8016ddc680d6a7954007cdc`: 6 tests, 1 passed, 5 SQLite syntax errors. The template uses `%s` placeholders against SQLite; those searches do not work.
- Instructor injection [PR #2](https://github.com/Khemology/skills-introduction-to-codeql/pull/2), head `d73e204537dbf10b58934ef456bbb7486a490fab`.
- Vulnerable runtime [run 38461227418](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461227418), job 115516603121: 6 tests, 2 passed, 1 failed, 3 errored. The injection string returned all synthetic books; an apostrophe-containing name caused SQL syntax error; author searches retained the template placeholder defect.
- Actual PR scanner finding, main alert triage, corrected implementation, and fresh successful runtime/scanner evidence remain pending.

## Execution scope

Tests run on a standard GitHub-hosted Ubuntu runner with Python 3.12.15 and Flask 3.1.2, using Flask's in-process test client and an in-memory SQLite database. No listener is started. No real credentials, private system data, deployment, Codespaces session, model inference, or local Docker access is involved.

The teacher workflows advance on broad event/keyword checks. Teacher completion is not treated as proof of resolved alerts or passing functional tests. The proposed fix will use SQLite `:name` and `:author` bindings with wildcard strings passed as data, as illustrated by the source repository's `fixme` file.

This record is incomplete until the remaining observations are verified.
