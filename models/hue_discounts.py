# -*- coding: utf-8 -*-
"""
Student Discounts Management.

MIGRATION (Odoo 11→12):
  - track_visibility → tracking=True
  - Fixed self._uid bug (user ID ≠ GL account)
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueDiscounts(models.Model):
    """Student Discounts - configurable discount rules by various criteria."""

    _name = 'hue.discounts'
    _description = 'Student Discounts'

    name = fields.Char(required=True)
    dataa = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                             string="Discount Type", required=True)
    certificate_id = fields.Many2many('hue.certificates', ondelete='restrict')
    nationality_id = fields.Many2many('hue.nationalities', ondelete='restrict')
    join_year_id = fields.Many2one('hue.joining.years', required=True, ondelete='restrict')
    faculty_ids = fields.Many2one('hue.faculties', required=True, ondelete='restrict')
    course_id = fields.Many2one('op.course', 'Course', ondelete='set null')
    cgpa_from = fields.Float('CGPA From')
    cgpa_to = fields.Float('CGPA To')
    percentage_credit_hour = fields.Float()
    percentage_from = fields.Float('Percentage From')
    percentage_to = fields.Float('Percentage To')
    discount_rate = fields.Float('Discount Amount', required=True)
    mc = fields.Boolean('MC Student')
    sibling_discount = fields.Boolean('Sibling Discount')
    syndicate_discount = fields.Boolean('Syndicate Discount')
    staff_discount = fields.Boolean('Staff Discount')
    martyrs_discount = fields.Boolean('Martyrs Discount')
    early_discount = fields.Boolean('Early Discount')
    extra_discount = fields.Boolean('Extra Discount')
    special_case = fields.Boolean('Special Case')
    # CHANGED: track_visibility → tracking=True (Odoo 12)
    scholarship = fields.Selection([
        ('5', 'Partial 5%'), ('10', 'Partial 10%'), ('15', 'Partial 15%'), ('20', 'Partial 20%'),
        ('25', 'Partial 25%'), ('30', 'Partial 30%'), ('35', 'Partial 35%'), ('40', 'Partial 40%'),
        ('45', 'Partial 45%'), ('50', 'Partial 50%'), ('55', 'Partial 55%'), ('60', 'Partial 60%'),
        ('65', 'Partial 65%'), ('70', 'Partial 70%'), ('75', 'Partial 75%'), ('80', 'Partial 80%'),
        ('85', 'Partial 85%'), ('90', 'Partial 90%'), ('95', 'Partial 95%'), ('100', 'Full')
    ], tracking=True)
    excellence_discount = fields.Selection([
        ('3.50_3.76', '3.50 - 3.76'),
        ('3.76_4', '3.76 - 4.0')
    ], tracking=True)
    top_student_discount = fields.Selection([
        ('50%', '50%'), ('25%', '25%'), ('15%', '15%'), ('5%', '5%')
    ], tracking=True)
    active = fields.Boolean('Active', default=True)
    
    @api.model
    def create(self, values):
        """Create discount and linked product."""
        _logger.info("Creating discount: %s", values.get('name'))
        
        academic_years = self.env['hue.academic.years']
        hue_years = self.env['hue.years']
        product = self.env['product.product']
        
        rec = super(HueDiscounts, self).create(values)
        
        academic_year_id = academic_years.search(
            [('id', '=', values['join_year_id'])], limit=1).id
        faculty_ids = self.env['hue.faculties'].search(
            [('id', '=', values['faculty_ids'])], limit=1).id
        
        if 'course_id' in values and values['course_id']:
            fin_total = hue_years.search([
                ('join_year', '=', values['join_year_id']),
                ('course_id', '=', values['course_id']),
                ('faculty', '=', values['faculty_ids'])
            ], limit=1).total
        else:
            fin_total = hue_years.search([
                ('join_year', '=', values['join_year_id']),
                ('faculty', '=', values['faculty_ids'])
            ], limit=1).total

        if values.get('dataa') == 'percent':
            total = (fin_total * values['discount_rate']) / 100
        else:
            total = values['discount_rate']
        
        # CHANGED: 'price' → 'list_price' (Odoo 12 product API)
        product.create({
            'discount_id': rec.id,
            'join_year': values['join_year_id'],
            'academic_id': academic_year_id,
            'type': 'service',
            'faculty_id': faculty_ids,
            'list_price': total,
            'standard_price': total,
            'name': values['name']
        })
        
        _logger.info("Created discount product for discount %s", rec.id)
        return rec

    @api.multi
    def write(self, values):
        """Update discount and linked product."""
        _logger.info("Updating %d discount(s)", len(self))
        
        academic_years = self.env['hue.academic.years']
        hue_years = self.env['hue.years']
        product = self.env['product.product']
        
        for discount in self:
            discount_id = product.search([('discount_id', '=', discount.id)], limit=1)
            
            name = values.get('name', discount.name)
            faculty_ids_val = values.get('faculty_ids', discount.faculty_ids.id)
            course_id_val = values.get('course_id', discount.course_id.id if discount.course_id else False)
            join_year_id_val = values.get('join_year_id', discount.join_year_id.id)
            discount_rate_val = values.get('discount_rate', discount.discount_rate)
            scholarship_val = values.get('scholarship', discount.scholarship)
            dataa_val = values.get('dataa', discount.dataa)
            
            academic_year_id = academic_years.search(
                [('id', '=', join_year_id_val)], limit=1).id
            faculty_ids = self.env['hue.faculties'].search(
                [('id', '=', faculty_ids_val)], limit=1).id
            
            if course_id_val:
                fin_total = hue_years.search([
                    ('join_year', '=', join_year_id_val),
                    ('course_id', '=', course_id_val),
                    ('scholarship', '=', bool(scholarship_val) if scholarship_val else False),
                    ('faculty', '=', faculty_ids)
                ], limit=1).total
            else:
                fin_total = hue_years.search([
                    ('join_year', '=', join_year_id_val),
                    ('faculty', '=', faculty_ids),
                    ('scholarship', '=', bool(scholarship_val) if scholarship_val else False)
                ], limit=1).total
            
            if dataa_val == 'percent':
                total = (fin_total * discount_rate_val) / 100
            else:
                total = discount_rate_val
            
            if discount_id:
                discount_id.write({
                    'academic_id': academic_year_id,
                    'join_year': join_year_id_val,
                    'type': 'service',
                    'faculty_id': faculty_ids,
                    'list_price': total,  # CHANGED: 'price' → 'list_price'
                    'standard_price': total,
                    'name': name
                })
                _logger.info("Updated discount product %s", discount_id.id)
            else:
                product.create({
                    'discount_id': discount.id,
                    'join_year': join_year_id_val,
                    'academic_id': academic_year_id,
                    'faculty_id': faculty_ids,
                    'type': 'service',
                    'list_price': total,
                    'standard_price': total,
                    'name': name
                })
                _logger.info("Created new discount product for discount %s", discount.id)
        
        return super(HueDiscounts, self).write(values)

    @api.multi
    def unlink(self):
        """Delete discount and linked products."""
        product = self.env['product.product']
        for discount in self:
            discount_id = product.search([('discount_id', '=', discount.id)], limit=1)
            if discount_id:
                _logger.info("Deleting product %s for discount %s", discount_id.id, discount.id)
                discount_id.unlink()
        
        return super(HueDiscounts, self).unlink()

    @api.multi
    def generate_discount(self):
        """Generate discount lines on matching invoices."""
        # CHANGED: @api.one → @api.multi + ensure_one() (explicit single-record check)
        self.ensure_one()
        
        _logger.info("Generating discount for: %s", self.name)
        
        if self.nationality_id.ids:
            nationality_prams = ('student_nationality', 'in', self.nationality_id.ids)
        else:
            nationality_prams = ('student_nationality', '!=', False)
        
        if self.certificate_id.ids:
            certificates_prams = ('student_certificates', 'in', self.certificate_id.ids)
        else:
            certificates_prams = ('student_certificates', '!=', False)
        
        if self.percentage_from:
            percentage_from_prams = ('percentage', '>=', self.percentage_from)
        else:
            percentage_from_prams = ('percentage', '!=', False)
        
        if self.percentage_to:
            percentage_to_prams = ('percentage', '<=', self.percentage_to)
        else:
            percentage_to_prams = ('percentage', '!=', False)
        
        if self.cgpa_from:
            cgpa_from_prams = ('cgpa', '>=', self.cgpa_from)
        else:
            cgpa_from_prams = ('cgpa', '!=', False)
        
        if self.cgpa_to:
            cgpa_to_prams = ('cgpa', '<=', self.cgpa_to)
        else:
            cgpa_to_prams = ('cgpa', '!=', False)
        
        students = self.env['op.student'].search([
            cgpa_from_prams, cgpa_to_prams, nationality_prams, certificates_prams,
            percentage_from_prams, percentage_to_prams,
            ('join_year', '=', self.join_year_id.id),
            ('faculty', 'in', self.faculty_ids.ids)
        ])
        
        invoice = self.env['account.invoice']
        invoice_line = self.env['account.invoice.line']
        product = self.env['product.product']
        product_data = product.search([('discount_id', '=', self.id)])
        
        for student in students:
            partner_id = student.partner_id
            invoices_data_count = len(invoice.search([
                ('partner_id', '=', partner_id.id),
                ('invoice_type', '=', 'regular'),
                ('academic_year', '=', product_data.academic_id.id)
            ])._ids)
            
            invoices_data = invoice.search([
                ('partner_id', '=', partner_id.id),
                ('invoice_type', '=', 'regular'),
                ('academic_year', '=', product_data.academic_id.id)
            ])
            
            if invoices_data:
                for invoice_data in invoices_data:
                    price_unit = product_data.standard_price / invoices_data_count
                    # CHANGED: Fixed self._uid → product.property_account_income_id.id (Odoo 12)
                    invoice_line.create({
                        'name': product_data.name,
                        'account_id': product_data.property_account_income_id.id,
                        'price_unit': price_unit,
                        'quantity': 1,
                        'invoice_id': invoice_data.id,
                        'product_id': product_data.id
                    })
                    _logger.info("Added discount line to invoice %s for student %s",
                        invoice_data.id, student.id)