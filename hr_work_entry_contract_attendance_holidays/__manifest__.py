# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Work Entries from Contracts, Attendances and Holidays",
    "summary": (
        "Generate work entries from attendances and holidays according to contracts"
    ),
    "version": "18.0.1.0.0",
    "category": "Human Resources/Employees",
    "website": "https://github.com/coopiteasy/cie-hr",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "depends": [
        "hr_attendance",
        "hr_work_entry_contract",
        "hr_work_entry_holidays",
    ],
    "data": [
        "views/hr_contract_views.xml",
        "views/hr_work_entry_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
