EXPECTED PRIMARY CAUSE (do not show to the diagnostician): Failure mode #3 —
self-inflicted domain reputation damage: a purchased list of 18,000 addresses
plus a volume ramp from ~150/day to ~3,000/day burned the sending domain's
reputation (Postmaster domain rep High → Bad, spam rate through the 0.3%
ceiling, 6.4% hard bounces = spam-trap territory). Authentication is fully
clean, which is the trap: a weak diagnostician sees dmarc=pass and starts
blaming content or the tool. The vendor's "verified list" claim is the decoy.

