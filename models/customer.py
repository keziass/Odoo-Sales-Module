from odoo import models, fields, api

class customer(models.Model):
    _inherit = 'res.partner'

    customer_id = fields.Char("Code", default="New Customer", readonly=True)
    sales_count = fields.Integer("Jumlah Beli", default=0, compute="compute_sales_count")
    level = fields.Selection(selection=[("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold")],
                             string="Level", default="bronze", readonly=True, compute="cek_level")
    sales_ids = fields.One2many("swalayan_sales.sales", "customer_id", string="Sales Order")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'customer_id': self.env["ir.sequence"].with_context().next_by_code('res.partner')
        })
        return super(customer, self).create(vals_list)

    @api.multi
    @api.onchange("sales_ids")
    def cek_level(self):
        for rec in self:
            jumlah = 0
            for rec2 in rec.sales_ids:
                jumlah = jumlah + 1
            if jumlah >= 5:
                rec.level = "gold"
            elif jumlah >= 3:
                rec.level = "silver"
            else:
                rec.level = "bronze"

    @api.multi
    def compute_sales_count(self):
        for rec in self:
            jumlah = 0
            for rec2 in rec.sales_ids:
                jumlah = jumlah + 1
            rec.sales_count=jumlah

