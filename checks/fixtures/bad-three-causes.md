DIAGNOSIS: There are several causes here working together:
1. Your DKIM is signed by Mailchimp's domain, not yours.
2. Your list may have decayed over time.
3. Gmail has tightened its filtering recently.

EVIDENCE CHAIN:
1. "dkim=pass header.i=@mcsv.net header.s=k1" → signed by Mailchimp's domain.
2. "dmarc=fail (p=NONE sp=NONE dis=NONE) header.from=harboursupplies.ie" →
   the receiver's verdict.

RULED OUT: Nothing conclusively.

CONTRIBUTING FACTORS: See list above.

CONFIDENCE: Moderate — several factors are plausible.
