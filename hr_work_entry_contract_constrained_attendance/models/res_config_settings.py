# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    absence_hr_work_entry_type_id = fields.Many2one(
        related="company_id.absence_hr_work_entry_type_id", readonly=False
    )
