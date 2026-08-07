# Blind spots & open defects

What this diagnostician structurally cannot see, and the defects found in
testing that were logged rather than papered over. A diagnostician that
won't diagnose itself isn't worth trusting.

## Structural blind spots (cannot be fixed by better prompting)

**It trusts the artifact.** Headers can be truncated in copying, forged, or
taken from an unrepresentative message. Intake checks for the obvious
stumbles (missing `Authentication-Results`), but a cleanly forged or
wrong-campaign artifact produces a confident wrong diagnosis. Garbage in,
conviction out.

**Receiver reasoning is inferred, never observed.** Gmail publishes no
per-message spam score. Every Gmail diagnosis that isn't stated in the
verdict line (i.e., anything beyond authentication) is an inference from
converging signals — which is why reputation-layer convictions carry
"what would confirm this" clauses and should never reach the certainty of
an authentication-layer one.

**Per-recipient placement is unexplainable.** One person's personal filters,
prior interactions, or corporate gateway can junk mail for reasons no
artifact in the sender's possession will ever show. That's why one anecdote
is tier-E evidence and the taxonomy has a "not-a-failure" category.

**It cannot look anything up.** No live DNS, no blocklist queries, no
Postmaster access. Every external fact must arrive through the user's hands
(guided in `reference/evidence-collection.md`), which means a diagnosis is
only as current as the artifacts supplied.

**Reference files age.** Provider rules and ESP defaults drift; the
reference layer is dated and flagged accordingly, and the live headers
always outrank it. A diagnosis leaning on an outdated rulebook detail is a
real failure mode of this folder itself.

## Open defects observed in testing (see TESTING.md for full runs)

**D1 — Paraphrase in quote marks.** In the case-1 blind run, the
diagnostician rendered the user's "We haven't changed anything on our end"
as "nothing changed on our end" inside quotation marks in its evidence
chain. The conclusion was unaffected, but a quote that isn't a quote is an
integrity defect in an evidence-driven tool. `checks/verify.py` (GROUNDING)
catches exactly this — the failing transcript is preserved verbatim in
`eval/transcripts/`, unpatched, alongside the checker output that flags it.

**D2 — Confidence calibration wobbles between runs.** The case-3
reproducibility pair convicted the same cause on the same evidence twice,
but graded it "High" in one run and "Moderate-to-high" in the other. The
second run's hedge came with better epistemics (pool-reputation mechanism
is inferred, not stated by Gmail). The primary-cause conviction is
reproducible; the confidence grade is not yet. No structural gate enforces
calibration — verify.py can check that a level is stated, not that it's
right.

**D3 — The coda drifts past "stop".** Blind runs consistently appended
warm closing prose after the diagnosis block. None of it contained fixes
(verify.py's NO-RX scan covers the whole reply), but rules.md says "stop"
and the model demonstrably prefers to land the plane gently. Judged
harmless and human; logged because the rule and the behaviour disagree,
and honesty means recording which one won.
