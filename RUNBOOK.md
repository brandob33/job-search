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
inbox/linkedin-YYYY-MM-DD.json   roles found by the 8:10 Mac run (LinkedIn, signed in)
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
3. `inbox/linkedin-*.json` written by the Mac run that morning (and any unprocessed earlier ones).
Exclude: 3+ yrs required, active clearance already required, non-security helpdesk, gig "AI trainer" postings, roles already in data/seen.json (unless the posting materially changed or reopened).
Verify each new role is open by fetching the posting. Save posting text to the role folder notes.

## Scoring (1-10)
Weights: Required quals met 40% | Keyword/skill match 25% | Eligibility (location, enrollment/grad window, citizenship) 20% | Seniority fit 15%.
- Hard eligibility fail (e.g., requires active TS clearance, must graduate between dates he can't meet and posting is strict, >1hr onsite) -> cap at 4 and say why.
- Grad-window mismatch where posting says "currently enrolled" -> he qualifies (certificate program). Where it says "pursuing a bachelor's" -> flag, -1.
- AppSec/product security/IAM roles usually fit better than pure SOC roles; score honestly.
Record in notes.md: score, 2-line why, matched keywords, missing keywords, eligibility flags.

## Tailoring threshold
TAILOR_THRESHOLD = 6  (7 -> 5 on 2026-11-21, then 5 -> 6 on 2026-11-21 at Brandon's request: 5 produced too many roles; tailor every role scoring >= 6)
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
- In the report, never re-suggest applied roles; list applied roles whose follow-up date is within 3 days under "Follow-ups due".

## Mac folder layout (written by the 9:12 Mac task)
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
- Dropped roles (status "dropped" in data/roles.json): delete their folder wherever it is and never recreate it. Dropped 2026-11-21: "Tevora - SOC Intern", "Millennium Space - Cybersecurity Analyst", "Varda - Cybersecurity Intern", "First American - InfoSec Analyst".
- Cloud runs cannot reach the Mac; they only set status in data/roles.json and data/seen.json (and the "Folder" column in data/applications-submitted.md uses Applications/Applied/<folder>).
Use a short, readable folder name (e.g., "Tevora - Solutions Intern", "Ventura Foods - Associate AppSec Engineer"); store it as "folder" on the role in data/roles.json so both runs agree.

## Report (daily/<date>/report.md) and delivery
- New roles ranked by score: title (linked), company, location/mode, pay, deadline, score + one-line why, files link for every role >= TAILOR_THRESHOLD.
- Below 7: one line each. Count of roles skipped as already seen.
- Deadlines in the next 7 days for any role >= TAILOR_THRESHOLD not yet marked applied.
- Push notification: "N new roles, M scored 6+: <top 2 titles>". Commit and push everything.
- Update data/seen.json and data/roles.json.
- Delivery (Brandon's request 2026-11-21): no combined packets file. Send each tailored role's resume.docx + cover_letter.docx together in its own SendUserFile call, ranked by score, with the caption "<n>. <Company> — <Title>, score N: <posting URL>". Copy them to distinct names first (<role-id>-resume.docx, <role-id>-cover_letter.docx). Send report.md separately.
