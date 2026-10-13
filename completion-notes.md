# CodeQL hands-on evidence

Completed the attributed [GitHub Skills Introduction to CodeQL](https://github.com/skills/introduction-to-codeql) exercise and independently checked the security and functional results. GitHub, Inc. MIT license is retained unchanged. This is course-derived practice, not an original product or deployed service.

## Learning applied

CodeQL traces untrusted Flask query parameters into SQL execution. Parameter binding separates data from SQL syntax. Static analysis and functional tests answer different questions: a successful analysis job can report a vulnerability, and a scanner-suggested fix can be syntactically safe yet incompatible with the database.

The instructor and generated suggestion use `%s` placeholders against SQLite. Actual execution showed those searches fail. The final implementation uses SQLite `:name` and `:author` placeholders with wildcard strings supplied through named parameter dictionaries, consistent with the source repository's `fixme` example.

## Evidence sequence

1. Initial CodeQL Setup [run 38443761596](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38443761596) succeeded.
2. Before introducing injection, runtime [run 38461216888](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461216888), commit `ee2182fd879ae384a8016ddc680d6a7954007cdc`: 6 tests, 1 passed, 5 errors from incompatible SQLite placeholders.
3. Instructor injection [PR #2](https://github.com/Khemology/skills-introduction-to-codeql/pull/2), head `d73e204537dbf10b58934ef456bbb7486a490fab`: CodeQL check 115516849436 failed with **1 new high severity security vulnerability**. The coordinator independently inspected GitHub UI: rule `py/sql-injection`, SQL query built from user-controlled sources, `server/routes.py` line 16, [alert 1](https://github.com/Khemology/skills-introduction-to-codeql/security/code-scanning/1).
4. Vulnerable runtime [run 38461227418](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461227418), job 115516603121: 6 tests, 2 passed, 1 failed, 3 errors. An injection string returned all synthetic records; an apostrophe caused SQL syntax error; author searches retained the placeholder defect.
5. The intentionally vulnerable **unserved training** PR was merged as `c2ebe6ba29522712f2f2ac361ee63853fd05eef6` to perform the instructor's alert-lifecycle exercise. Main analysis [run 38461578654](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461578654) processed the alert.
6. The coordinator inspected alert 1 on main, dismissed it as **Used in tests** with the isolated-playground explanation, freshly verified **Dismissed**, reopened it, and freshly verified **Open**. The activity trail records both actions. Dismissal was an educational lifecycle operation, not remediation.
7. Fixed both search paths in commit `9cd9f249fad836842fd621fa7596032815a6fdea`.
8. Fresh runtime [run 38461938419](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461938419), job 115519058471: **all 6 tests passed** in 0.090 seconds. Default listing, normal name and author searches, apostrophes, and injection strings in both parameters were exercised.
9. Fresh CodeQL [run 38461938733](https://github.com/Khemology/skills-introduction-to-codeql/actions/runs/38461938733): Python job 115519063951 and Actions job 115519064387 succeeded; Python SARIF upload was processed. The coordinator then independently verified alert 1 is actually **Fixed on main**, with the activity trail naming commit `9cd9f249fad836842fd621fa7596032815a6fdea`. The earlier dismissal and reopening remain visible in its audit trail.
10. Teacher [issue #1](https://github.com/Khemology/skills-introduction-to-codeql/issues/1) closed; finish comment 6154429658 was read back. Teacher completion was checked separately from the evidence above.

## Reproduce the runtime checks

```sh
python -m pip install Flask==3.1.2
python -m unittest discover -s tests -v
```

Tests use Flask's in-process test client and an in-memory SQLite database with synthetic records. The verified runner was standard GitHub-hosted Ubuntu, Python 3.12.15, Flask 3.1.2. No listener was started. The runtime workflow uses read-only repository permissions and pinned checkout/setup-python action commits.

## Scope and limits

No deployed application, Codespaces session, real user data, new secret, paid model inference, private runtime access, or local Docker execution is claimed. This closes the demonstrated SQL injection and associated search regression; it is not a complete security assessment of the legacy teaching application or its dependency lock file. Intentional vulnerable history remains as the educational failure evidence.

Teacher checks advance on broad workflow events and keyword matching. They are not acceptance tests for actual alert state or runtime behavior. Future applied AI tool/API handlers should pair their source-to-sink security analysis with synthetic regression checks and explicit findings triage; this lesson does not claim such integration into the private system.
