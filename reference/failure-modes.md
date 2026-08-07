# Failure modes — ranked by how often each is the true primary cause

Use this as the prior-probability table when evidence is thin, and as a cross-check when it's rich. Ranking reflects bulk-sender reality since the 2024–2025 mailbox-provider rule changes.

## 1. DMARC alignment failure (ESP signs with its own domain)

The sender's From domain is theirs; the DKIM signature and SPF envelope belong to the ESP. Authentication "passes" but nothing aligns. Harmless for years, now a filtering/rejection offence for bulk senders at Gmail, Yahoo, and Microsoft.

**Signature in evidence:** `dkim=pass header.d=<esp-domain>` + `dmarc=fail` in headers; DMARC aggregate reports showing high volume with 0% alignment from ESP IPs.
**Commonly misdiagnosed as:** content problems, "the algorithm changed."

## 2. Missing or broken DMARC under bulk-sender rules

No `_dmarc` record at all, a syntactically invalid one, or SPF `permerror` (e.g., more than 10 DNS lookups) that silently voids one alignment path. Bites hardest at Microsoft (outright `550 5.7.515` rejections since May 2025) and at Gmail/Yahoo for 5,000+/day senders.

**Signature:** uniform 550-series bounces naming authentication; `spf=permerror` in headers.
**Misdiagnosed as:** blocklisting, reputation collapse.

## 3. Self-inflicted domain reputation damage

A volume spike from a young or quiet domain, a purchased or scraped list (spam-trap hits), or a complaint rate crossing 0.1% (degraded) toward 0.3% (no mitigation eligibility at Gmail). Reputation damage is gradual-onset and recipient-provider-specific.

**Signature:** Postmaster Tools domain reputation Low/Bad; complaint rate trend; failure correlated with one provider while others deliver fine.
**Misdiagnosed as:** ESP problems, content problems.

## 4. Shared IP pool reputation (the neighbourhood, not the house)

On shared ESP pools, other tenants' behaviour moves your placement. Distinguishing mark: sender's own auth and complaint metrics are clean, yet placement degrades across many of that ESP's customers at once.

**Signature:** clean `dmarc=pass` headers + junk placement; blocklist entries for the ESP's IP ranges; timing matches other users of the same ESP reporting issues.
**Misdiagnosed as:** something the sender did.

## 5. List decay and engagement collapse

Old lists go stale: recipients churn jobs, abandon mailboxes, stop opening. Mailbox providers read sustained non-engagement as unwantedness. Slow-onset, all-providers, no auth anomalies.

**Signature:** gradual multi-month decline; bounce rate creeping up; no header or bounce anomalies at all.
**Misdiagnosed as:** deliverability failure (it is an audience failure).

## 6. Infrastructure misconfiguration (miscellaneous)

Broken or missing reverse DNS/PTR, no TLS, forwarding chains that break DKIM without ARC, a CNAME migration that silently dropped DKIM selectors, an expired selector after an ESP migration.

**Signature:** provider-specific or path-specific failures; `dkim=fail (signature verification failed)` on forwarded mail; onset matching a DNS or platform change.

## 7. Content triggers (genuinely rare as primary cause)

Content is the most-accused, least-convicted layer. When it *is* primary: link-shortener domains (bit.ly etc.) with poor reputation, link-text/href mismatch, a blocklisted domain in the body, attachment types. "Spammy words" almost never sink authenticated, wanted mail on their own.

**Rule:** only convict content when layers 1–3 are demonstrably clean.

## 8. Not-a-failure presentations

Presentations that arrive as failures but aren't:

- **Promotions/Updates tab placement** — classification, not filtering.
- **Open-rate shifts from measurement change** — Apple Mail Privacy Protection inflates then plateaus opens; a mix shift toward MPP or away from it moves the metric without delivery changing.
- **Seasonality** — bulk engagement moves with the calendar.
- **One anecdotal "it went to junk"** — a single recipient's personal filters, prior interactions, or corporate gateway. One data point is not a pattern.

## Benchmarks (what "normal" looks like)

- Spam complaint rate: healthy < 0.1%; ≥ 0.3% = Gmail mitigation ineligibility territory.
- Hard bounce rate: healthy < 2%; > 5% signals list-quality pathology.
- DMARC aggregate alignment for a correctly configured bulk sender: ~100% of own-sent volume. Anything materially below is finding #1 or #2.
- Open rates: treat as directional only (MPP distortion). Reply rate is the honest metric for cold outreach; click rate for newsletters.
