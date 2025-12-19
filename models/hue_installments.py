# -*- coding: utf-8 -*-
"""
Year Installments and Product Data Management.

MIGRATION (Odoo 11→12):
  - Fixed typo: active_disount → active_discount
  - Added _description, docstrings, ondelete
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class HueInstallments(models.Model):
    """Year Installments - payment plan definitions per year."""

    _name = 'hue.installments'
    _description = 'Year Installments'

    name = fields.Char()
    installments = fields.Integer()
    years_id = fields.Many2one('hue.years', ondelete='cascade')
    term_id = fields.Many2one('hue.global.terms', string='Global Term')
    one_time = fields.Boolean()
    extra_inv = fields.Boolean(default=False)
    foreign_nationality = fields.Boolean()
    special_case = fields.Boolean()
    currency = fields.Many2one('res.currency', string='Currency')

    @api.model
    def create(self, values):
        """Create installment and linked product."""
        _logger.info("Creating installment: %s", values.get('name'))

        hue_years = self.env['hue.years']
        hue_joining_years = self.env['hue.joining.years']
        hue_faculties = self.env['hue.faculties']
        product = self.env['product.product']

        rec = super(HueInstallments, self).create(values)

        year_record = hue_years.search([('id', '=', values['years_id'])], limit=1)
        if not year_record:
            _logger.warning("Year record not found for ID: %s", values['years_id'])
            return rec

        year_name = year_record.name
        join_year = year_record.join_year
        faculty = year_record.faculty

        join_year_name = hue_joining_years.search([('id', '=', join_year.id)], limit=1).name
        faculty_name = hue_faculties.search([('id', '=', faculty.id)], limit=1).name

        product_name = '{} / {} / {} / {}'.format(
            values.get('name'),
            year_name,
            join_year_name,
            faculty_name
        )

        product.create({
            'installments_id': rec.id,
            'faculty_id': faculty.id,
            'type': 'service',
            'list_price': values.get('installments', 0),
            'standard_price': values.get('installments', 0),
            'name': product_name
        })

        _logger.info("Created product for installment %s", rec.id)
        return rec


class ProductData(models.Model):
    """Product extended data - link products to HUE entities."""

    _inherit = 'product.product'
    _description = 'Product Extended Data'

    installments_id = fields.Many2one('hue.installments')
    faculty_id = fields.Many2one('hue.faculties')
    academic_id = fields.Many2one('hue.academic.years')
    discount_id = fields.Many2one('hue.discounts')
    join_year = fields.Many2one('hue.joining.years', string='Join Year')
    # CHANGED: Fixed typo active_disount → active_discount
    active_discount = fields.Boolean('Active Discount')
    event_ticket = fields.Boolean()
