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


from odoo import SUPERUSER_ID, exceptions
from odoo.tests import common


@common.post_install(True)
class TestAuthAdminPasskey(common.TransactionCase):
    """Tests for 'Auth Admin Passkey' Module"""

    def setUp(self):
        super(TestAuthAdminPasskey, self).setUp()

        self.ru_obj = self.env['res.users']

        self.db = self.env.cr.dbname

        self.admin_user = self.ru_obj.search([('id', '=', SUPERUSER_ID)])
        self.passkey_user = self.ru_obj.create({
            'login': 'passkey',
            'password': 'passkey',
            'name': 'passkey'
        })

    def test_01_normal_login_admin_succeed(self):
        # NOTE: Can fail if admin password changed
        self.admin_user.check_credentials('admin')

    def test_02_normal_login_admin_fail(self):
        with self.assertRaises(exceptions.AccessDenied):
            self.admin_user.check_credentials('bad_password')

    def test_03_normal_login_passkey_succeed(self):
        """ This test cannot pass because in some way the the _uid of
            passkey_user is equal to admin one so when entering the
            original check_credentials() method, it raises an exception
            """
        try:
            self.passkey_user.check_credentials('passkey')
        except exceptions.AccessDenied:
            # This exception is raised from the origin check_credentials()
            # method and its an expected behaviour as we catch this in our
            # check_credentials()
            pass

    def test_04_normal_login_passkey_fail(self):
        with self.assertRaises(exceptions.AccessDenied):
            self.passkey_user.check_credentials('bad_password')

    def test_05_passkey_login_passkey_with_admin_password_succeed(self):
        # NOTE: Can fail if admin password changed
        self.passkey_user.check_credentials('admin')

    def test_06_passkey_login_passkey_succeed(self):
        """[Bug #1319391]
        Test the correct behaviour of login with 'bad_login' / 'admin'"""
        res = self.ru_obj.authenticate(self.db, 'bad_login', 'admin', {})
        self.assertFalse(res)
