# -*- coding: utf-8 -*-
from odoo import http

# class P7AnalyticAccount(http.Controller):
#     @http.route('/p7_analytic_account/p7_analytic_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/p7_analytic_account/p7_analytic_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('p7_analytic_account.listing', {
#             'root': '/p7_analytic_account/p7_analytic_account',
#             'objects': http.request.env['p7_analytic_account.p7_analytic_account'].search([]),
#         })

#     @http.route('/p7_analytic_account/p7_analytic_account/objects/<model("p7_analytic_account.p7_analytic_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('p7_analytic_account.object', {
#             'object': obj
#         })