# -*- coding: utf-8 -*-
from odoo import http

# class P7EmeraldInvoice(http.Controller):
#     @http.route('/p7_emerald_invoice/p7_emerald_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/p7_emerald_invoice/p7_emerald_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('p7_emerald_invoice.listing', {
#             'root': '/p7_emerald_invoice/p7_emerald_invoice',
#             'objects': http.request.env['p7_emerald_invoice.p7_emerald_invoice'].search([]),
#         })

#     @http.route('/p7_emerald_invoice/p7_emerald_invoice/objects/<model("p7_emerald_invoice.p7_emerald_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('p7_emerald_invoice.object', {
#             'object': obj
#         })