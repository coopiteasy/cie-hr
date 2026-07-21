# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytz

from odoo import api, models

from odoo.addons.hr_work_entry_contract.models.hr_work_intervals import WorkIntervals


class HrWorkEntry(models.Model):
    _inherit = "hr.work.entry"

    @api.model
    def subtract_validated_work_entries(self, start_dt, end_dt, intervals_by_resource):
        """
        Subtract intervals corresponding to validated work entries from the
        provided intervals.

        This is a helper function that can be called from modules generating
        work entries.
        """
        resources = self.env["resource.resource"].browse(intervals_by_resource.keys())
        employees = resources.employee_id
        resource_to_employee = {e.resource_id.id: e for e in employees}
        validated_work_entries = self.env["hr.work.entry"].search(
            [
                ("employee_id", "in", employees.ids),
                ("state", "=", "validated"),
                ("date_start", "<", end_dt),
                ("date_stop", ">", start_dt),
            ]
        )

        def work_entry_employee_filter(employee):
            return lambda work_entry: work_entry.employee_id == employee

        for resource_id, intervals in intervals_by_resource.items():
            employee = resource_to_employee.get(resource_id)
            if employee is None:
                continue
            employee_work_entries = validated_work_entries.filtered(
                work_entry_employee_filter(employee)
            )
            work_entries_intervals = []
            # the dates in the provided intervals have a timezone, while the
            # date_start and date_stop fields of hr.work.entry are naive utc
            # datetime values. the returned intervals must contain dates with a
            # timezone.
            for work_entry in employee_work_entries:
                work_entries_intervals.append(
                    (
                        pytz.utc.localize(work_entry.date_start),
                        pytz.utc.localize(work_entry.date_stop),
                        work_entry,
                    )
                )
            intervals_by_resource[resource_id] = intervals - WorkIntervals(
                work_entries_intervals
            )
        return intervals_by_resource

    def write(self, vals):
        """
        Prevent to set state to "conflict" if state == "validated".
        """
        if vals.get("state") != "conflict":
            return super().write(vals)
        validated = self.filtered(lambda r: r.state == "validated")
        if not validated:
            return super().write(vals)
        not_validated = self.filtered(lambda r: r.state != "validated")
        super(HrWorkEntry, not_validated).write(vals)
        new_vals = vals.copy()
        del new_vals["state"]
        if not new_vals:
            return
        return super(HrWorkEntry, validated).write(new_vals)
