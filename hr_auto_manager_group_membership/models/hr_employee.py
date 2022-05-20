# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

MANAGER_GROUP = "hr_auto_manager_group_membership.group_employee_manager"
MANAGER_GROUP_DOMAIN = [
    ("model", "=", "res.groups"),
    ("module", "=", "hr_auto_manager_group_membership"),
    ("name", "=", "group_employee_manager"),
]


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result._update_manager_group_membership()
        if result.parent_id:
            result.parent_id._update_manager_group_membership()
        return result

    @api.multi
    def write(self, vals):
        parent_ids = [rec.parent_id for rec in self]
        result = super().write(vals)
        for rec, parent_id in zip(self, parent_ids):
            rec._update_manager_group_membership()
            if parent_id and parent_id != rec.parent_id:
                parent_id._update_manager_group_membership()
            if rec.parent_id:
                rec.parent_id._update_manager_group_membership()
        return result

    @api.multi
    def unlink(self):
        parent_ids = [rec.parent_id for rec in self]
        result = super().unlink()
        for parent_id in parent_ids:
            if parent_id:
                parent_id._update_manager_group_membership()
        return result

    @api.multi
    def _update_manager_group_membership(self):
        manager_group_id = self._get_manager_group_id()
        for rec in self:
            user = rec.user_id
            if not user:
                continue
            is_manager = user.has_group(MANAGER_GROUP)
            if rec.child_ids:
                if not is_manager:
                    user.groups_id = [(4, manager_group_id, False)]
            else:
                if is_manager:
                    user.groups_id = [(3, manager_group_id, False)]

    def _get_manager_group_id(self):
        return self.env["ir.model.data"].search(MANAGER_GROUP_DOMAIN).res_id
