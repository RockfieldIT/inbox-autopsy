DIAGNOSIS: The newsletter is junked because the sending IP 205.201.131.84 is
listed on a public blocklist, which Gmail honours for bulk senders.

EVIDENCE CHAIN:
1. "205.201.131.84 LISTED on Spamhaus SBL" → the sending IP carries a live
   blocklisting.
2. "dkim=pass header.i=@mcsv.net header.s=k1" → authentication passes but
   cannot outweigh a blocklisted source.

RULED OUT: Alignment — treated as secondary to the blocklisting.

CONTRIBUTING FACTORS: None.

CONFIDENCE: High — the blocklist entry is decisive.
