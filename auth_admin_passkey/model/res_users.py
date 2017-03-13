# -*- encoding: utf-8 -*-
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

import datetime

from odoo import SUPERUSER_ID, _, api, exceptions, models
from odoo.tools.safe_eval import safe_eval


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def _send_email_passkey(self, user_id):
        """ Send a email to the admin of the system and / or the user
            to inform passkey use."""
        mail_obj = self.env['mail.mail'].sudo()
        icp_obj = self.env['ir.config_parameter']

        admin_user = self.browse(SUPERUSER_ID)
        login_user = self.browse(user_id)

        send_to_admin = safe_eval(
            icp_obj.get_param('auth_admin_passkey.send_to_admin')
        )
        send_to_user = safe_eval(
            icp_obj.get_param('auth_admin_passkey.send_to_user')
        )

        mails = []
        if send_to_admin and admin_user.email:
            mails.append({'email': admin_user.email, 'lang': admin_user.lang})
        if send_to_user and login_user.email:
            mails.append({'email': login_user.email, 'lang': login_user.lang})

        for mail in mails:
            subject = _('Passkey used')
            body = _(
                "Admin user used his passkey to login with '%s'.\n\n"
                "\n\nTechnicals informations belows : \n\n"
                "- Login date : %s\n\n"
            ) % (login_user.login,
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            mail_obj.create({
                'email_to': mail['email'],
                'subject': subject,
                'body_html': '<pre>%s</pre>' % body
            })

    @api.model
    def _send_email_same_password(self, login):
        """ Send an email to the admin user to inform that
            another user has the same password as him."""
        mail_obj = self.env['mail.mail'].sudo()
        admin_user = self.browse(SUPERUSER_ID)

        if admin_user.email:
            mail_obj.create({
                'email_to': admin_user.email,
                'subject': _('[WARNING] Odoo Security Risk'),
                'body_html':
                    _("<pre>User with login '%s' has the same "
                      "password as you.</pre>") % (login),
            })

    @api.model
    def check_credentials(self, password):
        """ Check that credentials are ok for the current user
            or if the password is the same as admin user"""
        try:
            super(Users, self).check_credentials(password)

            if self._uid != SUPERUSER_ID:
                try:
                    super(Users, self).sudo().check_credentials(password)
                    self._send_email_same_password(self.login)
                except exceptions.AccessDenied:
                    pass

        except exceptions.AccessDenied:
            if self._uid == SUPERUSER_ID:
                raise

            # Just be sure that parent methods aren't wrong
            user = self.sudo().search([('id', '=', self._uid)])
            if not user:
                raise

            try:
                super(Users, self).sudo().check_credentials(password)
                self._send_email_passkey(self._uid)
            except exceptions.AccessDenied:
                raise
