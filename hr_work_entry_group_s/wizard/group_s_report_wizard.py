# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import base64
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError


@dataclass
class FieldFormatter:
    name: str  # Output field name
    length: int or tuple(int)  # Length of the field
    formatter: Callable  # Function to format the value


class GroupSReportWizard(models.TransientModel):
    _name = "group.s.report.wizard"
    _description = "Wizard to generate the group S work entries report"

    employee_ids = fields.Many2many(
        comodel_name="hr.employee", string="Selected Employees"
    )
    # Default is the 1st day of the previous month
    date_start = fields.Date(
        "Start Date",
        required=True,
        default=datetime.today().replace(day=1) - relativedelta(months=1),
    )
    # Default is the last day of the previous month
    date_stop = fields.Date(
        "End Date",
        required=True,
        default=datetime.today().replace(day=1) - relativedelta(days=1),
    )

    def action_generate_report(self):
        self.ensure_one()

        field_formatters = self._get_field_formatters()
        file_content = self.generate_report_content(field_formatters)
        file_data = base64.b64encode(file_content.encode("ascii"))
        report_name = self._get_report_name()

        attachment = self.env["ir.attachment"].create(
            {
                "name": report_name,
                "type": "binary",
                "datas": file_data,
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "text/plain",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    def _get_report_name(self):
        social_secretariat_membership_number = self.pad_with_zeroes(
            self.env.company.social_secretariat_membership_number,
            6,
            "social_secretariat_membership_number",
        )
        sequence_number = self.env.company.group_s_file_sequence_number
        self.env.company.increment_group_s_file_sequence_number()
        sequence_number_str = self.pad_with_zeroes(sequence_number, 3)
        return f"SA{social_secretariat_membership_number}.{sequence_number_str}"

    def _get_field_formatters(self):
        field_formatters = (
            FieldFormatter(
                name=_("group_s_code"), length=6, formatter=self._prepare_group_s_code
            ),
            FieldFormatter(name=_("date"), length=6, formatter=self._prepare_date),
            FieldFormatter(name=_("code"), length=9, formatter=self._prepare_code),
            FieldFormatter(
                name=_("team_code"), length=1, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name=_("amount"), length=(7, 2), formatter=self._prepare_amount
            ),
            FieldFormatter(
                name=_("unitary_value"), length=(5, 4), formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name=_("percentage"), length=(3, 2), formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name=_("analytical_cost_center"),
                length=10,
                formatter=self.pad_with_spaces,
            ),
            FieldFormatter(
                name=_("project_reference"), length=6, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name=_("activity_reference"), length=5, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name=_("management_level_reference"),
                length=15,
                formatter=self.pad_with_zeroes,
            ),
            FieldFormatter(
                name=_("justification"), length=1, formatter=self.pad_with_spaces
            ),
            FieldFormatter(name=_("reserve"), length=1, formatter=self.pad_with_spaces),
            FieldFormatter(
                name=_("work_entry_code_2"), length=9, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name=_("mobility_km"), length=5, formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name=_("transport_km"), length=5, formatter=self.pad_with_zeroes
            ),
            FieldFormatter(
                name=_("mobility_code"), length=2, formatter=self.pad_with_spaces
            ),
            FieldFormatter(
                name=_("transport_code"), length=2, formatter=self.pad_with_spaces
            ),
            FieldFormatter(name=_("days"), length=5, formatter=self.pad_with_zeroes),
            FieldFormatter(
                name=_("hours"), length=(8, 2), formatter=self._prepare_hours
            ),
        )
        return field_formatters

    @staticmethod
    def _check_length(field_value, length, field_name):
        field_value = str(field_value)
        if len(field_value) > length:
            raise ValidationError(
                _(
                    "The length of the value for the field %(field_name)s should "
                    "be at most %(length)s, but is %(field_value)s with a length of "
                    "%(len_field_value)s and will not fit in the SAIAU format",
                    field_name=field_name,
                    length=length,
                    field_value=field_value,
                    len_field_value=len(field_value),
                )
            )

    # TODO: check if default parameters are needed
    def pad_with_zeroes(self, field_value=0, length=0, name="", **kwargs):
        if isinstance(field_value, models.BaseModel):
            # If field_value is a model, it's an unprocessed work entry
            # we can just fill the field with zeroes
            field_value = 0

        if isinstance(length, int):
            total_length = length
            formatted_value = f"{field_value:0{length}d}"
        else:
            length_int, length_decimals = length
            total_length = length_int + length_decimals
            formatted_value = (
                f"{field_value:0{total_length + 1}.{length_decimals}f}".replace(".", "")
            )

        self._check_length(formatted_value, total_length, name)
        return formatted_value

    def pad_with_spaces(self, field_value="", length=0, name="", **kwargs):
        # If field_value is a model, it's probably an unprocessed work entry
        if isinstance(field_value, models.BaseModel):
            field_value = ""

        formatted_value = f"{field_value: <{length}}"
        self._check_length(formatted_value, length, name)
        return formatted_value

    def _prepare_group_s_code(self, work_entry, length, name, **kwargs):
        group_s_code = work_entry.contract_id.group_s_code
        if not group_s_code:
            raise ValidationError(
                _('"{employee_name}" doesn\'t have an assigned Group S code').format(
                    employee_name=work_entry.employee_id.name
                )
            )
        return self.pad_with_zeroes(group_s_code, length, name)

    def _prepare_date(self, work_entry, length, name, **kwargs):
        date = work_entry.date_start
        date = date.strftime("%y%m%d")
        return date

    def _prepare_code(self, work_entry, length, name, **kwargs):
        code = work_entry.external_code
        if not code:
            raise ValidationError(
                _('The work entry "{name}" doesn\'t have an external code').format(
                    name=work_entry.name
                )
            )
        return self.pad_with_spaces(code, length, name)

    def _prepare_amount(self, work_entry, length, name, **kwargs):
        # dummmy value, we currently don't write amounts
        # but this field requires a sign in front of the value
        amount = self.pad_with_zeroes(0, length, name)
        return "+" + amount

    def _prepare_hours(self, work_entry, length, name, **kwargs):
        worker_code = work_entry.contract_id.group_s_code
        entry_date = work_entry.date_start

        context = kwargs["context"]
        errors_dict = context.setdefault(
            "hours_rounding_errors", defaultdict(lambda: defaultdict(float))
        )
        accumulated_error = errors_dict[worker_code][entry_date]

        # all the calculations are done after multiplying the value by
        # 10 ** decimals to limit the impact of floating points errors
        decimals = length[1]
        td = work_entry.date_stop - work_entry.date_start
        hours = td.seconds * 10**decimals / 3600
        corrected_value = hours - accumulated_error

        # since it has been scaled up, we now round to the closest integer.
        rounded_value = round(corrected_value)
        errors_dict[worker_code][entry_date] = rounded_value - corrected_value
        return self.pad_with_zeroes(rounded_value, sum(length))

    def generate_report_content(self, field_formatters):
        res = "VERSION 2\r\n"
        work_entries = self.env["hr.work.entry"].search(
            [
                ("employee_id", "in", self.employee_ids.ids),
                ("date_start", ">=", self.date_start),
                ("date_stop", "<=", self.date_stop),
            ],
            order="employee_id, date_start, date_stop",
        )

        if not work_entries:
            raise UserError(_("No work entries found for the selected dates"))
        context = {}
        for work_entry in work_entries:
            line = ""
            for field_formatter in field_formatters:
                name = field_formatter.name
                formatter = field_formatter.formatter
                length = field_formatter.length
                line += formatter(work_entry, length, name, context=context)
            line += "\r\n"
            res += line
        return res
