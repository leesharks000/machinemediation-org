# Cohort baseline for the pre-removal download figures

**Measured 2026-07-04, unauthenticated Zenodo REST API.** Raw sample: `zenodo-baseline-sample.json` (checkable; re-runnable from the query below).

**Question.** Is 666 downloads in ~2 days (captured, this set) / 1,000+ in ~4 days (asserted contemporaneously in zenodo/zenodo#2606, day of removal) "a lot by Zenodo's standards"?

**Method.** Cohort = all Zenodo records of type `dataset` with `publication_date:[2026-06-14 TO 2026-06-16]` — the same publication window as the registry's v7.2 (June 15). Cohort population: **1,791**. Sample: first 200 by `mostrecent` within the window (API page cap 25 unauthenticated; 8 pages). Stats read 2026-07-04, i.e. after **~19 days** of accumulation for the cohort, versus **~2 days** for the registry's captured figure — the comparison is therefore conservative by roughly a factor of ten in accumulation time, in the cohort's favor.

**Findings (n=200).**

| statistic | this-version downloads | all-versions downloads |
|---|---|---|
| median | 7 | 6 |
| mean | 43.0 | 21.1 |
| p90 | 53 | 43 |
| p95 | 116 | 77 |
| p99 | 804 | 397 |
| max | 3,087 | 561 |
| ≥ 666 after ~19 days | 2/200 (1.0%) | 0/200 (0.0%) |

**Reading.** After ~19 days, 99% of the registry's own publication cohort had not reached the download count the registry reached in ~2. The captured 666-at-day-2 sits at approximately the 99th percentile of the cohort's 19-day counts; the 1,000+-at-day-4 figure asserted at removal sits above it. The registry's day-2 count was ~95× the cohort's 19-day median.

**Limitations, on the record.** (1) The sample is the window's 200 most recent, not a random draw; the window is only three days wide, limiting ordering bias, but this is a convenience sample. (2) The Zenodo UI counter captured at 666 is not field-labeled in the interface; API naming (`downloads` = this-version, `version_downloads` = all-versions) means the captured figure maps to one of the two columns above — it clears the 99th percentile threshold in either mapping at the version level and exceeds the observed maximum at the all-versions level. (3) Bot and crawler traffic is unmodeled on both sides of the comparison. (4) Cohort stats were measured post-hoc on 2026-07-04 and will drift; the raw sample is preserved for exactly that reason.

**Conclusion, bounded.** By the platform's own contemporaneous cohort, the removed dataset's usage was in the top ~1% of same-week datasets on a fraction of the accumulation time. "A lot by Zenodo's standards" is hereby a measurement, not an impression.
