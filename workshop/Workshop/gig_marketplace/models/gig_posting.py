from odoo import models, fields
import requests


class GigPosting(models.Model):
    _name = 'gig.posting'
    _description = 'Student Gig Posting'
    application_ids = fields.One2many(
        'gig.application', 'gig_id', string='Applications')

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    poster_id = fields.Many2one('res.partner', string='Posted By')
    category = fields.Selection([
        ('graphic_design', 'Graphic Design'),
        ('programming', 'Programming'),
        ('tutoring', 'Tutoring'),
        ('writing', 'Writing'),
        ('photography', 'Photography'),
        ('video_editing', 'Video Editing'),
        ('marketing', 'Marketing'),
        ('event_support', 'Event Support'),
        ('translation', 'Translation'),
        ('design', 'Design'),
        ('music', 'Music'),
        ('research', 'Research'),
        ('other', 'Other'),], string='Category')
    budget = fields.Float(string='Budget')
    deadline = fields.Date(string='Deadline')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open')

    def action_suggest_category(self):
        valid_categories = {
            'graphic_design',
            'programming',
            'tutoring',
            'writing',
            'photography',
            'video_editing',
            'marketing',
            'event_support',
            'translation',
            'design',
            'music',
            'research',
            'other',
        }
        for gig in self:
            if not gig.description:
                gig.category = 'other'
                continue
            prompt = f"""
            You are categorising student gigs.
            
            Based ONLY on the gig description below, suggest the most appropriate category.

            Gig description:
            {gig.description}

            Choose ONE category from this list:

            graphic_design
            programming
            tutoring
            writing
            photography
            video_editing
            marketing
            event_support
            translation
            design
            music
            research
            other

            Return ONLY the category name.
            Do not provide an explanation.
            """
            response = requests.post('http://localhost:11434/api/generate',
                                     json={
                                         'model': 'llama3.2:3b',
                                         'prompt': prompt,
                                         'stream': False
                                     },
                                     timeout=120)
            response.raise_for_status()
            result = response.json()
            suggested_category = result.get('response', '').strip()

            if suggested_category in valid_categories:
                gig.category = suggested_category
            else:
                gig.category = 'other'
        return True

    def action_suggest_budget(self):

        for gig in self:
            if not gig.description:
                gig.budget = 0.0
                continue
            prompt = f"""
                You are a student gig marketplace assistant.
                Suggest from a student's perspective with a reasonable budget.
                Based ONLY on the gig description and the gig title below, suggest a reasonable budget for the gig in AED.
                
                Gig title: {gig.name}
                Gig description: {gig.description}
                
                Return ONLY the numeric amount.
                Do not include AED, DHS, currency symbols, words, or explanations.
                For example: 150
                """

            response = requests.post('http://localhost:11434/api/generate',
                                     json={
                                         'model': 'llama3.2:3b',
                                         'prompt': prompt,
                                         'stream': False
                                     },
                                     timeout=120)
            response.raise_for_status()
            result = response.json()
            suggested_budget = result.get('response', '').strip()

            try:
                gig.budget = float(suggested_budget)
            except ValueError:
                gig.budget = 0.0

        return True
