# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class HrContract(models.Model):
    _inherit = "hr.contract"

    def _get_attendance_intervals(self, start_dt, end_dt):
        intervals = super()._get_attendance_intervals(start_dt, end_dt)
        # this context key allows dependent modules to compute this themselves
        # if needed (because they need the validated intervals to be still
        # present during the computation, for example).
        if self.env.context.get("hr_work_entry_subtract_validated", True):
            intervals = self.env["hr.work.entry"].subtract_validated_work_entries(
                start_dt, end_dt, intervals
            )
        return intervals
