# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import TransactionCase


class TestHRWorkEntryContractAttendance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # TODO: test that an attendance that begins before the working schedule
    # slot generates a work entry that is trimmed to the beginning of the
    # working schedule slot

    # TODO: test that an attendance that ends after the working schedule slot
    # generates a work entry that is trimmed to the end of the working
    # schedule slot

    # TODO: test that an attendance that begins before and ends after the work
    # schedule slot generates a work entry that is trimmed to the beginning
    # and end of the working schedule slot

    # TODO: test that an attendance that begins after the working schedule
    # slot generates two work entries: one from the beginning of the working
    # schedule slot to the beginning of the attendance and one corresponding
    # to the attendance

    # TODO: test that an attendance that ends before the working schedule slot
    # generates two work entries: one corresponding to the attendance and one
    # from the end on the attendance to the end of the working schedule slot

    # TODO: test that the work entry at the beginning of a working schedule
    # slot not corresponding to an attendance is always linked to the first
    # attendance of the slot (if any) (should it?)

    # TODO: test that the work entry at the end of a working schedule slot not
    # corresponding to an attendance is always linked to the last attendance
    # of the slot (if any) (should it?)

    # TODO: test that modifying an attendance modifies or deletes the
    # corresponding absence work entries

    # TODO: test that work entries are generated for working schedule slots
    # that are not covered by attendances (but when? when a new (later)
    # attendance is created: fill the gaps, or when the work entries are
    # (re)generated manually, or each night)
