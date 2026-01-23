# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import TransactionCase


class TestHRWorkEntryContractAttendanceOCA(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # test that a work entry is created when an attendance (with check_out
    # set) is created

    # test that a work entry is created when an attendance with check_out not
    # set is modified by setting its check_out field

    # test that a work entry is updated when an attendance is modified

    # test that modifying an attendance linked to a validated work entry
    # raises an error

    # test that regenerating the work entries for a given date span archives
    # the existing ones and create new ones

    # test that modifying an attendance linked to multiple work entries
    # updates all work entries correspondingly

    # test that a conflict is generated in case of an attendance overlapping a
    # leave.
