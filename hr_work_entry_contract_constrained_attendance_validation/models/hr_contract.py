# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class HrContract(models.Model):
    _inherit = "hr.contract"

    def _get_attendance_intervals(self, start_dt, end_dt):
        # this context key tells modules on which this one depends to not
        # compute this, as it would yield incorrect results (validated
        # attendance intervals would be invisible to the contract-constrained
        # work entry generation code, which would consider the employee as
        # absent during these intervals) and we need to do it afterwards.
        intervals = super(
            HrContract, self.with_context(hr_work_entry_subtract_validated=False)
        )._get_attendance_intervals(start_dt, end_dt)
        intervals = self.env["hr.work.entry"].subtract_validated_work_entries(
            start_dt, end_dt, intervals
        )
        return intervals
