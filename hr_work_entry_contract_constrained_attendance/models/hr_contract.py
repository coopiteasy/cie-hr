# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import timedelta

import pytz

from odoo import api, fields, models

from odoo.addons.hr_work_entry_contract.models.hr_work_intervals import WorkIntervals


class HrContract(models.Model):
    _inherit = "hr.contract"

    def _get_open_hr_attendances(self, start_dt, end_dt):
        # return attendances that are still open and that started in the
        # interval
        return self.env["hr.attendance"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("check_out", "=", False),
                ("check_in", ">=", start_dt),
                ("check_in", "<=", end_dt),
            ]
        )

    @api.model
    def _constrain_hr_attendance_intervals_to_contract(
        self, hr_attendance_intervals, contract_intervals, limit_dt
    ):
        """
        Constrain hr.attendance work intervals to the contract attendance
        intervals, and drop all intervals that end after limit_dt.
        """
        # intersection with the attendances first return the attendance
        # intervals constrained to the contract intervals, but still linked to
        # the hr.attendance record.
        presence_intervals = hr_attendance_intervals & contract_intervals
        absence_intervals = contract_intervals - hr_attendance_intervals
        all_intervals = presence_intervals | absence_intervals
        return WorkIntervals(filter(lambda x: x[1] < limit_dt, all_intervals))

    def _get_attendance_intervals(self, start_dt, end_dt):
        result = super()._get_attendance_intervals(start_dt, end_dt)
        contracts = self.filtered(lambda c: c.work_entry_source == "attendance_oca")
        contract_intervals = contracts._get_hr_attendance_contract_intervals(
            start_dt, end_dt
        )
        now = fields.Datetime.now()
        # limit datetime for attendances that don't have a check_out date.
        default_check_out_dt = now + timedelta(minutes=1)
        now_with_tz = pytz.utc.localize(now)
        for contract in contracts:
            open_hr_attendances = contract._get_open_hr_attendances(start_dt, end_dt)
            open_hr_attendance_intervals = self._hr_attendances_to_work_intervals(
                open_hr_attendances, default_check_out_dt=default_check_out_dt
            )
            resource_id = contract.employee_id.resource_id.id
            intervals = contract._constrain_hr_attendance_intervals_to_contract(
                result[resource_id] | open_hr_attendance_intervals,
                contract_intervals[resource_id],
                now_with_tz,
            )
            result[resource_id] = intervals
        return result

    def _get_interval_work_entry_type(self, interval):
        if (
            self.work_entry_source == "attendance_oca"
            and interval[2]._name != "hr.attendance"
        ):
            return self.env.company.absence_hr_work_entry_type_id
        return super()._get_interval_work_entry_type(interval)
