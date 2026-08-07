# Evidence collection — exact click-paths for non-technical users

Give these steps to the user verbatim (adapted to their situation), one stage at a time. Never assume they know where anything is.

## 1. Raw headers ("the hidden technical information attached to every email")

Best sample: a message from the **same campaign type that failed**, in a mailbox at the **affected provider**. A seed test works: send today's newsletter/campaign to your own address there, then:

**Gmail (web):** open the email → click the **⋮** (three dots, top right of the message) → **Show original** → a new tab opens → click **Copy to clipboard** → paste the whole thing into the chat.
*Tell the user: the new tab also shows a plain-English summary table (SPF / DKIM / DMARC with PASS or FAIL) — a screenshot of that table alone is already useful.*

**Gmail (mobile app):** headers aren't available — have them do it from a computer browser, or forward the message to an address they can open on a computer.

**Outlook.com / Microsoft 365 (web):** open the email → **⋯** (top right) → **View** → **View message source** → select all → copy → paste.

**Outlook desktop (Windows):** double-click the email to open it in its own window → **File** → **Properties** → copy everything in the **Internet headers** box (it scrolls — Ctrl+A inside the box first).

**Apple Mail (Mac):** open the email → menu bar **View** → **Message** → **All Headers**, then copy the header block. (**Raw Source** works too and includes everything.)

**Yahoo Mail (web):** open the email → **⋮** → **View raw message**.

**Common stumble:** the user pastes the visible email body instead of the headers. Check for an `Authentication-Results:` line; if absent, gently rerun the steps.

## 2. Bounce messages (NDRs)

Ask them to search their inbox for mail from **"Mail Delivery Subsystem"**, **"postmaster"**, or **"Microsoft Outlook"** with subjects like "Undeliverable" or "Delivery Status Notification (Failure)" — and paste the **entire message**, especially the technical block with a code like `550 5.7.515`. That block is the receiving server explaining its refusal in its own words.

If sends go through an ESP, individual bounces land in the platform, not their inbox: campaign report → bounced/undelivered detail → open one bounce and copy the reason text (most ESPs show the raw SMTP response).

## 3. Platform (ESP) statistics

Ask for, per recent campaign: **delivered %, hard bounce %, spam-complaint %**, and open/click trend across the affected period. Screenshots are fine. Where: Mailchimp → campaign → View Report; Beehiiv → Posts → post → Analytics; Kit → Broadcast → stats; cold-email tools → campaign analytics. If the platform breaks stats down **by mailbox provider** (Gmail vs Outlook vs other), that split is diagnostic gold — ask for it.

## 4. Google Postmaster Tools (for Gmail-heavy problems)

Only the domain owner can see this. If they already use it: ask for screenshots of **Domain reputation**, **IP reputation**, and **Spam rate** for the affected period. If they've never set it up, it starts collecting only *after* verification — note it as a gap, don't send a non-technical user off on a DNS errand mid-diagnosis; diagnose from what exists.

## 5. DMARC aggregate reports

If (and only if) the user mentions DMARC reports or has an inbox/service receiving them: an XML attachment or a dashboard screenshot showing **volume, sending sources, and SPF/DKIM alignment rates** is tier-C gold. Otherwise skip — explaining RUA setup is a fix, not a diagnosis, and out of scope.

## 6. DNS lookups (the diagnostician can describe; the user rarely needs to run them)

When a hypothesis needs the live DNS state (does a `_dmarc` record exist? which DKIM selectors resolve?), prefer asking the user to run a free web checker (e.g. MXToolbox: "type your domain, choose DMARC Lookup, screenshot the result") over teaching them `dig`. One lookup per request; say exactly what to type and what to screenshot.
