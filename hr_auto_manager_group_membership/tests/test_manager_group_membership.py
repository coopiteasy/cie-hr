# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

MANAGER_GROUP = "hr_auto_manager_group_membership.group_employee_manager"


def _is_manager(employee):
    return employee.user_id.has_group(MANAGER_GROUP)


class TestAutoManagerGroupMembership(TransactionCase):
    def setUp(self):
        super().setUp()

        # users
        user1_dict = {"name": "User 1", "login": "user1", "password": "user1"}
        self.user1 = self.env["res.users"].create(user1_dict)
        user2_dict = {"name": "User 2", "login": "user2", "password": "user2"}
        self.user2 = self.env["res.users"].create(user2_dict)
        user3_dict = {"name": "User 3", "login": "user3", "password": "user3"}
        self.user3 = self.env["res.users"].create(user3_dict)
        user4_dict = {"name": "User 4", "login": "user4", "password": "user4"}
        self.user4 = self.env["res.users"].create(user4_dict)

        # employees
        employee1_dict = {
            "name": "Employee 1",
            "user_id": self.user1.id,
        }
        self.employee1 = self.env["hr.employee"].create(employee1_dict)
        employee2_dict = {
            "name": "Employee 2",
            "user_id": self.user2.id,
            "parent_id": self.employee1.id,
        }
        self.employee2 = self.env["hr.employee"].create(employee2_dict)
        employee3_dict = {
            "name": "Employee 3",
            "user_id": self.user3.id,
        }
        self.employee3 = self.env["hr.employee"].create(employee3_dict)

    def test_create_employee_with_manager_without_subordinates(self):
        self.assertFalse(_is_manager(self.employee3))
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee3.id,
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee3))
        self.assertFalse(_is_manager(employee4))

    def test_create_employee_with_manager_with_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.assertFalse(_is_manager(employee4))

    def test_create_employee_without_manager(self):
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertFalse(_is_manager(employee4))

    def test_create_employee_with_subordinate(self):
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "child_ids": [(6, False, [self.employee3.id])],
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(employee4))
        self.assertFalse(_is_manager(self.employee3))

    def test_create_employee_with_manager_and_subordinate(self):
        self.assertFalse(_is_manager(self.employee2))
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee2.id,
            "child_ids": [(6, False, [self.employee3.id])],
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(employee4))
        self.assertTrue(_is_manager(self.employee2))
        self.assertFalse(_is_manager(self.employee3))

    def test_create_employee_without_user_with_subordinate(self):
        employee4_dict = {
            "name": "Employee 4",
            "child_ids": [(6, False, [self.employee3.id])],
        }
        self.env["hr.employee"].create(employee4_dict)
        # no need to test whether employee4 is a manager because only a user
        # can be in a group. the test here checks whether the creation
        # succeeds.

    def test_write_employee_remove_manager_without_other_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        self.employee2.parent_id = False
        self.assertFalse(_is_manager(self.employee1))

    def test_write_employee_remove_manager_with_other_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        self.employee2.parent_id = False
        self.assertTrue(_is_manager(self.employee1))

    def test_write_employee_change_manager_1(self):
        """
        change manager without other subordinates to another one without other
        subordinates.
        """
        self.assertTrue(_is_manager(self.employee1))
        self.assertFalse(_is_manager(self.employee3))
        self.employee2.parent_id = self.employee3.id
        self.assertFalse(_is_manager(self.employee1))
        self.assertTrue(_is_manager(self.employee3))

    def test_write_employee_change_manager_2(self):
        """
        change manager without other subordinates to another one with other
        subordinates.
        """
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee3.id,
        }
        employee4 = self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.assertTrue(_is_manager(self.employee3))
        employee4.parent_id = self.employee1.id
        self.assertTrue(_is_manager(self.employee1))
        self.assertFalse(_is_manager(self.employee3))

    def test_write_employee_change_manager_3(self):
        """
        change manager with other subordinates to another one without other
        subordinates.
        """
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.assertFalse(_is_manager(self.employee3))
        self.employee2.parent_id = self.employee3.id
        self.assertTrue(_is_manager(self.employee1))
        self.assertTrue(_is_manager(self.employee3))

    def test_write_employee_change_manager_4(self):
        """
        change manager with other subordinates to another one with other
        subordinates.
        """
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        employee5_dict = {
            "name": "Employee 5",
            "parent_id": self.employee3.id,
        }
        self.env["hr.employee"].create(employee5_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.assertTrue(_is_manager(self.employee3))
        self.employee2.parent_id = self.employee3.id
        self.assertTrue(_is_manager(self.employee1))
        self.assertTrue(_is_manager(self.employee3))

    def test_write_employee_add_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        self.employee1.child_ids = [(4, self.employee3.id, False)]
        self.assertTrue(_is_manager(self.employee1))

    def test_write_employee_remove_subordinate_with_others_left(self):
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.employee1.child_ids = [(3, self.employee2.id, False)]
        self.assertTrue(_is_manager(self.employee1))

    def test_write_employee_remove_last_subordinate(self):
        self.assertTrue(_is_manager(self.employee1))
        self.employee1.child_ids = [(3, self.employee2.id, False)]
        self.assertFalse(_is_manager(self.employee1))

    def test_archive_employee_with_manager_without_other_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        self.employee2.active = False
        self.assertFalse(_is_manager(self.employee1))

    def test_archive_employee_with_manager_with_other_subordinates(self):
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.employee2.active = False
        self.assertTrue(_is_manager(self.employee1))

    def test_unlink_employee_with_manager_without_other_subordinates(self):
        self.assertTrue(_is_manager(self.employee1))
        self.employee2.unlink()
        self.assertFalse(_is_manager(self.employee1))

    def test_unlink_employee_with_manager_with_other_subordinates(self):
        employee4_dict = {
            "name": "Employee 4",
            "user_id": self.user4.id,
            "parent_id": self.employee1.id,
        }
        self.env["hr.employee"].create(employee4_dict)
        self.assertTrue(_is_manager(self.employee1))
        self.employee2.unlink()
        self.assertTrue(_is_manager(self.employee1))
