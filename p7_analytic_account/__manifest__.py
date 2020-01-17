# -*- coding: utf-8 -*-
{
    'name': "p7_analytic_account",

    'summary': """
        Making analytic account as mandatory""",

    'description': """
        Whenever the user selecting the P&L Account in vendor bill and customer invoice analytic account should become mandatory otherwise it will be non mandatory
    """,

    'author': "Pinnacle Seven Technologies",
    'website': "https://pinnacleseven.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}