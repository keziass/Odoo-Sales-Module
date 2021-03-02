# -*- coding: utf-8 -*-
from odoo import http

# class SwalayanSales(http.Controller):
#     @http.route('/swalayan_sales/swalayan_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/swalayan_sales/swalayan_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('swalayan_sales.listing', {
#             'root': '/swalayan_sales/swalayan_sales',
#             'objects': http.request.env['swalayan_sales.swalayan_sales'].search([]),
#         })

#     @http.route('/swalayan_sales/swalayan_sales/objects/<model("swalayan_sales.swalayan_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('swalayan_sales.object', {
#             'object': obj
#         })