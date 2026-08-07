# Transcript — case 3 (shared pool), two independent runs

The reproducibility test: the same `input.txt`, two fresh model contexts,
one day apart, run 2 on a slightly later revision of the folder (the checks/
layer had been added between runs; the diagnostic files were unchanged in
substance). If the diagnostician is a method and not a dice roll, both runs
must convict the same primary cause.

- Run 1: 2026-08-03. Run 2: 2026-08-04.
- Conditions per run: fresh context, folder contents only, `input.txt` as
  first message, blind to `expected.md` and to the other run.
- Diagnosis blocks below verbatim. (Run 1's full reply also included opening
  and closing prose, as did run 2's; the complete outputs are preserved in
  the builder's session log — the blocks are what the structural gate reads.)

## Run 1 — diagnosis block

```
DIAGNOSIS: Your email is being junked because the shared sending IP your
donor platform assigned you (149.72.123.24, a SendGrid-infrastructure
address) has developed a bad reputation — it is currently listed on
Spamhaus ZEN (CSS) for emitting low-reputation email. That reputation was
earned by other customers sharing that IP, not by anything St Brigid's
sent. This is the "neighbourhood, not the house" failure: your
authentication and your list are clean; the pipe you share is not.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@stbrigidstrust.ie" and "dmarc=pass (p=QUARANTINE)
   header.from=stbrigidstrust.ie" → Gmail itself confirms your mail is
   fully authenticated and aligned to your own domain. [...]
2. "Received: from o1.em4821.stbrigidstrust.ie ... [149.72.123.24]" +
   the sendgrid.info signature and ct.sendgrid.net unsubscribe link →
   your platform sends through SendGrid's shared infrastructure [...]
3. "LISTED - Spamhaus ZEN (CSS)" for that exact IP → the address that
   handed your newsletter to Gmail is currently flagged for sending
   low-reputation email. [...]
4. Complaint rate 0.02% (healthy is under 0.1%) and hard bounces 0.4%
   (healthy is under 2%) → your own audience behaviour is well inside
   normal. Nothing in your metrics could have earned this.
5. A completely different charity, on the same donor platform, junked
   the same week → the failure follows the shared infrastructure [...]
6. Sudden onset last Tuesday across multiple Gmail accounts → matches a
   pool IP's reputation tipping, not gradual list decay [...]

RULED OUT:
- Authentication/DMARC alignment: dmarc=pass, aligned DKIM — cleared by
  Gmail's own verdict line.
- Self-inflicted list damage (the 800 hand-typed June addresses): a
  poisoned list shows up as rising hard bounces and complaints; yours
  are 0.4% and 0.02%, both healthy — and it could not junk another
  charity's newsletter. Cleared.
- Bulk-sender compliance: one-click unsubscribe headers are present [...]
- Content: not examined — the failure is fully explained upstream [...]

CONTRIBUTING FACTORS: None on your side. (Hand-transcribed paper
sign-ups are a hygiene risk in general — typos become bounces — but
your bounce rate says it hasn't materialised [...])

CONFIDENCE: High — clean tier-A headers, healthy sender metrics, a
listed shared IP, and an unrelated tenant failing simultaneously all
converge on the same cause. What would make it conclusive: Google
Postmaster Tools showing your *domain* reputation as good while the
*IP* reputation reads Low/Bad for the affected period. [...]
```

## Run 2 — diagnosis block

```
DIAGNOSIS: Your update is being junked because of the shared sending IP pool
your donor platform runs on SendGrid infrastructure underneath — the specific
IP that delivered your mail, 149.72.123.24, is currently Spamhaus-listed for
low-reputation traffic, and on a shared pool that reputation belongs to the
neighbourhood of other senders on the same IP, not to your organisation.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@stbrigidstrust.ie" and "dmarc=pass (p=QUARANTINE
   sp=QUARANTINE dis=NONE) header.from=stbrigidstrust.ie" → Gmail's own
   verdict says your authentication is clean and properly aligned [...]
2. "o1.em4821.stbrigidstrust.ie. [149.72.123.24]" in the Received line, plus
   the second signature "dkim=pass header.i=@sendgrid.info" → your platform
   sends through SendGrid's shared infrastructure [...]
3. "LISTED - Spamhaus ZEN (CSS) - 149.72.123.24 was listed" with the stated
   reason [...] → the IP that carried your mail has been observed emitting
   low-reputation email. Your metrics (below) show that email wasn't yours.
4. Complaint rate 0.02% (healthy is under 0.1%) and hard bounces 0.4%
   (healthy is under 2%) → your own audience behaviour is clean. [...]
5. Sudden onset "since last Tuesday", across three separate Gmail accounts,
   and a completely different charity on the same donor platform junked the
   same week → a shared-infrastructure event [...]

RULED OUT:
- Authentication/alignment: dmarc=pass with your own domain's DKIM — clean.
- Your list quality (the 800 paper sign-ups): hand-typed addresses would show
  up as elevated hard bounces and complaints; 0.4% and 0.02% are both well
  inside healthy range. [...] it cannot junk another charity's newsletter
  in the same week.
- Content: not examined; the failure is explained upstream [...]

CONTRIBUTING FACTORS: The 800 manually-typed addresses are a latent
list-quality risk worth watching in your bounce numbers over time, but the
current metrics acquit them of this incident. [...]

CONFIDENCE: Moderate-to-high — I'm stating it as moderate because Gmail
doesn't publish its internal reasoning, so the mechanism (pool reputation)
is inferred from the listing plus the cross-tenant timing rather than stated
by Gmail directly. Two things would make it conclusive: (1) [...] Postmaster
Tools Domain reputation vs IP reputation [...]; (2) the other charity's
headers showing an IP in the same range [...]
```

## Comparison

| Axis | Run 1 | Run 2 | Match |
|---|---|---|---|
| Primary cause | Shared IP pool reputation (149.72.123.24, Spamhaus CSS) | Same | ✅ |
| Decoy verdict (800 hand-typed addresses) | Acquitted, on the same metric evidence | Acquitted, same evidence | ✅ |
| Key evidence cited | dmarc=pass alignment, listed IP, clean metrics, cross-tenant timing | Same four | ✅ |
| Confirming evidence requested | Postmaster domain-vs-IP reputation split | Same, plus the other charity's headers | ✅ |
| Confidence wording | "High" | "Moderate-to-high", with the reasoning for the hedge stated | ⚠️ divergence, logged |

**Verdict:** the conviction is reproducible; the confidence calibration
wobbles by half a grade between runs. Logged in `BLIND-SPOTS.md` as an open
observation rather than smoothed over — run 2's hedge ("the mechanism is
inferred, not stated by Gmail") is arguably the more honest reading.
