# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class discount(models.Model):
    _name = 'swalayan_sales.discount'

    discount_id = fields.Char(string="Code", default="New", readonly=True)
    name = fields.Char("Nama Discount")
    jumlah = fields.Float("Jumlah Discount")
    min_amount = fields.Monetary("Minimum Amount", default=0)
    max_amount = fields.Monetary("Maximum Amount", default=0)
    start_date = fields.Date("Tanggal Mulai", default=datetime.date.today())
    end_date = fields.Date("Tanggal Selesai", default=datetime.date.today())
    is_active = fields.Boolean(default="True", compute="setActive")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    @api.model
    def create(self, vals_list):
        vals_list.update({
            'discount_id': self.env["ir.sequence"].with_context().next_by_code('swalayan_sales.discount')
        })
        return super(discount, self).create(vals_list)

    @api.multi
    @api.onchange('start_date','end_date')
    def setActive(self):
        date = datetime.date.today()
        if date >= self.start_date and date <= self.end_date:
            self.is_active = True
        else:
            self.is_active = False


