import xmlrpc
import xmlrpc.client
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from itertools import groupby
import logging
from odoo import api, fields, models, _

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib

_logger = logging.getLogger(__name__)


class RemoteServer(models.Model):
    _name = "remote.server"
    _description = "Remote Server"

    name = fields.Char("Name", required=1)
    url = fields.Char("Server Url", required=1)
    user = fields.Char("User", required=1)
    password = fields.Char("Password", required=1)
    dbname = fields.Char("Database", required=1)
    partner_id = fields.Many2one(
        'res.partner', "Customer", ondelete="cascade", copy=False)
    date_sync = fields.Datetime(
        string="Last Sync Date", default=datetime.now())

    def _fetch_client_log_data(self, server):
        log_datas = []
        if server:
            addr = server.url
            userid = server.user
            password = server.password
            dbname = server.dbname
        try:
            uid = xmlrpclib.ServerProxy("%s/xmlrpc/common" % (addr)).authenticate(
                dbname, userid, password, {}
            )
        except:
            _logger.warning("Could not authenticate user on the remote server")

        try:
            log_datas = xmlrpclib.ServerProxy(
                "%s/xmlrpc/object" % (addr)).execute(
                dbname,
                uid,
                password,
                'hr.employee',
                'search_read',
                [
                    ('state', '!=', 'terminated')
                ],
                [
                    'full_name',
                    'emp_code',
                    'partner_company_id'
                ]
            )
        except:
            _logger.warning("Could not retrieve data from client server")
        employee_data = []
        for logdata in log_datas:
            vals = {
                'partner_id': self.partner_id.id,
                'emp_name': logdata.get('full_name'),
                'res_model': 'hr.employee',
                'emp_code': logdata.get('emp_code'),
                'partner_company': logdata.get(
                    'partner_company_id')[1] if logdata.get(
                    'partner_company_id') else '',
                'date': fields.Date.today(),
            }
            employee_data.append(vals)
        self.env['client.data'].create(employee_data)
        server['date_sync'] = datetime.now()
        return True

    def button_sync_partner_data(self):
        for server in self:
            url = server.url
            userid = server.user
            password = server.password
            dbname = server.dbname
            try:
                uid = xmlrpclib.ServerProxy(
                    "%s/xmlrpc/common" % (url)).authenticate(
                    dbname, userid, password, {}
                )
                if not uid:
                    raise UserError(_('Connection Failed!'))
            except:
                raise UserError(_('Connection Failed!'))
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Synced successfully!"),
                    'message': _("Everything seems properly synced!"),
                    'sticky': False,
                }
            }

    @api.model
    def _client_log_data_fetch(self):
        server_datas = self.env['remote.server'].search([])
        for server in server_datas:
            server._fetch_client_log_data(server)
            self._cr.commit()

    @api.model
    def _generate_customer_bill(self):
        current_date = fields.Date.today()
        one_month_before_date = fields.Date.today() #current_date + relativedelta(months=-1)
        client_datas = self.env['client.data'].with_context(
            active_test=False).search([
                '|',
                ('date_end', '=', False),
                '&',
                ('date_end', '>=', one_month_before_date),
                ('date_end', '<=', current_date)
            ])
        product_id = self.env.ref(
            'sync_clients_data_master.employee_creation_invoice_product')
        for partner, lines in groupby(client_datas, lambda l: l.partner_id):
            invoice_vals = {
                'partner_id': partner.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'product_id': product_id.id,
                    'quantity': len(list(lines)),
                    'price_unit': product_id.lst_price,
                })]
            }
            self.env['account.move'].create(invoice_vals).action_post()
