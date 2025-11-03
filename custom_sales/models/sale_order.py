# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    """
    Extension dari model sale.order
    Modul ini digunakan sebagai kerangka dasar untuk setiap perubahan 
    dan penambahan pada model sales.order
    
    CONTOH CASE: Custom Fields dan Computed Fields
    ===============================================
    Contoh implementasi menambahkan:
    1. Field Tanggal PO Customer
    2. Field Persentase Diskon Custom
    3. Computed Field Total Setelah Diskon Custom
    4. Field Catatan Internal Khusus
    """
    _inherit = 'sale.order'

    # === CONTOH FIELD TAMBAHAN ===
    
    customer_po_date = fields.Date(
        string='Tanggal PO Customer',
        help='Tanggal Purchase Order dari customer',
        tracking=True,
        copy=False
    )
    
    custom_discount_percent = fields.Float(
        string='Diskon Custom (%)',
        default=0.0,
        digits='Discount',
        help='Persentase diskon tambahan yang akan diterapkan',
        tracking=True
    )
    
    custom_internal_note = fields.Text(
        string='Catatan Internal',
        help='Catatan khusus internal untuk sales order ini',
        groups='base.group_user'
    )
    
    # === CONTOH COMPUTED FIELD ===
    
    total_after_custom_discount = fields.Monetary(
        string='Total Setelah Diskon Custom',
        compute='_compute_total_after_custom_discount',
        store=True,
        currency_field='currency_id',
        help='Total amount setelah dikurangi diskon custom'
    )
    
    @api.depends('amount_total', 'custom_discount_percent')
    def _compute_total_after_custom_discount(self):
        """
        Menghitung total setelah dikurangi diskon custom
        Catatan: Widget percentage menyimpan nilai sebagai desimal (0.50 = 50%)
        Rumus: amount_total * (1 - custom_discount_percent)
        """
        for record in self:
            if record.custom_discount_percent > 0:
                # Widget percentage sudah menyimpan sebagai desimal, jadi langsung dikalikan
                discount_amount = record.amount_total * record.custom_discount_percent
                record.total_after_custom_discount = record.amount_total - discount_amount
            else:
                record.total_after_custom_discount = record.amount_total
    
    # === CONTOH METHOD CUSTOM ===
    
    def action_apply_custom_discount(self):
        """
        Method untuk menerapkan diskon custom ke semua order line
        Catatan: Widget percentage menyimpan nilai sebagai desimal (0.50 = 50%)
        """
        self.ensure_one()
        if self.custom_discount_percent > 0:
            # Widget percentage sudah menyimpan sebagai desimal, jadi langsung digunakan
            discount_factor = 1 - self.custom_discount_percent
            for line in self.order_line:
                line.price_unit = line.price_unit * discount_factor
            # Format persentase untuk display (kalikan 100)
            display_percent = self.custom_discount_percent * 100
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Diskon Custom Diterapkan',
                    'message': f'Diskon {display_percent:.0f}% telah diterapkan ke semua line item.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        return False

