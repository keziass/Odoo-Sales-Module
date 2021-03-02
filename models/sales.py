# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class sales(models.Model):
    _name = 'swalayan_sales.sales'

    sales_id = fields.Char("Code", default="New", required=True, readonly=True)
    tanggal = fields.Date("Order Date", default=datetime.date.today())
    total = fields.Monetary("Total Amount", compute='get_total', default=0, readonly="True", store=True)
    detail_order_ids = fields.One2many("swalayan_sales.detail_order", "sales_id",
                                        string="Detail Order")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    discount_id = fields.Many2one('swalayan_sales.discount', "Discount", compute="cek_discount", store=True)
    discount = fields.Char("Discount", default="0", compute="cek_discount", store=True)
    customer_id = fields.Many2one("res.partner", "Customer ID")
    # employee_id = fields.Many2one("hr.employees", string="Yang bertugas") // ini kalau mau nyambung ke modul lain (depends pada manifest)
    # employee_id = fields.Many2one('res.users', string='Yang bertugas', index=True,
    #                               track_visibility='onchange', default=lambda self: self.env.user, readonly=True)


    @api.model  # UNTUK CRUD -> bawaan odoo
    def create(self, vals_list):
        vals_list.update({
            'sales_id': self.env["ir.sequence"].with_context().next_by_code('swalayan_sales.sales')
        })
        return super(sales, self).create(vals_list)

    @api.multi
    @api.onchange("detail_order_ids")
    @api.depends("detail_order_ids")
    def get_total(self):
        for rec in self:
            jumlah = 0
            for x in rec.detail_order_ids:
                jumlah = jumlah + x.subtotal
            rec.total = jumlah


    @api.multi
    @api.onchange("total")
    def cek_discount(self):
        for rec in self:
            print("Masuk", rec.tanggal, rec.total)
            disc = rec.env["swalayan_sales.discount"].sudo().search(
                    [("start_date", "<=", rec.tanggal), ("end_date", ">=", rec.tanggal), ("min_amount", "<=", rec.total)])
            if disc:
                temp = disc[0]
                for i in disc:
                    print("iterasi")
                    if i.max_amount >= rec.total:
                        print("amount")
                        if i.jumlah >= temp.jumlah:
                            temp = i
                            print(i.jumlah)
                persen = temp.jumlah*100
                totaldisc = rec.total*temp.jumlah
                rec.total = rec.total - totaldisc
                rec.discount_id = temp
                rec.discount ="Rp " + str(totaldisc) + " (" + str(persen) + "%)"
    # self.alertbooktelat()
    #
    # @api.multi
    # def print_transaksi_buku(self):
    #     return self.env.ref('books.action_report_transaksi_buku') \
    #         .with_context({'discard_logo_check': True}).report_action(self)


class detail_order(models.Model):
    _name = 'swalayan_sales.detail_order'

    name = fields.Char("Code", default="Detail Code", required=True, readonly=True)
    tanggal = fields.Date("Tanggal", compute="get_tanggal", store=True)
    product_id = fields.Many2one("sw_wh.product", string="Product", required=True)
    qty = fields.Float("Jumlah", default=0, required=True)
    price = fields.Monetary("Harga Satuan", required=True, default=0, readonly=True,
                            compute="hitung_subtotal", store=True)
    subtotal = fields.Monetary("SubTotal", required=True, default=0, compute="hitung_subtotal")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    sales_id = fields.Many2one("swalayan_sales.sales", string="sales Order")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'name': self.env["ir.sequence"].with_context().next_by_code('swalayan_sales.detail_order')
        })
        update_new = self.env['sw_wh.product'].sudo().search([('id', '=', vals_list['product_id'])])
        update_new.write({'qty_out': vals_list['qty']})
        return super(detail_order, self).create(vals_list)

    @api.multi
    @api.onchange('qty')
    @api.depends("sales_id")
    def get_tanggal(self):
        for rec in self:
          rec.tanggal = rec.sales_id.tanggal

    @api.multi
    @api.depends("qty","product_id")
    def hitung_subtotal(self):
        for rec in self:
            if rec.product_id:
                rec.price = rec.product_id.price_sales
                subtotal = rec.product_id.price_sales*rec.qty
                rec.subtotal = subtotal

    @api.multi
    def write(self, vals_list):
        self.ensure_one()
        if 'qty' in vals_list:
            new_qty = vals_list['qty']
            old_qty = self.qty
            if 'product_id' in vals_list:
                update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                update_new.write({'qty_out': new_qty})
                self.product_id.write({'qty_in': old_qty})
            else:
                self.product_id.write({'qty_in': old_qty,
                                       'qty_out': new_qty})
        else:
            if 'product_id' in vals_list:
                qty = self.qty
                pid = vals_list['product_id']
                update_new = self.env['sw_wh.product'].sudo().search([('id', '=', pid)])
                update_new.write({'qty_out': qty})
                self.product_id.write({'qty_in': qty})
        res = super(detail_order, self).write(vals_list)
        return res
