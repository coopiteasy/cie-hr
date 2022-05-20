# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Automatic Manager Group Membership",
    "summary": """
        Automatically set employees with subordinates into a manager group
    """,
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr",
    ],
    "excludes": [],
    "data": [
        "security/security.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_init_hook": "update_all_manager_group_memberships",
}
