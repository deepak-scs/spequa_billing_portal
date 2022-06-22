from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Partner"

    remote_servers_ids = fields.One2many(
        'remote.server', 'partner_id', "Remote Server")
    agent_id = fields.Many2one('res.partner', string='Agent')
    agent_commission = fields.Float(string='Commission')
    is_agent = fields.Boolean(string='Is Agent')
