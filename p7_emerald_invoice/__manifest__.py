# -*- coding: utf-8 -*-
{
    'name': "p7_emerald_invoice",

    'summary': """
        Emerald Invoice Format by P7""",

    'description': """
        This module has unique supplier invoice format done by Pinnacle Seven Technologies
    """,

    'author': "Pinnacle Seven Technologies",
    'website': "https://pinnacleseven.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing Management',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}