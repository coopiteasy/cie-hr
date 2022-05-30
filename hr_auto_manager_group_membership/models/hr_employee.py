# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

MANAGER_GROUP = "hr_auto_manager_group_membership.group_employee_manager"


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
                # this employee has another manager: the previous manager must be
                # removed from the group if they do not have subordinates anymore.
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
        manager_group_id = self.env.ref(MANAGER_GROUP).id
        for rec in self:
            user = rec.user_id
            if not user:
                continue
            # is this employee currently a manager?
            is_manager = user.has_group(MANAGER_GROUP)
            if rec.child_ids:
                if not is_manager:
                    # they have subordinates but are not yet a manager. add them to the
                    # group.
                    user.groups_id = [(4, manager_group_id, False)]
            else:
                if is_manager:
                    # they don't have subordinates but are currently a manager. remove
                    # them from the group.
                    user.groups_id = [(3, manager_group_id, False)]
