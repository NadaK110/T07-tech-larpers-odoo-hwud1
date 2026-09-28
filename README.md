# BuildOdoo 2026 — Student Freelance/Gig Marketplace (Team T07)

**Track:** Track 3 — Open Innovation
**Event:** Odoo × HW Tech Club BuildOdoo 2026 Hackathon

This repository contains the full Odoo 19.0 source plus our custom module.

## 👉 Where our project actually lives

Everything we built is in one folder:

```
workshop/Workshop/gig_marketplace/
├── __manifest__.py
├── models/
│   ├── gig_posting.py        # gig model + AI category and budget suggestion
│   └── gig_application.py    # application model + AI match scoring + access control
├── views/
│   ├── gig_posting_views.xml       # kanban, list, form, search
│   └── gig_application_views.xml
├── security/ir.model.access.csv
└── data/gig_demo_data.xml    # sample gigs and applications for testing
```

The rest of the repo (`odoo/`, `addons/`, `odoo-bin`, etc.) is standard Odoo 19.0 core, included so the project can run as-is. The team's original code repo is at https://github.com/NadaK110/T07-tech-larpers-odoo-hwud (the `workshop/Workshop` folder).

## What it does

Students post small gigs (tutoring, design, errands). Other students apply. AI helps in three places:

1. **Category suggestion** from the gig description
2. **Budget suggestion** based on the description
3. **Applicant match scoring** (0-100, with a short reason) so posters can spot the best fit

Access control is enforced in the model logic: applicants cannot accept or reject their own application, and only the gig's poster can accept or reject. Accepting an application moves the gig to "In Progress."

## How to run it (for judges / testers)

**Requirements:** macOS or Linux, Python 3.11, PostgreSQL 15, and [Ollama](https://ollama.com) for the AI features.

1. **Install dependencies**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install wheel
   pip install psycopg2-binary
   pip install -r requirements.txt
   ```
   (`psycopg2-binary` avoids needing `pg_config` on macOS. The `venv/` folder is not included in the repo.)

2. **Start PostgreSQL** and create a superuser for your OS user:
   ```bash
   createuser -s $(whoami)
   ```

3. **Set up the AI model (local, no API key needed)**
   ```bash
   ollama pull llama3.2:3b
   ollama serve
   ```
   If Ollama isn't running, the app still works. AI fields just stay empty.

4. **Check `odoo.conf`**: `db_user` should match your OS username, and `addons_path` should include `workshop/Workshop`.

5. **Run Odoo and install our module**
   ```bash
   python odoo-bin --config=odoo.conf -d admin -i gig_marketplace
   ```

6. Open **http://localhost:8069** and go to **Gig Marketplace → Gigs**.

## Testing the access control

Create a second user (Settings → Users), log in as that user, and try to accept your own application. You'll get a blocked-action error. Log in as the gig's poster and accept it, and the gig moves to "In Progress."

## Team

| Area | Owner |
|---|---|
| Backend models (`gig.posting`, `gig.application`) + access control | Nada |
| Frontend / views | Zuha |
| AI: category + budget | Irina |
| AI: applicant match scoring | Shayaan |
| Presentation | Irina + team |

## Data note

Records created while testing live in each person's local database and are not part of this repo. `data/gig_demo_data.xml` loads sample gigs and applications on install.
