from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Partner"

    def _compute_agent_bills_count(self):
        for rec in self:
            rec.agent_bills_count = rec.env['account.move'].search_count([
                ('partner_id', '=', self.id),
                ('move_type', 'in', ('in_invoice', 'in_refund'))
            ])

    remote_servers_ids = fields.One2many(
        'remote.server', 'partner_id', "Remote Server")
    agent_id = fields.Many2one('res.partner', string='Agent')
    agent_commission = fields.Float(string='Commission')
    is_agent = fields.Boolean(string='Is Agent')
    pan_number = fields.Char(string='Pan Number')
    agent_bills_count = fields.Integer(
        compute='_compute_agent_bills_count', string='Agent Bills')
