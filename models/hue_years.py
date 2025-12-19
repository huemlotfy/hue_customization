# -*- coding: utf-8 -*-
"""
Alumni Fees and Financial Years Configuration.

MIGRATION (Odoo 11→12):
  - Added docstrings to models and methods
  - Added _description fields
  - Added ondelete='cascade' for referential integrity
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
import datetime

_logger = logging.getLogger(__name__)


class HueAlumniFees(models.Model):
    """Alumni Fees Configuration - tracks fees payable by alumni students."""

    _name = 'hue.alumni.fees'
    _description = 'Alumni Fees Configuration'

    name = fields.Char(required=True)
    total = fields.Integer('Total EGP', required=True)
    total_dollar = fields.Integer('Total USD', required=True)
    total_special = fields.Integer('Total Special Cases', required=True)
    status_ids = fields.Many2many('hue.std.data.status')
    faculty = fields.Many2one('hue.faculties', 'faculty')
    academic_year = fields.Many2one('hue.academic.years', 'Academic Year', required=True)
    installment_ids = fields.One2many(
        'hue.alumni.installment', 'alumni_fees_id',
        string="Fees Installments"
    )

    @api.multi
    def generate_invoices(self):
        """Generate invoices for alumni based on fee configuration."""
        for rec in self:
            _logger.info("Generating alumni invoices for: %s (ID: %s)", rec.name, rec.id)

            financial_years = self.env['hue.years']
            hue_installments = self.env['hue.installments']
            product = self.env['product.product']
            invoice = self.env['account.invoice']
            invoice_line = self.env['account.invoice.line']
            student_status = self.env['hue.student.status']
            terms = self.env['hue.terms']

            domain = [('student_status', 'in', rec.status_ids.ids)]
            if rec.faculty:
                domain.append(('faculty', '=', rec.faculty.id))

            students = self.env['op.student'].search(domain)
            _logger.info("Found %d students for alumni fees generation", len(students))

            for student in students:
                std_code = student.student_code
                std_faculty_id = student.faculty.id

                for installment in rec.installment_ids:
                    global_term_id = installment.term_id.id
                    term_data = terms.sudo().search(
                        [('term_id', '=', rec.academic_year.id),
                         ('global_term_id', '=', global_term_id)],
                        limit=1)

                    if not term_data:
                        _logger.warning(
                            "No term found for academic year %d, global term %d",
                            rec.academic_year.id, global_term_id)
                        continue

                    from_date = term_data.from_date
                    to_date = term_data.to_date
                    name = term_data.name

                    invoice_data = invoice.sudo().create({
                        'academic_term': term_data.id,
                        'notes': rec.name,
                        'invoice_type': 'miscellaneous',
                        'account_id': student.partner_id.property_account_receivable_id.id,
                        'type': 'out_invoice',
                        'reference': rec.name,
                        'faculty': std_faculty_id,
                        'student_code': std_code,
                        'academic_year': rec.academic_year.id,
                        'date_due': to_date,
                        'date_invoice': from_date,
                        'partner_id': student.partner_id.id,
                        'state': 'draft'
                    })

                    account_id = (
                        installment.product_id.property_account_income_id.id
                        or installment.product_id.categ_id.property_account_income_categ_id.id
                    )
                    if not account_id:
                        raise UserError(
                            _('No income account defined for product "%s". '
                              'Please configure product accounting.')
                            % installment.product_id.name)

                    invoice_line.sudo().create({
                        'name': installment.product_id.name,
                        'account_id': account_id,
                        'price_unit': installment.product_id.list_price,
                        'quantity': 1,
                        'invoice_id': invoice_data.id,
                        'product_id': installment.product_id.id
                    })

                    _logger.info("Created invoice %d for student %s", invoice_data.id, std_code)


class HueAlumniInstallment(models.Model):
    """Alumni Fee Installments - product-based installment definitions."""

    _name = 'hue.alumni.installment'
    _description = 'Alumni Fee Installments'
    _inherits = {'product.product': 'product_id'}

    alumni_fees_id = fields.Many2one('hue.alumni.fees', required=True, ondelete='cascade')
    term_id = fields.Many2one('hue.global.terms', string='Global Term')
    product_id = fields.Many2one('product.product', required=True, ondelete='cascade')
    foreign_nationality = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        """Override create to set product type as service."""
        res = super(HueAlumniInstallment, self).create(vals)
        res.update({
            'type': 'service',
            'purchase_ok': False,
        })
        return res


class HueYears(models.Model):
    """Financial Years Configuration - fee structure per academic year."""

    _name = 'hue.years'
    _description = 'Financial Years Configuration'

    name = fields.Char(required=True)
    join_year = fields.Many2one('hue.joining.years', 'Join Year', required=True)
    total = fields.Integer('Total EGP', required=True)
    total_dollar = fields.Integer('Total USD', required=True)
    total_special = fields.Integer('Total Special Cases', required=True)
    year = fields.Selection(
        [(num, str(num)) for num in range(
            (datetime.datetime.now().year - 15),
            (datetime.datetime.now().year + 1)
        )],
        required=True)
    in_ids = fields.One2many('hue.installments', 'years_id', string="Year Installments")
    faculty = fields.Many2one('hue.faculties', 'Faculty', required=True)
    course_id = fields.Many2one('op.course', 'Course')
    notes = fields.Char(string="Notes")
    increase_ids = fields.One2many('hue.years.increase', 'year_id', string="Year Installments Increase")
    scholarship = fields.Boolean()
    active = fields.Boolean('Active', default=True)


class HueYearsIncrease(models.Model):
    """Year Installments Increase - dynamic fee increases per year."""

    _name = 'hue.years.increase'
    _description = 'Year Installments Increase'
    _inherits = {'product.product': 'product_id'}

    sequence = fields.Integer(required=True)
    year_id = fields.Many2one('hue.years', required=True, ondelete='cascade')
    increase_percentage = fields.Float(required=True)
    foreign_nationality = fields.Boolean(default=False)
    special_case = fields.Boolean(default=False)
    increase_type = fields.Selection(
        [('percentage', 'Percentage'), ('amount', 'Amount')],
        'Type',
        default='percentage')
    amount = fields.Float()

    @api.model
    def create(self, vals):
        """Calculate and store increase value."""
        res = super(HueYearsIncrease, self).create(vals)

        if res.increase_type == 'percentage':
            if res.foreign_nationality:
                increase_value = (res.year_id.total_dollar * res.increase_percentage) / 100
                _logger.debug("Calc increase (foreign): %.2f", increase_value)
            else:
                increase_value = (res.year_id.total * res.increase_percentage) / 100
                _logger.debug("Calc increase (local): %.2f", increase_value)
        else:
            increase_value = res.amount

        res.update({
            'type': 'service',
            'purchase_ok': False,
            'list_price': increase_value / 2,
            'standard_price': increase_value / 2,
        })
        return res


