# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class HrWorkEntryRegenerationWizard(models.TransientModel):
    _inherit = "hr.work.entry.regeneration.wizard"

    def _compute_valid(self):
        # override to ignore validated work entries, as they will anyway be
        # skipped during the generation.
        for wizard in self:
            wizard.valid = wizard.search_criteria_completed
