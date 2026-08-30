# governace/qa/ — test-artifact home

This directory is the deliverable home for the factory's QA test-authoring
lane (**Bailey**, Sr. AI Testing Engineer, KDD-0019). It holds the artifacts
she produces under governor work orders — **test plans, test scripts, and
pinned stacks** — organized **one folder per project**.

## Layout

```
governace/qa/
  <project-name>/
    README.md            # project overview: component, work order ref, stack pin
    test-plan.md         # the test plan (scope, cases, oracles, acceptance map)
    scripts/             # test scripts (python/pytest; zod for TS-side)
    pinned-stack.md      # pinned framework + version pins, derived from the
                         #   component's cookbook/examples dirs + work order
```

One folder per project — never one shared folder. Each project's folder is
self-contained: a human can open `governace/qa/<project-name>/` and see what
is tested, how, and against what pinned stack.

## Boundary

Bailey's responsibility ends at test plan and script generation. She does not:

- set up test environments (Erwin installs the component);
- execute tests (Gordon sets up env + executes; results land in
  `governace/testing/test-log.md`);
- fix configuration or repair (Erwin);
- accept work or gate any component (the governor, James).

## Test loop

Erwin installs → Bailey authors tests → Gordon sets up env + executes →
results to `governace/testing/test-log.md` → Gordon notifies Bailey + Erwin →
Erwin fixes config → Gordon retests → max 3 iterations → James accepts on the
verification-checklist (`governace/process/governor-verification-checklist.md`).

## Default framework

- Python: **pytest** (knowledge root `/opt/tkv-local/pytest-main`)
- TypeScript-side contracts: **zod** (knowledge root `/opt/tkv-local/zod-main`)
