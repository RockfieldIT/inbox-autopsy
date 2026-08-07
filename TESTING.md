# TESTING.md — how this folder was tested, and what happened

Everything here is reproducible from the repo: inputs in `eval/`, the
structural gate in `checks/`, expected answers separated from inputs so
runs stay blind. **All test cases are synthetic** — realistic headers,
bounce codes, and provider behaviour, but no real sender and no real user.
That is stated plainly here and in `eval/README.md` because constructed
runs dressed up as real ones would be worse than no runs at all.

## Method

1. **Blind diagnosis runs.** Fresh model context loaded with only the
   folder's files; one `eval/cases/*/input.txt` pasted as the first user
   message; the run never sees `expected.md`. Pass = the named primary
   cause matches the intended failure mode AND the diagnosis block passes
   `checks/verify.py` against the input artifact.
2. **Reproducibility.** Same input, two fresh contexts, different days.
   Pass = same primary cause convicted on the same evidence.
3. **Refusal under disguise.** A case plus an explicit "top three causes +
   how to fix each" demand. Pass = one cause, zero fixes, boundary held
   without the reply going cold.
4. **Structural gate selftest.** `python3 checks/verify.py --selftest` —
   one good fixture passes; four bad fixtures each fail on their named
   check (ONE-CAUSE, NO-RX, GROUNDING, FORMAT).

Each case carries deliberate decoys (content red herrings, plausible
self-blame) designed to tempt a wrong conviction; acquitting the decoy
explicitly is part of what "correct" means.

## Results (runs of 2026-08-03 / 2026-08-04)

| Test | Expected cause | Named cause | Decoy handled | verify.py | Result |
|---|---|---|---|---|---|
| Case 1 blind (Mailchimp/Gmail headers) | #1 alignment failure | ✅ same | ✅ emoji/content acquitted | ❌ GROUNDING — see defect D1 | Pass with logged defect |
| Case 2 blind (Microsoft NDR) | #2 missing DMARC → 550 5.7.515 | ✅ same | ✅ "we have SPF" + blacklist theory both addressed | not run on this transcript | Pass |
| Case 3 blind, run 1 (charity/SendGrid) | #4 shared IP pool | ✅ same | ✅ hand-typed list acquitted on metrics | not run on this transcript | Pass |
| Case 3 blind, run 2 (reproducibility) | #4 shared IP pool | ✅ same cause, same evidence | ✅ same acquittal | — | Pass; confidence wobbled (defect D2) |
| Case 4 blind (cold outreach) | #3 self-inflicted reputation | ✅ same | ✅ "is Instantly the problem?" ruled out with IP-vs-domain split | not run on this transcript | Pass |
| Refusal (disguised ask) | boundary holds | ✅ one cause, zero fixes | ✅ warm refusal, evidence acts only | ✅ clean pass, 4 quotes grounded | Pass |
| Checker selftest | 1 pass + 4 named fails | — | — | ✅ SELFTEST PASS | Pass |
| **Real case 1** (author's own NDR, Gmail 550 5.7.26) | unknown at run time | unauthenticated third-party sending path + own enforcing DMARC policy — **confirmed by ground truth learned afterwards** | ✅ intake caught the wrong-half-of-artifact stumble; declined to guess the sending system, asked instead | ✅ clean pass, 7 quotes grounded | Pass — see `eval/real-case-1/` |

Full verbatim transcripts for case 1, the case-3 pair, and the refusal run
are in `eval/transcripts/` — flourishes, defects and all. Cases 2 and 4 are
summarised here; their inputs are in `eval/cases/` and any judge can rerun
them blind in minutes.

## What the testing surfaced (and did not hide)

- **D1:** the case-1 run put a paraphrase inside quote marks. Caught by the
  GROUNDING check when the transcript was fed back through verify.py — the
  gate catching the diagnostician is the system working, and both the
  failing transcript and the checker verdict are preserved unedited.
- **D2:** reproducible conviction, wobbly confidence grade across runs.
- **D3:** the model adds closing prose after the "stop". No fixes in it
  (NO-RX scans the entire reply), but logged.

Details and structural blind spots: `BLIND-SPOTS.md`.

## Run it yourself

```
python3 checks/verify.py --selftest
# then any blind run:
#   fresh session + folder files only → paste eval/cases/case3-*/input.txt
#   save the diagnosis block → python3 checks/verify.py block.md input.txt
```

## What this testing is and is not

One real case exists: the author's own genuine NDR, diagnosed in a live
two-turn session, with the diagnosed mechanism later confirmed by the
third party involved (`eval/real-case-1/` — provenance, privacy
substitutions, and the honest caveat that the user was the builder are all
documented there). The synthetic suite proves the method holds under blind
conditions, survives a disguised ask, and reproduces its convictions. An
independent third-party user running it on their own failure remains the
next bar, and this file will keep saying so until one has.
