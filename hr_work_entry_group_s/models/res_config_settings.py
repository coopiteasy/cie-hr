# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # the field name must not start with "group_" as this prefix is reserved
    # for group settings.
    company_group_s_file_sequence_number = fields.Integer(
        related="company_id.group_s_file_sequence_number",
        readonly=False,
    )
