# ESP quirks — who signs with what, by default

The most common root cause in the wild (failure-mode #1) is platform-specific: what an ESP does *before* the sender sets up custom domain authentication. This table is the lookup.

> Defaults drift as platforms update. Treat this as the expected pattern and verify the live behaviour in the actual headers — the headers always win.

| Platform | Default (no custom domain auth) | After domain authentication | Notes |
|---|---|---|---|
| **Mailchimp** | DKIM signed `d=mcsv.net`/`mcdlv.net`; SPF passes for Mailchimp bounce domain. From domain unaligned → `dmarc=fail`. Gmail may show "via mailchimp". | Two CNAME records (k2/k3 selectors) → DKIM signs with sender's domain; DMARC aligns via DKIM. SPF still never aligns (Mailchimp envelope). | Mailchimp's own docs now push authentication + DMARC to meet Gmail/Yahoo rules. |
| **Kit (ConvertKit)** | Sends from Kit's shared infrastructure/domains; unaligned for custom From domains. | Verified custom sending domain → aligned DKIM. | Creators on the free tier historically stayed on shared defaults. |
| **Beehiiv** | Sends via Beehiiv's mail domain; From on shared setup is Beehiiv-controlled or unaligned. | Custom sending domain (paid tiers) → aligned DKIM. | Beehiiv docs explicitly walk through DMARC for custom domains. |
| **Substack** | From address is effectively a substack.com identity, and Substack authenticates its own domain — so there's usually **no alignment failure by design**. | Custom domains affect the web publication more than mail auth. | If a Substack sender reports spam placement, look at reputation/engagement, not alignment. |
| **Brevo / MailerLite / similar mid-market ESPs** | Shared signing domain until sender adds DKIM records; unaligned. | DNS records → aligned DKIM. | Same pattern as Mailchimp. |
| **Microsoft 365** | DKIM enabled by default only for `onmicrosoft.com`; custom domains may send with the fallback signature until custom DKIM is enabled. SPF (`include:spf.protection.outlook.com`) **does** align because M365 uses the sender's own envelope domain. | Enabling DKIM for the custom domain (two selector CNAMEs) → both paths align. | M365 senders usually pass DMARC via SPF even with default DKIM — until they route through a third-party tool that breaks the envelope. |
| **Google Workspace** | Signs with the sender's domain once DKIM is set up; before that, a default `*.gappssmtp.com` signature (unaligned) with SPF alignment usually carrying DMARC. | Standard. | Same "aligned via SPF until a relay breaks it" caveat as M365. |
| **Cold-email tools (Instantly, Smartlead, lemlist...)** | Send *through* the user's own Google/M365 mailboxes, so authentication usually aligns out of the box. | n/a | Their failure modes live in reputation and behaviour (volume ramp, list quality, spintax patterns, tracking domains), not alignment. Check the tracking/click domain — often a shared shortener with poor reputation. |

## Diagnostic implications

- `dmarc=fail` + ESP in the `Received` chain → check this table before anything else; the cause is probably a never-completed domain authentication setup.
- SPF alignment is structurally impossible on most ESPs (they must use their own bounce domain for bounce processing). **DKIM is the only alignment path for ESP mail** — which is why a missing pair of CNAME records can be the entire diagnosis.
- A sender who "authenticated years ago" can still regress: domain migrations, DNS provider switches, and ESP account moves silently drop selector CNAMEs. Match the `s=` selector in the header against what's live in DNS.
- Mail that aligns from the ESP but fails from the sender's *transactional* or *CRM* stream (or vice versa) means multiple sending systems share one From domain — diagnose per stream, not per domain.
