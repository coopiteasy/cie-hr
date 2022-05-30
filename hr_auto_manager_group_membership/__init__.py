# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models

import odoo


def update_all_manager_group_memberships(cr, registry):
    with odoo.api.Environment.manage():
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        for employee in env["hr.employee"].search([]):
            employee._update_manager_group_membership()
