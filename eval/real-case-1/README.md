# real-case-1 — a real bounce, diagnosed live, ground truth confirmed

**This case is real.** On 1 July 2026 the author (Colm Whelan, rockfieldit.com)
received a genuine "Undelivered Mail Returned to Sender" NDR carrying a Gmail
`550 5.7.26` rejection. On 4 August 2026 he ran it through this diagnostician
in a live two-turn session — arriving, like a real user, with the wrong half
of the artifact first. The full exchange is in `transcript.md`; the final
diagnosis block is in `diagnosis.md`; the artifact as supplied is in
`artifact.txt`.

## What happened in the session

1. The user pasted the NDR's *outer headers* — the envelope of the bounce,
   not its verdict. Intake recognised the miss, explained envelope-vs-verdict
   in plain language, and walked him to the visible body.
2. With the body supplied, the diagnostician convicted one cause: the mail
   was sent *as* rockfieldit.com by a third-party VoIP provider's server on
   an unauthenticated path (no aligned SPF or DKIM), and rockfieldit.com's
   own enforcing DMARC policy instructed Google to reject it. It explicitly
   noted the DMARC policy was not the pathology — it was doing its job — and,
   rather than guessing which system sent the mail, asked.

## Ground truth (learned after the diagnosis)

The provider later confirmed what no artifact could show: a contractor
testing their systems had entered email addresses into the wrong fields,
causing their platform to send test mail as the author's address — accidental
spoofing, in effect. The diagnosed mechanism was exactly right, and the
diagnostician's refusal to guess below the artifact's reach (the operational
cause) was the correct boundary. `checks/verify.py` passes the diagnosis
against the artifact: format, one cause, all 7 quotes grounded, no
prescription language, confidence stated.

## Provenance and privacy

- The diagnosis session ran on 2026-08-04, during development, before this
  repository's first public commit; the repo's commit history shows the
  method files committed before this case folder was added.
- The transcript and artifact are verbatim **except** three substitutions
  applied consistently across every file in this folder, to protect third
  parties: the recipient's address → `recipient@masked-recipient.example`,
  the provider's mail hostname → `mail.voip-provider.example`, and the
  provider's IP → `203.0.113.41` (a documentation-range address). No other
  edits. Originals are retained privately by the author. rockfieldit.com is
  the author's own domain and is left real precisely so this case is
  verifiable as real.
- The caveat, stated plainly: the user in this session was the builder. The
  artifact, the failure, and the confirmed outcome are real; an independent
  third-party user run remains the next bar.
