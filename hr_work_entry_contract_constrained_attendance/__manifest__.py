# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Constrain Attendance Work Entries to Contract",
    "summary": (
        "Constrain work entries generated from attendances to the contract's "
        "working schedule"
    ),
    "version": "18.0.1.0.0",
    "category": "Human Resources/Employees",
    "website": "https://github.com/coopiteasy/cie-hr",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "depends": [
        "hr_work_entry_contract_attendance_oca",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
