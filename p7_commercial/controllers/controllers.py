# -*- coding: utf-8 -*-
from odoo import http

# class P7Commercial(http.Controller):
#     @http.route('/p7_commercial/p7_commercial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/p7_commercial/p7_commercial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('p7_commercial.listing', {
#             'root': '/p7_commercial/p7_commercial',
#             'objects': http.request.env['p7_commercial.p7_commercial'].search([]),
#         })

#     @http.route('/p7_commercial/p7_commercial/objects/<model("p7_commercial.p7_commercial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('p7_commercial.object', {
#             'object': obj
#         })