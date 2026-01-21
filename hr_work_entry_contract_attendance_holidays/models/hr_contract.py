# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections import defaultdict
from datetime import timedelta

import pytz

from odoo import fields, models

from odoo.addons.hr_work_entry_contract.models.hr_work_intervals import WorkIntervals


class HrContract(models.Model):
    _inherit = "hr.contract"

    work_entry_source = fields.Selection(
        selection_add=[("contract_attendance", "Attendances According To Contract")],
        ondelete={"contract_attendance": "set default"},
        default="contract_attendance",
    )

    def _get_hr_attendances(self, start_dt, end_dt):
        return self.env["hr.attendance"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                "|",
                # attendances fully contained in the interval
                "&",
                ("check_in", ">=", start_dt),
                ("check_out", "<=", end_dt),
                "|",
                # attendances overlapping the start of the interval
                "&",
                ("check_in", "<", start_dt),
                ("check_out", ">", start_dt),
                "|",
                # attendances overlapping the end of the interval
                "&",
                ("check_in", "<", end_dt),
                ("check_out", ">", end_dt),
                # attendances that are still open and that started in the
                # interval
                "&",
                ("check_out", "=", False),
                "&",
                ("check_in", ">=", start_dt),
                ("check_in", "<=", end_dt),
            ]
        )

    def _constrain_hr_attendances_to_contract(
        self, hr_attendances, contract_intervals, now
    ):
        """
        Compute work intervals from the attendances constrained to the
        contract attendance intervals, and drop all intervals that end after
        now.
        """
        # the data processed here is for one employee only.
        intervals = []
        # limit date for attendances that don't have a check_out date.
        limit_dt = (now + timedelta(minutes=1)).replace(tzinfo=None)
        # the dates in the intervals in contract_intervals have a timezone,
        # while the check_in and check_out fields of hr.attendance are naive
        # utc datetime values. the returned intervals must contain dates with
        # a timezone.
        for hr_attendance in hr_attendances:
            intervals.append(
                (
                    pytz.utc.localize(hr_attendance.check_in),
                    pytz.utc.localize(hr_attendance.check_out or limit_dt),
                    hr_attendance,
                )
            )
        hr_attendance_intervals = WorkIntervals(intervals)
        # intersection with the attendances first return the attendance
        # intervals constrained to the contract intervals, but still linked to
        # the hr.attendance record.
        presence_intervals = hr_attendance_intervals & contract_intervals
        absence_intervals = contract_intervals - hr_attendance_intervals
        all_intervals = presence_intervals | absence_intervals
        return WorkIntervals(filter(lambda x: x[1] < now, all_intervals))

    def _get_attendance_intervals(self, start_dt, end_dt):
        result = super(
            HrContract,
            self.filtered(lambda c: c.work_entry_source != "contract_attendance"),
        )._get_attendance_intervals(start_dt, end_dt)
        contracts = self.filtered(
            lambda c: c.work_entry_source == "contract_attendance"
        )
        # this is exactly the same code as the overridden method from
        # hr_work_entry_contract, except that the checked work_entry_source
        # value is different, and the intervals are not used directly in the
        # result.
        employees_by_calendar = defaultdict(lambda: self.env["hr.employee"])
        for contract in contracts:
            employees_by_calendar[contract.resource_calendar_id] |= contract.employee_id
        contract_intervals = dict()
        for calendar, employees in employees_by_calendar.items():
            contract_intervals.update(
                calendar._attendance_intervals_batch(
                    start_dt,
                    end_dt,
                    resources=employees.resource_id,
                    tz=pytz.timezone(calendar.tz),
                )
            )
        now = pytz.utc.localize(fields.Datetime.now())
        for contract in contracts:
            hr_attendances = contract._get_hr_attendances(start_dt, end_dt)
            resource_id = contract.employee_id.resource_id.id
            intervals = contract._constrain_hr_attendances_to_contract(
                hr_attendances, contract_intervals[resource_id], now
            )
            result[resource_id] = intervals
        return result

    def _get_interval_work_entry_type(self, interval):
        if self.work_entry_source != "contract_attendance":
            return super()._get_interval_work_entry_type(interval)
        if interval[2]._name == "hr.attendance":
            return self.env.company.attendance_hr_work_entry_type_id
        return self.env.company.absence_hr_work_entry_type_id

    def _get_more_vals_attendance_interval(self, interval):
        result = super()._get_more_vals_attendance_interval(interval)
        if self.work_entry_source == "contract_attendance":
            if interval[2]._name == "hr.attendance":
                result += [("attendance_id", interval[2].id)]
        return result
