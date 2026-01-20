# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import TransactionCase


class TestHRWorkEntryContractAttendance(TransactionCase):
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

    # test that an attendance that begins before the work schedule slot
    # generates a work entry that is trimmed to the beginning of the work
    # schedule slot

    # test that an attendance that ends after the work schedule slot generates
    # a work entry that is trimmed to the end of the work schedule slot

    # test that an attendance that begins before and ends after the work
    # schedule slot generates a work entry that is trimmed to the beginning
    # and end of the work schedule slot

    # test that an attendance that begins after the work schedule slot
    # generates two work entries: one from the beginning of the work schedule
    # slot to the beginning of the attendance and one corresponding to the
    # attendance

    # test that an attendance that ends before the work schedule slot
    # generates two work entries: one corresponding to the attendance and one
    # from the end on the attendance to the end of the work schedule slot

    # test that modifying an attendance linked to multiple work entries
    # updates all work entries correspondingly

    # test that the work entry at the beginning of a work schedule slot not
    # corresponding to an attendance is always linked to the first attendance
    # of the slot (if any)

    # test that the work entry at the end of a work schedule slot not
    # corresponding to an attendance is always linked to the last attendance
    # of the slot (if any)

    # test that work entries are generated for work schedule slots that are
    # not covered by attendances (but when? when a new (later) attendance is
    # created: fill the gaps, or when the work entries are (re)generated
    # manually)
