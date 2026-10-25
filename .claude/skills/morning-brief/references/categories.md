# Gmail queries per area

Run each with `gws gmail +triage --max <N> --query "<query>" --format json`. The JSON is `{"messages":[{id, date, from, subject}, ...]}` — print just `id | date | from | subject` per row to keep the output small. `+triage` defaults to `is:unread`, but passing `--query` replaces that — so the area queries below see read mail too (intentional: an opened bill is still unpaid).

Tune these when Soumyanil says something was missed or is noise. Add the actual sender domains as you learn them (e.g. his card issuers, insurers).

| Area | Query | Max | What counts as actionable |
|---|---|---|---|
| General unread | `is:unread newer_than:3d -category:promotions -category:social` | 40 | Anything addressed to him personally with a question or deadline |
| Credit cards | `(subject:(statement OR "payment due" OR "due date" OR "minimum amount" OR "total amount due") OR "credit card") newer_than:35d -category:promotions` | 25 | Statement with amount + due date and no later "payment received" for that card |
| Card/bill payment done | `("payment received" OR "thank you for your payment" OR "payment successful" OR "received your payment") (card OR bill OR premium) newer_than:20d` | 15 | Not an action — use it to cross off bills already paid |
| Insurance | `subject:(premium OR "policy renewal" OR "renewal due" OR "renewal notice" OR insurance OR "policy lapse" OR "grace period") newer_than:45d -category:promotions` | 20 | Premium/renewal due, lapse warning, claim update. (Keep it subject-scoped: a body search for "policy" matches every privacy-policy footer) |
| Loans / EMI / bank | `(EMI OR "loan" OR "auto debit" OR "mandate" OR "insufficient balance" OR "bounce") newer_than:15d -category:promotions` | 15 | Failed debit, EMI due with low-balance warning |
| Trading & investing | `(from:(angelone.in OR angelbroking.com OR zerodha.com OR zerodha.net OR nse.co.in OR nseindia.com OR bseindia.com OR cdslindia.com OR nsdl.co.in OR camsonline.com OR kfintech.com) OR "margin" OR "contract note" OR "IPO" OR "buyback" OR "rights issue" OR "corporate action") newer_than:7d` | 30 | Margin shortfall / penalty, pledge requests, IPO/buyback/rights windows closing, failed SIP, unusual trade alert. Daily contract notes and fund-balance mails = FYI only |
| US stocks | `(from:(vested.co.in OR indmoney.com OR interactivebrokers.com) OR "W-8BEN" OR "LRS") newer_than:14d` | 10 | Form renewals, funding/remittance issues |
| IT / job | `(LTIM OR LTIMindtree OR "LTI Mindtree" OR recruiter OR interview OR "job opportunity" OR from:(naukri.com OR linkedin.com OR instahyre.com OR foundit.in)) newer_than:7d -category:promotions` | 25 | LTIM mails needing reply, interview invites, recruiters for relevant roles. LinkedIn "you appeared in N searches" = skip |
| Malkan | `(from:malkansview.com OR malkan OR "Vishal Malkan" OR Malkansview) newer_than:21d` | 15 | Upcoming live session/webinar (date, time IST, joining link), recordings, assignments. Senders seen: Team Malkansview / "Anybody Can Trade with AI" (webinar reminders), Meghana V Malkan "Mind Your Money" (newsletter = FYI) |
| Store | `(saree OR Surat OR Burrabazar OR "Marg ERP" OR margerp OR "Zoho Inventory" OR Wati OR ManyChat OR Looksy OR "AI Vastra" OR "Ma Lakhsmi" OR "Ma Lakshmi" OR quotation OR "GST registration") newer_than:14d -category:promotions -from:(zomato.com OR myntra.com OR swiggy.in OR amazon.in)` | 25 | Vendor/manufacturer replies, quotes, demo calls, GST/registration mail, tool trial expiries. Empty is normal pre-launch — then lean on `context/current-priorities.md` for the store items |
| Open complaints / tickets | `(complaint OR ticket OR grievance OR escalation) newer_than:21d -category:promotions` | 10 | A ticket he raised that's still waiting on him, or a reply that needs a response. Resolved tickets → FYI once, then drop |

## Known senders & noise (learned 2026-10-24)
- **Cards:** ICICI (credit_cards@icici.bank.in, card xx6010; CRED and Amazon Pay send duplicate reminders for the same bill — merge them), SBI Card (Statements@sbicard.com, BPCL Octane; amount is only inside the password-protected PDF → show "see PDF"), Axis card xx2038 spend alerts, HDFC cards xx8785 / xx7745.
- **Noise:** HDFC "Loan on Card Update" / "Higher Loan Eligibility" = marketing. Per-transaction spend/UPI alerts = skip (unless a large unexplained debit). IPO promos from INDmoney/Upstox/Nuvama/HDFC = one FYI line at most. Zerodha daily margin statements / contract notes and nse-direct "Trades executed" = FYI only.
- **SBI "KYC renewal"** mails come via a tracking-link domain — fine to mention, but tell him to renew via the SBI Card app, not the email link.
- **Security alerts** (GitHub/Google "new app authorized", new sign-in) → FYI with a "was this you?" line.

## Dedup
The same message can hit several queries (e.g. an LTIM salary credit hits Bank and IT). Put it in the area where the action lives, once.

## Calendar keyword hints
Use these to tag events into areas: "Malkan"/"webinar"/"live session" → Malkan; "standup"/"sprint"/"LTIM"/Teams links → IT; vendor names, "Surat", "Burrabazar", "demo" with Marg/Zoho/Wati → Store; "expiry"/"results" → Trading.
