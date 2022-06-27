# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        payment = super(AccountPayment, self).action_post()
        if self.payment_type == 'inbound' and self.partner_id.agent_id:
            product_id = self.env.ref(
                'sync_clients_data_master.agent_commission_product')
            invoice_vals = {
                'partner_id': self.partner_id.agent_id.id,
                'partner_company_id': self.partner_id.id,
                'invoice_date': fields.Date.today(),
                'move_type': 'in_invoice',
                'invoice_line_ids': [(0, 0, {
                    'product_id': product_id.id,
                    'quantity': 1,
                    'price_unit':
                        self.amount * self.partner_id.agent_commission / 100.00,
                })]
            }
            self.env['account.move'].create(invoice_vals).action_post()
        return payment
