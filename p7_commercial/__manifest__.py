# -*- coding: utf-8 -*-
{
    'name': "p7_commercial",

    'summary': """
        Managing commercial activity by P7""",

    'description': """
        This module allow us to maintain the commercial activity like managing the owner, home and contract.
    """,

    'author': "Pinnacle Seven Technologies",
    'website': "https://pinnacleseven.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing Management',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','analytic','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}