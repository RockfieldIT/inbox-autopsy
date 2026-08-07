# Inbox Autopsy 📧🔬

**A diagnostician for small-business email that didn't reach the inbox.**

Built from MSP casework — the calls that start "our invoices are bouncing," "customers say our newsletter is in their junk," "nobody's replying since last Tuesday." Whatever the stack — a Microsoft 365 tenant, Mailchimp, Kit, Beehiiv, Brevo, a cold-outreach tool — Inbox Autopsy works backward from the failure and tells you **the one reason why**, with the evidence trail that proves it.

It does not fix anything, rewrite anything, or hand you a checklist. It names the cause, shows how it got there, and stops. Like a pathologist, not a surgeon.

## Who it's for

The person at a small business who owns email — usually alongside twelve other jobs: the owner, the office manager, the marketing team of one. Also useful to newsletter creators and agencies hitting the same wall. No deliverability expertise required — the whole point is that the expertise lives in this folder.

## Setup

1. Create a new Claude project (claude.ai → Projects) — or a Claude Code / Cowork session.
2. Add every file in this folder to the project, keeping the `reference/` files too.
3. Optionally set the project instructions to: *"You are the diagnostician defined in identity.md. Follow rules.md exactly."*

That's it. Claude becomes the diagnostician.

## How to use it

**Just describe what went wrong, in plain English.** You don't need to know what headers, DMARC, or SPF are — the diagnostician's first job is to interview you and walk you, click by click, to the evidence it needs. A perfectly good opening message:

> People keep telling me our newsletter is going to their spam folder. It's sent through Mailchimp. Help?

It will ask a couple of questions (what you send, what happened, when it started), then guide you one step at a time — usually: send a test to your own Gmail, open it, click the three dots, click "Show original", copy, paste. It checks what you pasted, tells you what it sees, and keeps going until it has enough to name the cause.

If you *do* already have evidence, lead with it — you'll skip the interview. The strongest evidence, in order:

1. **Raw headers** of an affected (or seed-test) message
2. **A bounce message**, pasted whole — including the error code
3. **DMARC aggregate report** or **Google Postmaster Tools** screenshots
4. Your platform's campaign stats (opens, bounces, complaints) — weakest, but usable

## What you get back

A structured diagnosis:

```
DIAGNOSIS: one sentence — the primary cause
EVIDENCE CHAIN: what in your artifact points there, step by step
RULED OUT: what was checked and cleared
CONTRIBUTING FACTORS: subordinate findings, kept subordinate
CONFIDENCE: high / moderate / provisional — and what would confirm or overturn it
```

If your evidence is too weak to convict anything, it says so and names the exact artifact that would settle it — rather than guessing.

## What it will not do

Rewrite your subject lines. Produce a 12-point deliverability audit. Tell you which DNS records to add. Those are editor, auditor, and consultant jobs. This is a diagnostician: **why it broke**, full stop.

## Folder map

| File | Job |
|---|---|
| `identity.md` | Who the diagnostician is, what it does and refuses to do |
| `intake.md` | The bedside manner: how it interviews a non-technical user and leads them to evidence, one step at a time |
| `rules.md` | The diagnostic method: evidence grading, causal layers, cause-vs-symptom tests, output format |
| `examples.md` | Three worked diagnoses showing the reasoning standard — including one where the correct finding is "nothing is broken" |
| `reference/evidence-collection.md` | Exact click-paths for gathering evidence in Gmail, Outlook, Apple Mail, and the major ESPs |
| `reference/failure-modes.md` | Failure taxonomy ranked by real-world frequency, plus benchmarks |
| `reference/header-forensics.md` | How to read Authentication-Results, DKIM `d=`, ARC, Received chains, and bounce codes |
| `reference/esp-quirks.md` | Per-platform authentication defaults — the most common root cause lives here |
| `reference/bulk-sender-rules.md` | The Gmail / Yahoo / Microsoft bulk-sender rulebooks that turned old configs into new failures |
| `checks/verify.py` | Offline structural gate: one primary cause, quotes grounded in the artifact, no prescription language. `--selftest` runs it against known-good and known-bad fixtures |
| `eval/` | The test suite — one **real case** (a genuine NDR, diagnosed live, ground truth confirmed) plus four synthetic cases with decoys, a disguised-ask refusal test, and verbatim transcripts |
| `TESTING.md` | Method and results: blind runs, a reproducibility pair, refusal under disguise, and what the testing caught |
| `BLIND-SPOTS.md` | What this tool structurally cannot see, plus the open defects testing surfaced — logged, not patched over |

## Kick the tyres

Two minutes, no API key: `python3 checks/verify.py --selftest` proves the
structural gate works, and any file in `eval/cases/` can be run blind in a
fresh session (paste `input.txt`, compare against `expected.md`, feed the
diagnosis block back through verify.py). The eval suite is synthetic and
says so — see `TESTING.md` for results, including the defects it caught.

## A note on freshness

Mailbox-provider rules and ESP defaults drift. The reference files flag where to verify against live sources; the headers you paste always outrank anything written here.
