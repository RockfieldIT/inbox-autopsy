# eval/ — the test suite, honestly labelled

**One case here is real.** `real-case-1/` is a genuine NDR received by the
author, diagnosed in a live two-turn session and later confirmed correct by
ground truth — its README covers provenance, privacy substitutions, and
caveats. **Every case under `cases/` is synthetic.** The headers, bounce messages,
IPs, businesses, and people are constructed to be realistic (real ESP
infrastructure patterns, real SMTP codes, real provider ranges) — but no
real sender's mail is in here, and no real user has been harmed, helped, or
consulted in these runs. They are the builder's eval harness, not receipts
of real-world use, and nothing in this repo pretends otherwise. (If a real,
consented, anonymised case is added later it will live in its own clearly
marked folder with its method file committed before the run.)

## Structure

- `cases/caseN-<failure-mode>/input.txt` — the user message, verbatim, as it
  would be pasted into a fresh session. Each is built around one of the four
  most common failure modes in `reference/failure-modes.md`, with deliberate
  decoys (a content red herring, a plausible-but-wrong self-blame) designed
  to tempt a weak diagnostician into the wrong conviction.
- `cases/caseN-<failure-mode>/expected.md` — the intended primary cause and
  the traps, kept in a separate file so a test run can be genuinely blind.
- `refusal/disguised-ask-input.txt` — case 1 plus an explicit "give me the
  top three causes and how to fix each" — the disguised ask rules.md §7 must
  survive.
- `transcripts/` — verbatim outputs from the blind runs already performed,
  with run conditions in each file's header. Kept as-is, flourishes and all.

## How to run a blind test

1. Fresh Claude session (project or CLI) with ONLY the folder's md files
   loaded — no expected.md files, no transcripts.
2. Paste one `input.txt` as the first user message.
3. Compare the named primary cause against `expected.md`.
4. Save the diagnosis block to a file and run the structural gate:
   `python3 checks/verify.py <diagnosis.md> cases/caseN-*/input.txt`

Pass = correct primary cause + verify.py clean. A run that names the right
cause but fails verify.py (e.g. prescription language crept in) is a fail.

## Results to date

See `TESTING.md` at the repo root for the full results table, the
repeat-run reproducibility comparison, and defects observed during testing.
