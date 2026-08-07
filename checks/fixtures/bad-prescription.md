DIAGNOSIS: The newsletter fails DMARC alignment because the sending domain was
never authenticated in Mailchimp — DKIM is signed with Mailchimp's domain
rather than harboursupplies.ie.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@mcsv.net header.s=k1" → the signature verifies, but
   for mcsv.net (Mailchimp), not the sender's domain.
2. "dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=harboursupplies.ie" →
   the receiver's own verdict.

RULED OUT: Content — not examined; the failure is upstream.

CONTRIBUTING FACTORS: To fix this, go to Mailchimp and set up a custom
authenticated domain, then publish a DMARC record for harboursupplies.ie.
We recommend p=quarantine once alignment is confirmed.

CONFIDENCE: High — the receiving provider's verdict line states the mechanism.
