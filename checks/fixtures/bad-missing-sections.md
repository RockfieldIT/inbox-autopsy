DIAGNOSIS: The newsletter fails DMARC alignment because the sending domain was
never authenticated in Mailchimp.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@mcsv.net header.s=k1" → signed by Mailchimp's domain,
   not the sender's.
2. "dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=harboursupplies.ie" →
   the receiver's own verdict.

CONFIDENCE: High.
