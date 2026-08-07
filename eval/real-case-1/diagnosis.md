DIAGNOSIS: The email was handed to Google by the VoIP provider's mail server
(mail.voip-provider.example), which is not an authorized, authenticated sender for
rockfieldit.com — it produced no aligned SPF or DKIM for your domain — and
rockfieldit.com publishes an enforcing DMARC policy, so Google did exactly
what that policy instructs and rejected the message at the door.

EVIDENCE CHAIN:
1. "This is the mail system at host mail.voip-provider.example" and "Received: by
   mail.voip-provider.example (Postfix)" → the original message left through the VoIP provider's
   server, not the Microsoft 365 tenant that handles your day-to-day
   rockfieldit.com mail. This is a separate sending stream.
2. "550-5.7.26 Unauthenticated email from rockfieldit.com is not accepted due
   to 550-5.7.26 domain's DMARC policy" → Google's own verdict: the message
   claimed to be from rockfieldit.com, passed neither authentication path in
   alignment with that domain, and your domain's published DMARC policy told
   Google to refuse such mail. This rejection text only appears when the
   domain has an enforcing policy — the refusal is your own domain's standing
   instruction being obeyed.
3. "(in reply to end of DATA command)" → Google accepted the connection and
   the recipient address, then refused after seeing the full message — the
   pattern of an authentication-policy rejection, not a bad address.
4. From the bounce's own delivery headers: "spf=none (sender IP is
   203.0.113.41)" and "mail.voip-provider.example does not designate permitted sender
   hosts" with "dkim=none (message not signed)" → the VoIP provider's server sends
   without SPF authorization or DKIM signing even for its own hostname —
   consistent with it having no authentication for rockfieldit.com either.

RULED OUT:
- Blocklisting / IP reputation: Google's blocklist and reputation rejections
  use different codes and text (5.7.1, blocklist references). 5.7.26 is
  specifically an authentication verdict.
- Content or spam filtering: the refusal text names DMARC and nothing else;
  no spam classification appears.
- Bad recipient address: a nonexistent mailbox returns "user unknown"
  (550 5.1.1); Google knew the address and refused the message instead.
- Your Microsoft 365 sending path: not implicated by this artifact — the
  failed message never went through it.

CONTRIBUTING FACTORS: The DMARC policy itself is not the pathology — it is
doing its designed job of refusing mail that claims your domain without proof.
The pathology is that a legitimate message travelled an unauthenticated path.

CONFIDENCE: High — the receiver states the mechanism in its own refusal text.
Two checks would make it conclusive: (1) a DMARC lookup on rockfieldit.com
(MXToolbox: type rockfieldit.com, choose DMARC Lookup, screenshot the result)
to see the enforcing policy Google acted on; (2) an SPF lookup on the same
domain to confirm 203.0.113.41 / the VoIP provider is absent from your authorized
senders.
