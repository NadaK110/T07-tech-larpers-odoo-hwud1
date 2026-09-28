{
    'name': 'Gig Marketplace',
    'version': '1.0',
    'summary': 'Student freelance gig marketplace',
    'description': 'Post and apply to student gigs',
    'author': 'Team 07',
    'category': 'Services',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gig_posting_views.xml',
        'views/gig_application_views.xml',
        'data/gig_demo_data.xml',
    ],
    'installable': True,
    'application': True,
}