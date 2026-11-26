# Daily Cyber Job Search — Runbook

Owner: Brandon Burns (Costa Mesa, CA). This repo is the shared state for the daily job search.
Every scheduled run follows this file. Change rules here, not in the scheduled-task prompts.

## Repo layout
```
base/Brandon_Burns_Resume.docx   base resume (source of layout)
base/Brandon_Burns_Resume.pdf
career/ExperienceLibrary.json    ONLY source of resume claims — never invent experience
career/profile.md                targets, location, eligibility, availability
career/voice-profile.md          cover-letter voice
tools/tailor.py                  builds tailored resume .docx from a JSON spec (keeps base formatting)
tools/base/                      unpacked base docx used by tailor.py
tools/coverletter.js             builds cover letter .docx from a JSON spec
data/seen.json                   every role ever evaluated {id: {first_seen, score, url, status}}
data/roles.json                  full scored list (latest state of every role)
inbox/linkedin-YYYY-MM-DD.json   roles captured by the Mac step after Brandon says "go" (LinkedIn, signed in)
daily/YYYY-MM-DD/                that day's output:
    report.md                    the morning list
    <role-id>/resume.docx, cover_letter.docx, notes.md
```

## Candidate snapshot (see career/profile.md for full)
- UCI B.S. CS (Networked Systems), June 2026; enrolled in UCI continuing-ed certificate program -> treat as a CURRENT STUDENT for "currently enrolled" requirements.
- US citizen, no sponsorship; clearance-eligible (no active clearance).
- Security+ exam Jan 2027. Strengths: AppSec/IAM (CommunicAI), Burp, Wireshark, web & network attacks, crypto, Python/Swift/Node/C/Java, GCP/Firebase.
- Gaps: SIEM/Splunk, incident response, vuln scanning, NIST/MITRE, no professional security job.
- Wants: Summer 2027 internships + junior/entry roles (summer start). Spring 2027 only if low-hour. Paid or unpaid.
- Location: within ~1 hr of Costa Mesa (OC, LA County incl. El Segundo/Torrance/Long Beach, Corona/Ontario edge, north SD County) or remote open to CA.

## Search (sources, in order)
1. Indeed MCP (`mcp__Indeed__search_jobs`, `get_job_details`) — many queries x locations (Irvine, Santa Ana, Long Beach, Los Angeles, El Segundo, Anaheim, remote), with and without job_type=internship.
2. WebSearch / WebFetch: company career pages and ATS boards (Greenhouse, Lever, Workday, iCIMS), Handshake previews, Built In LA, Simplify, Dice, LinkedIn job pages.
3. `inbox/linkedin-*.json` written by the Mac step (any not yet processed), plus any unprocessed `inbox/simplify-*.json` and `inbox/gmail-*.json`; set "processed": true after scoring.
4. SimplifyJobs GitHub lists (added 2026-11-24 at Brandon's request): run `python3 tools/simplify_feed.py --days 3 --out inbox/simplify-<date>.json`. It reads the structured listings.json behind github.com/SimplifyJobs/New-Grad-Positions and SimplifyJobs/Summer2027-Internships, keeps active security-titled roles in SoCal or remote (US), and skips URLs already in seen.json. Security roles are rare there (a handful a month), mostly "Software Engineer - Security" titles; score them like any other role (SWE-heavy roles usually land 4-6).
5. Gmail job-alert emails (added 2026-11-24): search `newer_than:2d` from LinkedIn job alerts (jobalerts-noreply@linkedin.com, jobs-listings@linkedin.com), Indeed (match.indeed.com), Handshake (notifications.joinhandshake.com), Built In, Simplify, ZipRecruiter, Glassdoor, Dice. Read each digest with get_thread (bodies are long: strip URLs before reading). Pull only security/cyber/IT-security roles that fit the location rule; ignore retail, driver, and generic SWE matches. Find the posting on the employer's site before scoring (alert links are tracking redirects). Read-only: never reply to, label, or delete these emails.
6. Government boards (added 2026-11-26, from Career Navigator search-jobs): USAJobs (keywords: cybersecurity, information security, IT specialist INFOSEC, Pathways student intern; locations: Orange County, Los Angeles, Long Beach, Seal Beach, El Segundo/LA AFB, remote), CalCareers (calcareers.ca.gov: Information Technology Associate/Specialist I with security focus, Information Security Officer trainee), and county/city boards on governmentjobs.com (Orange County, City of Irvine, Costa Mesa, Anaheim, Santa Ana, Huntington Beach, Long Beach, LA County, City of LA) for IT security, cyber and information security intern/analyst roles. Many of these state a close date: record it as the deadline. Note citizenship or clearance-eligibility lines (he's a US citizen, clearance-eligible).
7. Target companies (added 2026-11-26): check each company in career/profile.md "Target Companies" every run for new security/IT-security internship or entry roles, directly on its careers/ATS page (Greenhouse/Lever/Workday/Pinpoint `site:` queries if the page can't be fetched). Already-applied requisitions stay skipped via seen.json; new reqs at these companies get a one-line "Target company" tag in the report.
8. Wellfound (added 2026-11-26): search wellfound.com for security engineer/analyst intern or junior roles, LA/OC or remote-US. Startup listings often lack pay or level: score what's there and flag missing fields. Expect few hits.
Exclude: 4+ yrs required (see Experience rule below), active clearance already required, non-security helpdesk, gig "AI trainer" postings, roles already in data/seen.json (unless the posting materially changed or reopened).
Verify each new role is open by fetching the posting (or, for LinkedIn inbox roles, the Mac step's saved `description`). Save posting text to the role folder notes.

## Daily task: one merged run (Brandon, 2026-11-26)
There is ONE scheduled task, "Job search (daily, Mac)", at 8:34 Pacific. It is tied to Brandon's Mac, so it starts when the Mac is awake (sometimes hours late; Brandon accepted the delay). The old cloud-only 8:34 task "Daily cyber job search" is disabled. The prompt is in handoffs/mac-step-prompt.md.
- Part A (automatic): every non-LinkedIn source in "Search", scoring, tailoring, report, delivery, then a push: "<N> new roles, <M> scored 6+: <top two>. Reply go for LinkedIn + folder sync." No browser and no Mac writes before "go".
- Part B (on "go" in that chat):
1. Mac reachable check (remote-devices). If it's still unreachable, say so and wait for another "go".
2. LinkedIn capture in Brandon's signed-in Chrome (Claude in Chrome), read-only: never apply, save, message, connect or follow. Token budget:
   - Search results first. Pull only title/company/location/link from the results list with a page-text or JS extraction, never screenshots. Search last 7 days: cyber/security internships, security analyst, junior security engineer, SOC analyst; OC, Irvine, Long Beach, LA, plus CA remote. Also read his "Jobs based on your preferences" list (linkedin.com/jobs, "Show all"). The jobs-guest listing endpoints (/jobs-guest/jobs/api/seeMoreJobPostings/search and /jobs-guest/jobs/api/jobPosting/<id>) return clean HTML from inside a linkedin.com tab. Pace them (~1-2 s apart) because they rate-limit with 429. The external apply URL is in the logged-in /jobs/view/<id>/ page as a safety/go?url= link.
   - Triage before opening anything. Drop ids already in data/seen.json (git pull first), roles more than ~1 hr from Costa Mesa (Bay Area, San Diego proper, Edwards, out of state unless remote-CA), titles that are senior/lead/manager/principal, and non-cyber "security" (guard, industrial/acquisition security).
   - Open only the survivors (cap 15). Extract just the job description text, not the whole page.
   - Record per posting in inbox/linkedin-<date>.json: linkedin_job_id, linkedin_url, company, title, location, work_mode, posted, pay, seniority, description (full text), apply_url (employer link if exposed; "easy_apply" if Easy Apply), status_note, capture_error if any. Also list the triaged-out postings briefly (title, company, reason) so they go into seen.json.
3. Score and tailor in the same session, following the rest of this RUNBOOK. Tailor 6+, add a "LinkedIn (Mac step)" section to daily/<date>/report.md, update seen.json/roles.json, set the inbox file "processed": true, commit and push.
4. Sync the Mac folder per "Mac folder layout" (reports, new Application folders for Part A and Part B roles, CareerNavigator files). Closed or dropped roles' folders go to "Job Search/_to_delete/" (deletes are disabled on the Mac).
5. Send each new 6+ role's resume + cover letter (per Delivery rules) and a one-message ranked list. No push needed (Brandon is in the chat).
If Brandon never replies, Part A was the day's run (no LinkedIn).
One-off postings: when Brandon pastes posting text in chat, score it like any role (cheapest path, no browser).

## Experience rule (Brandon, 2026-11-23; loosened 2026-11-26)
Brandon counts about 2 years of hands-on security work (labs, projects) and about 4 years of CS work including school. He has no security internships or jobs.
- Score leniently (Brandon, 2026-11-26): unless a posting REQUIRES 4+ years, do not let years of experience drag the score down. Up to 3 years required (including "1-3 years", "2+ years", "3 years or equivalent"): at most -1 total for seniority, and none when the posting allows equivalent experience, projects or education. "Preferred" years never cost points.
- Exclude only when 4+ years are required, or the posting requires prior professional security employment with no equivalent allowed.
- When a skill or tool is "preferred"/"nice to have", missing it costs little. Judge required quals generously when his projects or coursework plausibly cover them (e.g., "experience with access control" is met by CommunicAI).
- Never write a years-of-experience number on a resume or cover letter. The resume claims only what is in ExperienceLibrary.json.

## Scoring (1-10)
Weights: Required quals met 40% | Keyword/skill match 25% | Eligibility (location, enrollment/grad window, citizenship) 20% | Seniority fit 15%.
- Hard eligibility fail (e.g., requires active TS clearance, must graduate between dates he can't meet and posting is strict, >1hr onsite) -> cap at 4 and say why.
- Grad-window mismatch where posting says "currently enrolled" -> he qualifies (certificate program). Where it says "pursuing a bachelor's" -> flag it, no deduction unless the posting is strict about it.
- AppSec/product security/IAM roles usually fit better than pure SOC roles; score honestly.
Record in notes.md: score, 2-line why, matched keywords, missing keywords, eligibility flags.

## Tailoring threshold
TAILOR_THRESHOLD = 6  (7 -> 5 on 2026-11-21, then 5 -> 6 on 2026-11-21 at Brandon's request: 5 produced too many roles; tailor every role scoring >= 6)
Below-threshold roles never get files, including roles Brandon sends as links: score them and report first (Brandon, 2026-11-23). Tailor a role under 6 only when he names that specific role and asks for files.
Every run (Brandon, 2026-11-23): auto-tailor every role scoring 6+. Score-5 and score-4 roles get NO files; list them in the report under "Need your call (5s and 4s)" with link, one-line why and main gap, and ask Brandon which (if any) to tailor. Add "+ K to review (4-5)" to the push notification when there are any. Scores of 3 and below are one-liners, no question.
No backfill needed. Roles scoring 5 that were already tailored keep their files; just don't tailor new 5s. Score-5 roles go in the report as one-liners without files.
In report sections, files and pushes below, "7+" means ">= TAILOR_THRESHOLD". For roles scoring 6, add one line in notes.md on the main risk (eligibility, timing, missing requirement).

## Tailoring (score >= TAILOR_THRESHOLD)
- Build a spec JSON and run `python3 tools/tailor.py spec.json daily/<date>/<id>/resume.docx`.
  - headline: role-aligned (e.g., "Application Security Intern Candidate | Cyber Security Analyst").
  - summary: 2-3 sentences mirroring the posting's top terms that are TRUE.
  - skills: reorder lines and items so the posting's keywords come first; may drop irrelevant lines (e.g., Data & AI) but never add skills not in ExperienceLibrary skills_section/units.
  - communicai_bullets: reorder; light rewording to use posting vocabulary for the same facts (e.g., "authorization controls" vs "access-control rules"). Keep every number accurate.
  - section_order: PROJECTS before EXPERIENCE (default) for technical roles.
- ATS check: run ResumeNext `analyze_resume` with the full resume text + job description; target >= 90 and note keyword coverage. Fix and rebuild if < 85.
- Cover letter: write from scratch per career/voice-profile.md (250-320 words, 3-4 paragraphs: why this team/role specifically; CommunicAI security proof; one more proof point — captaincy/balancing load, coursework, or TracKing; close with availability "Summer 2027"). No invented facts. Build with `node tools/coverletter.js cl.json daily/<date>/<id>/cover_letter.docx`.
- Render-check EVERY resume (soffice -> pdf; `pdfinfo` must say Pages: 1). Keep the summary <= 50 words and skills to <= 7 lines; the base resume has ~1 line of slack. If it spills, cut words — never shrink fonts or margins.
- Always include `"replace": {"Run front-of-house service (expediting, to-go orders, bussing, and direct customer interaction).": "Handle front-of-house service, including expediting, to-go orders, bussing, and direct customer interaction."}` (action-verb fix; true).
- ATS honesty: if the checker wants keywords Brandon lacks (e.g., PCI-DSS, HIPAA, Excel, AWS), do NOT add them — list them as "missing" in notes.md. Mention the company and program name in the summary (it counts as a keyword match).
- Cover letters: header uses Irvine, CA (matches resume) — say "local to Irvine/Orange County", not "Costa Mesa".

## Applied tracking
- data/applications-submitted.md mirrors "Job Search/Applications Submitted.md" on the Mac (Brandon's list of applications he has sent). data/seen.json status "applied" marks them.
- Roles with status "deferred" (Brandon chose to wait): list them in the next report under "Saved for later" with deadline; don't re-tailor.
- In the report, never re-suggest applied roles; list applied roles whose follow-up date is within 3 days under "Follow-ups due".

## Mac folder layout (written in Part B of the daily task)
Restructured 2026-11-21 at Brandon's request: Applications is the head folder with exactly two subfolders.
Job Search/
  Applications Submitted.md
  Applications/
    Not Yet Applied/<Company> - <Short role>/   -> "<Company> - <Short role> - Resume.docx", "... - Cover Letter.docx", "Job Info.md"
    Applied/<Company> - <Short role>/           -> same files, moved here once Brandon applies
  Daily Reports/<YYYY-MM-DD>/report.md
  CareerNavigator/...
Rules for the Mac task (every run):
- New tailored roles (score >= TAILOR_THRESHOLD, status "tailored") go into Applications/Not Yet Applied/<folder>/.
- Any role with status "applied" in data/roles.json (or listed in Applications Submitted.md) is MOVED (not copied) from Not Yet Applied/ to Applied/<folder>/. Never leave a duplicate in Not Yet Applied.
- One-time migration (first run after 2026-11-21): create Not Yet Applied/ and Applied/, then move every existing Applications/<folder>/ into the matching subfolder by status. Folders left directly under Applications/ are not allowed after that.
- Dropped roles (status "dropped" in data/roles.json): delete their folder wherever it is and never recreate it. Dropped 2026-11-21: "Millennium Space - Cybersecurity Analyst", "Varda - Cybersecurity Intern", "First American - InfoSec Analyst". ("Tevora - SOC Intern" was un-dropped and tailored 2026-11-24 at Brandon's request; recreate its folder in Not Yet Applied.) Dropped 2026-11-23: "PayPal - Cybersecurity Intern Summer 2027", "Verkada - Security Software Engineering Intern". Also dropped 2026-11-23: "Beazley Security - Incident Response Consultant", "Abacus - Cybersecurity Analyst", "University of La Verne - Cybersecurity GRC Analyst", "FTI Consulting - Cybersecurity Consultant".
- Cloud runs cannot reach the Mac; they only set status in data/roles.json and data/seen.json (and the "Folder" column in data/applications-submitted.md uses Applications/Applied/<folder>).
Use a short, readable folder name (e.g., "Tevora - Solutions Intern", "Ventura Foods - Associate AppSec Engineer"); store it as "folder" on the role in data/roles.json so both runs agree.

## Report (daily/<date>/report.md) and delivery
- New roles ranked by score: title (linked), company, location/mode, pay, deadline, score + one-line why, files link for every role >= TAILOR_THRESHOLD.
- Below 7: one line each. Count of roles skipped as already seen.
- Deadlines in the next 7 days for any role >= TAILOR_THRESHOLD not yet marked applied.
- Push notification: "N new roles, M scored 6+: <top 2 titles>". Commit and push everything.
- Update data/seen.json and data/roles.json.
- Delivery (Brandon's request 2026-11-21): no combined packets file. Send each tailored role's resume.docx + cover_letter.docx together in its own SendUserFile call, ranked by score, with the caption "<n>. <Company> — <Title>, score N: <posting URL>". Copy them to distinct names first (<role-id>-resume.docx, <role-id>-cover_letter.docx). Send report.md separately.
