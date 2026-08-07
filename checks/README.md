# checks/ — enforcement in code, not prose

rules.md tells the diagnostician what a diagnosis must be. This folder makes
those musts structural. `verify.py` runs offline — no API key, no network,
Python 3 stdlib only — and validates any diagnosis against the artifact it
claims to be reading.

## Run it

```
python3 checks/verify.py <diagnosis.md> <artifact.txt>   # check one diagnosis
python3 checks/verify.py --selftest                      # prove the checker works
```

## What it enforces

| Check | Meaning |
|---|---|
| FORMAT | All five sections present, exactly once, in order. |
| ONE-CAUSE | The DIAGNOSIS section names a single primary cause — no lists, no "several causes", max four sentences. A symptom inventory cannot pass. |
| GROUNDING | Every double-quoted span in the EVIDENCE CHAIN must appear verbatim in the supplied artifact (whitespace-normalized; `...` splits a quote into parts that must each match). A fabricated quote cannot pass. |
| NO-RX | No prescription language anywhere — the scan runs outside quoted material, so a user saying "we set up SPF" is fine, but "set up a custom domain" in the diagnostician's own voice fails. Evidence acts (check / look up / screenshot / verify) are permitted; treatment is not. |
| CONFIDENCE | A stated level: high, moderate, or provisional. |

The output format itself has no field a fix could live in; NO-RX exists for
the case where one tries to squat in a field meant for something else.

## Negative fixtures

`fixtures/` contains one known-good diagnosis and four known-bad ones. Each
bad fixture fails on exactly the named check — run `--selftest` to see all
five verdicts. If you modify verify.py, the selftest is the contract: a
change that lets any bad fixture pass is a regression.

| Fixture | Fails on | Why |
|---|---|---|
| `good-output.md` | — | clean pass |
| `bad-three-causes.md` | ONE-CAUSE | a ranked-nothing list of three causes |
| `bad-prescription.md` | NO-RX | a fix hiding in CONTRIBUTING FACTORS |
| `bad-fabricated-quote.md` | GROUNDING | cites a blocklist line that isn't in the artifact |
| `bad-missing-sections.md` | FORMAT | no RULED OUT, no CONTRIBUTING FACTORS |
