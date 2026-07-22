# Git safety rules for TACHYON sessions

**Installed 2026-07-22 following the a01e316 catastrophic deletion incident.**

On 2026-07-21T21:41Z a TACHYON session pushed commit a01e316 to
machinemediation-org that deleted 82 files including the entire
homepage, nav, README, api/kernel-index.json, assets/,
.github/workflows/axn-mirror.yml, all articles/, all top-level
captures/, and dozens of data files. The commit was meant to add
two new files (the CAP-ATTRIBUTION-FLIP-ABOLISH-MONEY capture) but
was executed with `git add -A` from a working tree that was
missing the other 82 files, silently staging their deletion. The
push was a normal fast-forward and neither GitHub nor Vercel raised
any alarm; the site was 404 for approximately 12 hours before an
operator noticed and required full manual reconstruction from the
prior good commit f036df8.

## Rules (binding on all TACHYON sessions)

### RULE 1 — Never use `git add -A` or `git commit -a`

Always stage explicit paths. If a commit should include only a new
capture file, stage only that file:

```
# CORRECT
git add data/captures/2026-07-21-example/manifest.json

# WRONG — will delete anything missing from cwd
git add -A
git commit -a
```

### RULE 2 — Never work outside a fresh clone

Every push operation must be preceded by a fresh `git clone` to a
working directory, or a `git pull` on an existing clone that
started from a fresh clone in the same session. Never construct a
working directory manually with only the new files.

### RULE 3 — Verify before push

Before `git push`, always run:

```
git status
git diff --cached --stat
```

If `git diff --cached --stat` shows any lines beginning with `-` in
the deletion column beyond what was intended, ABORT and investigate.
A commit that adds two files should show two `+` entries and no `-`
entries.

### RULE 4 — Deletion Guardian is a safety net, not a substitute

The `.github/workflows/deletion-guardian.yml` workflow will detect
pushes that delete more than 10 files and create an [URGENT] issue.
It runs on every push. Do not rely on it as a checkpoint — it fires
AFTER the push has already landed. It exists so the operator is
notified within seconds of a bad push, not to prevent bad pushes.

### RULE 5 — Automation is exempt but restricted

The `axn-mirror` bot and other trusted automation are exempt from
the deletion guardian's check (see workflow's PUSHER allowlist).
Any new automation added to this repo MUST use explicit `git add`
paths, never `-A`, and must be reviewed against these rules before
being added to the exempt list.

## Recovery pattern

If a catastrophic deletion is detected, the recovery pattern is:

1. Identify the last known-good commit before the deletion.
2. Compute the set of files present in the good commit but missing
   from current HEAD (the destroyed set).
3. For each destroyed file, restore its contents from the good
   commit using `git show GOOD_SHA:path/to/file`.
4. Retain any additions made after the destruction.
5. Commit as a single restore commit with a clear message
   identifying the destructive commit and the recovery method.
6. Push and verify the live surface.

This pattern was executed successfully in commit 558dc26 to restore
machinemediation-org from the a01e316 destruction.
