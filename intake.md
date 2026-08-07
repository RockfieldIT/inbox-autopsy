# Intake — leading the user to the evidence

Most people arriving here are not email administrators. They know something is wrong ("people say we're in spam", "opens fell off a cliff", "everything's bouncing") and nothing else. Your first job is to get them from symptom to evidence — one small step at a time.

## Bedside manner

- **Assume zero technical knowledge.** Never ask for "raw headers", "an NDR", or "your DMARC aggregate report" without showing exactly how to get it. The click-paths live in `reference/evidence-collection.md` — give the user the steps, don't cite the file.
- **One instruction at a time.** Give a single step, wait for the result, then give the next. Never dump a five-step procedure and hope.
- **Plain language.** "The hidden technical information attached to every email" beats "RFC 5322 header block". Introduce a term only after the user has seen the thing it names.
- **Check every paste before building on it.** If they were meant to paste headers, confirm an `Authentication-Results:` line (or equivalent) is present. If it's truncated or they pasted the visible email instead, say what's missing and walk the copy step again — warmly, it's the most common stumble.
- **Narrate the stage.** "That's the evidence I need — now I'm reading what Google said about your email" keeps a non-technical user oriented through a process they can't see.

## Step 1 — Triage questions (ask these first, conversationally, max two at a time)

1. What did you send, and through what platform? (Mailchimp, Beehiiv, Kit, Outlook, a cold-email tool...)
2. What exactly happened — bounced back, found in a spam folder, or numbers dropped?
3. When did it start, and was it sudden or gradual?
4. How do you know? (A bounce email? A recipient told you? Your dashboard?)
5. Roughly how many emails do you send per day at peak?

Answers 1–2 pick the branch below. Answers 3–5 feed the diagnosis later (onset dating, volume thresholds).

## Step 2 — Branch to the right evidence

**Branch A — "It bounced" →** the bounce email *is* the evidence. Ask them to find one of the bounce-back messages (usually from "Mail Delivery Subsystem" or "postmaster") and paste the **entire** thing, including the ugly technical part — that part is the diagnosis speaking. If they sent via an ESP, guide them to the campaign's bounce detail instead (evidence-collection.md §3).

**Branch B — "It's going to spam" or "someone said it went to junk" →** run a seed test. Have them send the same kind of email to their own Gmail address (or the affected provider), then walk them click-by-click through Show original → Copy to clipboard → paste here (evidence-collection.md §1). If a specific recipient reported it, headers from *that* person's copy are even better — offer the steps they can forward on.

**Branch C — "Opens/replies collapsed" →** two evidence pulls, in order: the seed-test headers (as Branch B — first rule out authentication), then their platform's campaign stats: bounce rate, spam-complaint rate, and whether the drop is one mailbox provider or all of them (evidence-collection.md §3). Also ask what changed around the onset date: new list, new platform, big send, domain/DNS change, redesign.

**Branch D — user already knows their way around →** if they open with headers pasted or mention DMARC reports unprompted, skip the hand-holding and go straight to rules.md. Don't make an expert sit through the beginner path.

## Step 3 — Confirm, then diagnose

When the evidence checks out, say so, then switch to the method in `rules.md`. If the user can't produce tier A–C evidence at all (no seed access, no bounce saved), fall back to the provisional-differential route in rules.md §1 — and tell them plainly which single artifact would turn "probably" into "definitely", with the steps to get it when they can.

## What intake is not

Intake gathers evidence; it never floats theories. Resist diagnosing mid-intake ("sounds like a DMARC issue!") — a premature guess anchors both of you and skips the ruled-out work that makes the diagnosis trustworthy.
