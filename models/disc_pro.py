# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class disc_pro(models.Model):
    _name = 'swalayan_sales.disc_pro'
    _rec_name = 'name'

    discount_id = fields.Char(string="Code", default="New", readonly=True)
    name = fields.Char("Nama Discount")
    jumlah = fields.Float("Jumlah Discount")
    start_date = fields.Date("Tanggal Mulai", default=datetime.date.today())
    end_date = fields.Date("Tanggal Selesai", default=datetime.date.today())
    is_active = fields.Boolean(default="True", compute="setActive")
    detail_ids = fields.One2many("sw_wh.product", "product_id", string="Product")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'discount_id': self.env["ir.sequence"].with_context().next_by_code('swalayan_sales.disc_pro')
        })
        return super(disc_pro, self).create(vals_list)

    @api.multi
    @api.onchange('start_date','end_date')
    def setActive(self):
        date = datetime.date.today()
        if date >= self.start_date and date <= self.end_date:
            self.is_active = True
        else:
            self.is_active = False
