# -*- coding: utf-8 -*-
##############################################################################
#
#    Admin Passkey module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
from odoo.tools import safe_eval


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    @api.model
    def get_default_auth_admin_passkey_send_to_admin(self, _):
        icp = self.env['ir.config_parameter']
        return {
            'auth_admin_passkey_send_to_admin': safe_eval(icp.get_param(
                'auth_admin_passkey.send_to_admin', 'True')),
        }

    @api.model
    def get_default_auth_admin_passkey_send_to_user(self, _):
        icp = self.env['ir.config_parameter']
        return {
            'auth_admin_passkey_send_to_user': safe_eval(icp.get_param(
                'auth_admin_passkey.send_to_user', 'True')),
        }

    auth_admin_passkey_send_to_admin = fields.Boolean(
        'Send email to admin user.',
        help=('When the administrator use his password to login in '
              'with a different account, OpenERP will send an email '
              'to the admin user.'),
    )
    auth_admin_passkey_send_to_user = fields.Boolean(
        string='Send email to user.',
        help=('When the administrator use his password to login in '
              'with a different account, OpenERP will send an email '
              'to the account user.'),
    )

    @api.multi
    def set_auth_admin_passkey_send_to_admin(self):
        self.ensure_one()

        icp = self.env['ir.config_parameter']
        icp.set_param(
            'auth_admin_passkey.send_to_admin',
            repr(self.auth_admin_passkey_send_to_admin))

    @api.multi
    def set_auth_admin_passkey_send_to_user(self):
        self.ensure_one()

        icp = self.env['ir.config_parameter']
        icp.set_param(
            'auth_admin_passkey.send_to_user',
            repr(self.auth_admin_passkey_send_to_user))
