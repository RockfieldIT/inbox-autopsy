# Header forensics — reading the biopsy sample

Raw headers contain the receiving provider's own authentication verdicts. This file is how to read them.

(If the user hasn't supplied headers yet, don't read this file at them — walk them through getting a sample via `intake.md` and the click-paths in `evidence-collection.md`.)

## The line that matters most: `Authentication-Results`

Read the verdict stamped by the *receiving* provider (e.g. `mx.google.com`). Ignore any `Authentication-Results` added by intermediate hops for the primary verdict.

```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of bounce.esp.com designates 1.2.3.4 as permitted sender) smtp.mailfrom=bounce.esp.com;
       dkim=pass header.d=esp.com header.s=k1;
       dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=sender.ie
```

### SPF — pass *for whom*?

SPF is evaluated against the **envelope-from** (`smtp.mailfrom`), not the visible From header. ESP-sent mail almost always shows `spf=pass` for the *ESP's* bounce domain — that pass contributes nothing to DMARC alignment. `spf=permerror` usually means a broken record (commonly >10 DNS lookups) and silently removes SPF as an alignment path. `spf=softfail`/`fail` means the sending IP isn't authorized at all.

### DKIM — the `d=` is the whole story

`dkim=pass` alone means "some signature verified." The question is **`header.d=`**: whose domain signed? If `d=` is the ESP's domain, the sender's domain gets no credit. Multiple `dkim=` results can appear (ESP signs with both its domain and the customer's); only a passing signature whose `d=` aligns with the From domain helps DMARC. `dkim=fail (signature verification failed)` on otherwise-fine mail usually means the body was modified in transit — classic on forwarding chains and gateways that rewrite content.

### DMARC — the verdict that filtering actually uses

`dmarc=pass` requires at least one of: SPF pass where `smtp.mailfrom`'s organizational domain matches `header.from`'s, or DKIM pass where `d=`'s organizational domain matches `header.from`'s. The `(p=...)` shown is the *sender's own published policy* — `p=NONE` means even the sender asks for no enforcement (but bulk-sender rules filter unaligned mail regardless of `p=`). `header.from=` names the domain being judged. **Diagnostic shortcut:** `dmarc=fail` + `dkim=pass d=<esp>` = failure-mode #1 (see failure-modes.md).

## ARC — when forwarding is in the chain

`ARC-Authentication-Results` preserves the original verdicts across forwarders (mailing lists, corporate redirects). If `Authentication-Results` shows failures but the ARC chain (`arc=pass`) carries original passes, the pathology is in the forwarding path, not the sender's config.

## The `Received` chain

Read bottom-up (oldest first). It answers: which IP actually handed the message to the receiver (match it against SPF and blocklist evidence), whether the path matches the claimed sending platform, and where any unexpected relay sits. Timestamps expose queuing delays (greylisting, throttling — themselves reputation symptoms).

## Provider-specific tells

- **Microsoft:** `X-Forefront-Antispam-Report` contains `SCL:` (Spam Confidence Level — ≥5 junks, 9 is high-confidence spam) and `BCL:` (Bulk Complaint Level — bulk-sender reputation on a 0–9 scale; junked when it crosses the tenant's bulk threshold, default 7, stricter tenants set 4–6). `CAT:SPM`/`CAT:HSPM`/`CAT:BULK` states *which* verdict junked it. These headers say whether Microsoft junked the mail as *spam* or as *bulk* — different causes.
- **Gmail:** exposes no spam score. The Authentication-Results line plus Postmaster Tools aggregate data is all you get; infer the rest from placement and population data.
- **`Precedence: bulk` / `List-Unsubscribe` / `List-Unsubscribe-Post: List-Unsubscribe=One-Click`:** presence/absence of the one-click pair matters for bulk-sender compliance (RFC 8058).

## Bounce (NDR) codes worth recognizing on sight

| Code / text | Meaning |
|---|---|
| `550 5.7.515 ... does not meet the required authentication level` | Microsoft high-volume sender enforcement: SPF/DKIM/DMARC compliance rejection |
| `550 5.7.1` + blocklist name (Spamhaus etc.) | IP or domain on a public blocklist |
| `550 5.7.26 ... does not pass authentication checks` (Gmail) | Gmail rejecting unauthenticated mail |
| `421 4.7.0` / temporary deferrals | Throttling or greylisting — reputation smoke, not yet fire |
| `553` / `550 5.1.1` user unknown | List hygiene, not deliverability |
