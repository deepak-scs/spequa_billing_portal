
from odoo import fields, models


class ClientData(models.Model):
    _name = "client.data"
    _description = "Manage Client Billing Data"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "emp_name"

    partner_id = fields.Many2one(
        'res.partner', 'Customer', ondelete="cascade", copy=False, index=True)
    emp_name = fields.Char('Employee')
    emp_code = fields.Char('Spequa ID')
    partner_company = fields.Char('Partner Company')
    res_model = fields.Char('Res Model')
    date = fields.Date('Date', tracking=True)
