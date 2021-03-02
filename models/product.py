# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class product(models.Model):
    _inherit = 'sw_wh.product'

    price_sales = fields.Monetary("Harga Jual", default=0, compute="set_price")

    @api.multi
    @api.onchange("price")
    def set_price(self):
        for rec in self:
            rec.price_sales = rec.price * 1.2

    @api.multi
    def write(self, vals):
        new_qty = self.qty
        if 'qty_in' in vals:
            new_qty = new_qty + vals['qty_in']
        if 'qty_sales' in vals:
            if vals['qty_sales'] > new_qty:
                raise UserError("Stock Tidak Cukup")
            else:
                new_qty = new_qty - vals['qty_sales']
        if 'qty_out' in vals:
            if vals['qty_out'] > new_qty:
                raise UserError("Stock Tidak Cukup")
            else:
                new_qty = new_qty - vals['qty_out']
        if new_qty < 0:
            new_qty = 0

        vals.update({'qty': new_qty})

        res = super(product, self).write(vals)

        return res
