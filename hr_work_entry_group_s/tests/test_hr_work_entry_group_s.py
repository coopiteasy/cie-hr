# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta

from odoo.addons.base.tests.common import TransactionCase


class TestWorkEntryGroupS(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.GroupSReportWizard = cls.env["group.s.report.wizard"]
        cls.Employee = cls.env["hr.employee"]
        cls.WorkEntry = cls.env["hr.work.entry"]

        cls.employee = cls.env.ref("hr.employee_al")
        cls.contract = cls.env.ref("hr_contract.hr_contract_al")
        cls.contract.group_s_code = 1337

    def test_prepare_hours(self):
        date_start = datetime(year=2026, month=1, day=1)
        break_start = date_start + timedelta(minutes=14, seconds=42)
        break_stop = break_start + timedelta(hours=1)
        date_stop = break_stop + timedelta(hours=7, minutes=21, seconds=18)
        work_entry_1 = self.WorkEntry.create(
            {
                "name": "1st",
                "employee_id": self.employee.id,
                "date_start": date_start,
                "date_stop": break_start,
            }
        )
        work_entry_2 = self.WorkEntry.create(
            {
                "name": "2nd",
                "employee_id": self.employee.id,
                "date_start": break_stop,
                "date_stop": date_stop,
            }
        )
        context = {}
        res = self.GroupSReportWizard._prepare_hours(
            work_entry_1, (8, 2), "hours", context=context
        )
        self.assertEqual(res, "0000000024")
        res = self.GroupSReportWizard._prepare_hours(
            work_entry_2, (8, 2), "hours", context=context
        )
        self.assertEqual(res, "0000000736")
