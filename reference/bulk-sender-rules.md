# Bulk-sender rules — the receiver-side rulebook

The 2024–2025 mailbox-provider requirements are the reason many long-standing configurations suddenly became failures. When a symptom's onset is "recently, and nothing changed on our end," this file is usually why.

> Enforcement details evolve. If onset timing is central to a diagnosis, verify the current state of these rules before relying on a date.

## Gmail (Google) — from February 2024, escalating since

Applies in full to senders of **~5,000+ messages/day to personal Gmail accounts** (bulk-sender status, once acquired, is permanent). Requirements:

- **SPF and DKIM** both passing.
- **DMARC record** published (minimum `p=none`).
- **Alignment**: the From-header organizational domain must align with the SPF *or* DKIM organizational domain. This is the clause that convicts unauthenticated ESP setups.
- **Spam rate** (Postmaster Tools): stay under **0.1%**; at **0.3%+** the sender becomes ineligible for mitigation (June 2024 onward).
- **One-click unsubscribe** (RFC 8058 `List-Unsubscribe` + `List-Unsubscribe-Post`) on marketing/promotional mail; honored within 48 hours.
- TLS for transmission; valid forward and reverse DNS (PTR) for sending IPs.
- Enforcement escalated from temporary failures to **temporary and permanent rejections** of non-compliant traffic (escalation phase from late 2025).

## Yahoo — mirrors Gmail

Same February 2024 wave, same substance: auth + DMARC for bulk senders, one-click unsubscribe, complaint-rate threshold in the same band. Diagnostically, treat Gmail and Yahoo as one rulebook; evidence from one usually generalizes to the other.

## Microsoft (Outlook.com / Hotmail / Live) — from May 5, 2025

Applies to senders of **5,000+ messages/day** to Microsoft consumer domains:

- **SPF pass, DKIM pass, and DMARC** (minimum `p=none`) aligning with SPF or DKIM (ideally both).
- Non-compliant mail is rejected with **`550 5.7.515 Access denied, sending domain <domain> does not meet the required authentication level`** — the single most recognizable artifact of this rule. (Initial enforcement routed to junk; rejection followed.)
- Hygiene expectations: functional From/Reply-To, visible working unsubscribe, list hygiene and bounce management, non-deceptive headers.

Note: these are Microsoft's *consumer* rules. Corporate M365 tenants additionally filter via their own policies (SCL/BCL thresholds, tenant allow/block lists) — a rejection from one company's tenant is not evidence about the consumer rulebook.

## Diagnostic use of this file

1. **Onset dating.** Failure clusters near an enforcement wave + evidence of non-compliance = strong causal candidate. The config didn't change; the rules did.
2. **Threshold check.** Under ~5,000/day the *hard* requirements don't formally bind — but providers apply the same signals softly at lower volumes, and cold-email senders often cross thresholds in bursts they don't track.
3. **Symptom → rulebook mapping.** `5.7.515` → Microsoft rule. Gmail junking with `dmarc=fail` → alignment clause. Mitigation refusals with 0.3%+ spam rate → Gmail complaint clause. One-click header absent on marketing mail → compliance gap that caps reputation even when auth is clean.

## Primary sources

- Gmail: Email sender guidelines — https://support.google.com/a/answer/81126 and FAQ https://support.google.com/a/answer/14229414
- Yahoo: Sender best practices — https://senders.yahooinc.com/best-practices/
- Microsoft: Outlook high-volume sender requirements — https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%90s-new-requirements-for-high%E2%80%90volume-senders/4399730
- RFC 8058 (one-click unsubscribe) — https://www.rfc-editor.org/rfc/rfc8058
