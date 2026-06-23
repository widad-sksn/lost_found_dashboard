{
    "name": 'Smart Lost & Found',
    "description":"""
        Campus Lost & Found ERP
        -Log found items with tracking IDs.
        -Students file lost claims.
        -Auto-match engine connects claims to found items based on category and date
            """,
    "depends":["base", "mail", "portal", "website", "auth_signup"],
    "version": '1.0.17',
    "application": True,
    "data":[
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'data/mail_templates.xml',
        'views/menu_views.xml',
        'views/found_item_views.xml',
        'views/lost_claim_views.xml',
        'views/item_claim_request_views.xml',
        'views/portal_templates.xml',
        'views/login_templates.xml',
        'data/student_users.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'lost_found_dashboard/static/src/scss/portal_theme.scss',
            'lost_found_dashboard/static/src/scss/login.scss',
        ],
        'web.assets_backend': [
            'lost_found_dashboard/static/src/scss/backend_theme.scss',
            'lost_found_dashboard/static/src/scss/item_matching_dashboard.scss',
            'lost_found_dashboard/static/src/js/item_matching_dashboard.js',
            'lost_found_dashboard/static/src/xml/item_matching_dashboard.xml',
        ],
    }
}
