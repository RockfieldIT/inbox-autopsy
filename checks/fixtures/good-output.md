DIAGNOSIS: The newsletter fails DMARC alignment because the sending domain was
never authenticated in Mailchimp — DKIM is signed with Mailchimp's domain
rather than harboursupplies.ie — and Gmail filters unaligned bulk mail under
its sender requirements.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@mcsv.net header.s=k1" → the signature verifies, but
   for mcsv.net (Mailchimp), not the sender's domain. No DKIM alignment.
2. "spf=pass ... smtp.mailfrom=" → SPF passes for Mailchimp's bounce domain
   only; expected on any ESP and contributes nothing to alignment.
3. "dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=harboursupplies.ie" →
   the receiver's own verdict: neither passing mechanism aligns with the
   From domain.

RULED OUT: Reputation — a uniform dmarc=fail in the receiver's verdict fully
explains the placement upstream. Content — not examined; the failure is
established at the authentication layer.

CONTRIBUTING FACTORS: "(p=NONE sp=NONE)" means the sender receives no
enforcement and, as typically configured, no reports — the failure has been
invisible for as long as it has existed.

CONFIDENCE: High — the receiving provider's verdict line states the
mechanism. Overturning evidence would be headers from an affected recipient
showing dmarc=pass.
