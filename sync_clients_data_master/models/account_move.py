# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_company_id = fields.Many2one(
        'res.partner', string='Partner Company')
