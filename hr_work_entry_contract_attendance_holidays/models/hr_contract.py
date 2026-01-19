# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    work_entry_source = fields.Selection(
        selection_add=[("contract_attendance", "Attendances According To Contract")],
        ondelete={"contract_attendance": "set default"},
        default="contract_attendance",
    )

    def generate_work_entries(self, date_start, date_stop, force=False):
        new_work_entries = super(
            HrContract,
            self.filtered(lambda c: c.work_entry_source != "contract_attendance"),
        ).generate_work_entries(date_start, date_stop, force)
        return new_work_entries
