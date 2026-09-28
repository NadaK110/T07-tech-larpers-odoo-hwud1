from odoo import api, models, fields
from odoo.exceptions import UserError
import json
import requests

OLLAMA_URL = 'http://localhost:11434/api/generate'


class GigApplication(models.Model):
    _name = 'gig.application'
    _description = 'Gig Application'
    _order = 'match_score desc, id desc'   # best-fit applicants shown first

    gig_id = fields.Many2one('gig.posting', string='Gig', required=True)
    applicant_id = fields.Many2one('res.partner', string='Applicant', required=True)
    message = fields.Text(string='Message')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending')

    # AI match scoring
    match_score = fields.Integer(string='Match Score')
    match_reason = fields.Char(string='AI Reasoning')

    # accept button - marks this application as accepted and
    # moves the gig to "In Progress" since someone is now working on it
    def action_accept(self):
        for application in self:
            if application.applicant_id == self.env.user.partner_id:
                raise UserError("You can't accept your own application.")
            if application.gig_id.poster_id != self.env.user.partner_id:
                raise UserError("Only the gig poster can accept applications.")
            application.status = 'accepted'
            application.gig_id.state = 'in_progress'

    # reject button - just marks this application as rejected
    def action_reject(self):
        for application in self:
            if application.applicant_id == self.env.user.partner_id:
                raise UserError("You can't reject your own application.")
            if application.gig_id.poster_id != self.env.user.partner_id:
                raise UserError("Only the gig poster can reject applications.")
            application.status = 'rejected'

    # score automatically when a new application is created
    @api.model_create_multi
    def create(self, vals_list):
        applications = super().create(vals_list)
        for application in applications:
            try:
                application._run_ai_match()
            except requests.exceptions.RequestException:
                pass  # never block an application if the AI is offline
        return applications

    # "AI Match Score" button - re-scores on demand
    def action_ai_match_score(self):
        for application in self:
            try:
                application._run_ai_match()
            except requests.exceptions.RequestException:
                raise UserError("Couldn't reach the AI. Make sure Ollama is running.")
        return True

    def _run_ai_match(self):
        self.ensure_one()
        gig = self.gig_id
        if not self.message:
            self.match_score = 0
            self.match_reason = "No message provided by the applicant."
            return

        prompt = f"""
        You are helping a student decide which applicant fits their gig best.

        GIG TITLE: {gig.name}
        GIG CATEGORY: {gig.category or 'not set'}
        GIG DESCRIPTION: {gig.description or 'none'}

        APPLICANT MESSAGE: {self.message}

        Score how well the applicant fits the gig from 0 to 100:
        - 80-100: message shows skills or experience directly relevant to the gig
        - 50-79: some relevant skills, but not a strong match
        - 20-49: weak or vague connection
        - 0-19: unrelated, or no real effort in the message

        Reply ONLY with JSON in this exact format:
        {{"score": <number>, "reason": "<one short sentence>"}}
        """
        response = requests.post(OLLAMA_URL, json={
            'model': 'llama3.2:3b',
            'prompt': prompt,
            'stream': False,
            'format': 'json',   # forces the AI to answer in JSON
        }, timeout=120)
        response.raise_for_status()

        try:
            data = json.loads(response.json().get('response', '{}'))
            score = int(data.get('score', 0))
            self.match_score = max(0, min(100, score))   # keep it between 0 and 100
            self.match_reason = str(data.get('reason', ''))[:250]
        except (ValueError, TypeError):
            self.match_score = 0
            self.match_reason = "AI returned an unreadable answer - try again."