# Examples — three worked diagnoses

These show the reasoning standard. Note what each one does: names one cause, quotes the artifact, ranks everything else below it, and stops.

---

## Example 1 — Newsletter open rates fell off a cliff

**Presenting symptom:** "Our Mailchimp newsletter open rate dropped from 38% to 11% over three sends. Nothing changed on our end."

**Evidence supplied (Tier A):** Raw headers from a test send to a Gmail address:

```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of bounce.mcsv.net designates 205.201.x.x as permitted sender)
       dkim=pass header.d=mcsv.net header.s=k1;
       dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=example-shop.ie
```

**Diagnosis:**

```
DIAGNOSIS: The newsletter fails DMARC alignment because the domain was never
authenticated in Mailchimp — DKIM is signed with Mailchimp's domain, not the
sender's — and Gmail's bulk-sender requirements turn that from a cosmetic flaw
into a filtering offence.

EVIDENCE CHAIN:
1. "dkim=pass header.d=mcsv.net" → DKIM passes, but for mcsv.net (Mailchimp's
   domain), not example-shop.ie. No DKIM alignment.
2. "spf=pass ... bounce.mcsv.net" → SPF passes, but for Mailchimp's bounce
   domain. ESP-sent mail almost never aligns on SPF; that's expected.
3. Neither passing mechanism aligns with header.from=example-shop.ie →
   "dmarc=fail". Gmail requires bulk senders' From domain to align with SPF
   or DKIM; unaligned bulk mail is filtered regardless of content quality.
4. "Nothing changed on our end" is consistent, not contradictory: the config
   was always unaligned. What changed is receiver-side enforcement — the
   failure onset tracks Gmail's enforcement tightening, not any send.

RULED OUT:
- Reputation: same shared Mailchimp pool for years; a pool problem would not
  produce a clean dmarc=fail in every header.
- Content: not examined — the failure is fully explained upstream at layer 1,
  and content cannot rescue unaligned bulk mail.

CONTRIBUTING FACTORS: p=NONE means the sender gets no DMARC reports and has
been blind to this for as long as it's existed.

CONFIDENCE: High — the receiver's own verdict line states the mechanism.
Overturning evidence would be headers from an affected recipient showing
dmarc=pass, which would reopen the reputation layer.
```

---

## Example 2 — Cold outreach suddenly bouncing at Outlook

**Presenting symptom:** "Half our outbound campaign to corporate targets started bouncing this week."

**Evidence supplied (Tier B):** An NDR containing:

```
550 5.7.515 Access denied, sending domain outreach-acme.com does not meet
the required authentication level.
```

**Diagnosis:**

```
DIAGNOSIS: The sending domain has no DMARC record (or fails one of
SPF/DKIM/DMARC outright), and Microsoft's high-volume sender enforcement is
rejecting it at the door — this is a compliance rejection, not a reputation or
content judgment.

EVIDENCE CHAIN:
1. "550 5.7.515 ... does not meet the required authentication level" → this
   specific code is Microsoft's enforcement response for senders over ~5,000
   msgs/day to consumer Microsoft domains that lack passing, aligned
   SPF + DKIM + DMARC (enforced from May 2025; see
   reference/bulk-sender-rules.md).
2. Onset "this week", across many recipients at once, with a uniform SMTP
   code → receiver-side policy gate, not gradual reputation decay (decay
   produces junking and throttling before outright 550s).
3. "Half the campaign" ≈ the Microsoft-hosted share of the target list —
   consistent with a single-receiver policy cause.

RULED OUT:
- IP/domain reputation blocklisting: would return different codes (5.7.1,
  S3150, blocklist references), not 5.7.515.
- Content/spam filtering: rejection happens at authentication evaluation,
  before content scoring.

CONTRIBUTING FACTORS: A cold-outreach domain separate from the primary brand
domain ("outreach-acme.com") is often set up quickly and never given a DMARC
record — the setup pattern that walks straight into this gate.

CONFIDENCE: High — the receiver states the cause in the bounce text. A DNS
check of outreach-acme.com (missing/invalid _dmarc record, or unaligned
SPF/DKIM) would make it conclusive.
```

---

## Example 3 — "We're landing in Promotions"

**Presenting symptom:** "Gmail is putting our launch emails in Promotions. Our deliverability is broken."

**Evidence supplied (Tier A):** Headers from an affected recipient:

```
Authentication-Results: mx.google.com;
       dkim=pass header.d=example-studio.com;
       spf=pass; dmarc=pass (p=QUARANTINE) header.from=example-studio.com
Delivered-To: recipient@gmail.com
```

**Diagnosis:**

```
DIAGNOSIS: Nothing is broken. The mail is fully authenticated, aligned, and
delivered; Promotions is Gmail *classifying* commercial mail as commercial
mail, which is a categorization outcome, not a deliverability failure.

EVIDENCE CHAIN:
1. dkim=pass with aligned d=, dmarc=pass → authentication layer clean.
2. "Delivered-To" present, message in a visible tab → the mail was accepted
   and inboxed. Spam filtering rejects or junks; it does not file into tabs.
3. The artifact is a marketing send (offer copy, promo imagery, tracking
   links) → Promotions is the *designed* destination for this mail class.

RULED OUT:
- Spam filtering: the message is not in the spam folder.
- Reputation: an authenticated, dmarc=pass message delivered to a tab is not
  a reputation event.

CONTRIBUTING FACTORS: None.

CONFIDENCE: High. The honest finding is that there is no pathology to
diagnose — reporting one anyway would be malpractice. (Whether Promotions
placement matters commercially is a strategy question outside this
diagnostician's scope.)
```
