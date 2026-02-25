# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    social_secretariat_membership_number = fields.Integer()
    group_s_file_sequence_number = fields.Integer()

    def increment_group_s_file_sequence_number(self):
        self.group_s_file_sequence_number += 1
