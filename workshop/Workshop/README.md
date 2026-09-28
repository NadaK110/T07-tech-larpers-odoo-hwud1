# BuildOdoo 2026 — Student Freelance/Gig Marketplace

**Track:** Track 3 — Open Innovation
**Event:** Odoo × HW Tech Club BuildOdoo 2026 Hackathon
**Repo:** https://github.com/NadaK110/T07-tech-larpers-odoo-hwud

## What we're building

A platform where students post small gigs (tutoring, design work, errands, etc.) and
other students apply to them. AI helps organize and improve the marketplace in three
ways: auto-categorizing gigs, suggesting fair budgets, and scoring how well an applicant
matches a gig.

## ⚡ Current Status (updated)

| Task | Owner(s) | Status |
|---|---|---|
| Backend: `gig.posting` model + module setup | Nada | ✅ Done |
| Backend: `gig.application` model + Applications tab (incl. access control — applicants can't self-approve; only poster can accept/reject) | Nada | ✅ Done |
| Frontend/Views (list, kanban, search, form polish) | Zuha | ✅ Done |
| AI: category + budget suggestion | Irina | ✅ Done |
| AI: applicant-to-gig match scoring | Shayaan | ✅ Done |
| Presentation / demo prep | Irina | ✅ Done |
| Sample/demo data + end-to-end testing | **OPEN — needs an owner** | ✅ Done |

## Getting started (for teammates joining now)

1. Make sure Odoo is running locally on your own machine (setup guide from before the
   hackathon). This repo only holds our custom module code, not the Odoo core itself.

2. Clone this repo:
   ```bash
   git clone https://github.com/NadaK110/T07-tech-larpers-odoo-hwud.git
   ```

3. Pull the latest before you start working, every time:
   ```bash
   git pull --no-rebase
   ```

4. Our module lives in `gig_marketplace/` (alongside the `estate` and `estate_accounts`
   reference modules from the intro workshop — those are just examples, not our project).

5. **Don't commit straight to `main` without pulling first.** Always
   `git pull --no-rebase` before you start editing, and again before you push.

6. ⚠️ **Important — data does NOT sync via git, only code does.** Each of you runs Odoo
   on your own laptop with your own local database. Gigs/applications you create only
   exist on your own machine. For the actual demo, we need ONE laptop with all the code
   pulled in and good sample data created on it — see "Sample/demo data" below.

## What's already working

- Create a gig (title, description, category, budget, deadline, status)
- Gigs show in a Kanban board grouped by status, plus a list view with filters
- Opening a gig shows a status bar (Open → In Progress → Completed) and a polished form
- **AI auto-fills the category** from the gig's description when it's created
- **AI suggests a fair budget** based on the description
- Applicants can apply via the Applications tab (applicant, message, status)
- **AI scores how well an applicant matches a gig**, to help the poster spot good fits
- Accept/Reject buttons on applications:
  - An applicant **cannot** accept/reject their own application (blocked with an error)
  - Only the gig's poster can accept/reject applications to their own gig
  - Accepting an application automatically moves the gig to "In Progress"

## What's left before submission

**Sample/demo data + testing — OPEN ROLE**
Whoever picks this up should, on whichever laptop will be used for the actual demo:
- Pull the latest code from everyone (`git pull --no-rebase`, restart server, Apps →
  Upgrade)
- Create 8-10+ realistic gigs across different categories, so the AI category/budget
  features have real variety to show off
- Create several applications per gig (using a second test user, not just admin) so the
  match-scoring and accept/reject flow can be demoed properly
- Test the full journey end-to-end: post a gig → AI fills category/budget → apply as a
  different user → check match score → accept as the poster → gig moves to In Progress
- Flag any bugs found to whoever owns that part

**Presentation (Irina, in progress)**
- Demo script (aim for 2-3 minutes)
- Slides: problem, solution, how it works, tech stack, impact
- Note: presenting itself is a team effort — everyone should be ready to speak to the
  part they built

## Data model (for reference)

**`gig.posting`**
- `name`, `description`, `poster_id` (→ res.partner), `category` (AI), `budget` (AI),
  `deadline`
- `state`: Open / In Progress / Completed / Cancelled
- `application_ids` (One2many → gig.application)

**`gig.application`**
- `gig_id` (→ gig.posting), `applicant_id` (→ res.partner), `message`
- `status`: Pending / Accepted / Rejected
- `match_score` (AI) — how well the applicant fits the gig

## Timeline reminders

- **Submission deadline:** Monday 28th September, 12 PM
- **Presentation:** Wednesday 30th September, 2–4 PM

## Questions or blockers?

Ping the group chat — don't spend more than ~20–30 minutes stuck alone on a setup issue,
just ask.