# -*- coding: utf-8 -*-
"""
Certificates and Student Status Management.

MIGRATION (Odoo 11→12):
  - track_visibility → tracking=True
  - Added _description, docstrings, translations
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class HueCertificates(models.Model):
    """Certificate Types - track certificate options."""
    
    _name = 'hue.certificates'
    _description = 'Certificate Types'
    
    name = fields.Char()
    d_id = fields.Char(string="External ID", readonly=True)
    certificate_active = fields.Boolean()
    certtype = fields.Selection([('1', 'Egyptian'), ('2', 'Arabic'), ('3', 'Foreign')],
                                 string='Certificate Type')
    enroll_code = fields.Char(string="Enrollment Code")

class HueCities(models.Model):
    """Cities - geographic location data."""
    
    _name = 'hue.cities'
    _description = 'Cities'
    
    name = fields.Char()
    d_id = fields.Char(string="External ID", readonly=False)
             
             
class HueStudentDataStatus(models.Model):
    """Student Data Status - student enrollment status types."""
    
    _name = 'hue.std.data.status'
    _description = 'Student Data Status'
    
    name = fields.Char()
    en_name = fields.Char()
    d_id = fields.Char(string="External ID")
    active_invoice = fields.Boolean()
 

class HueCertificateConditions(models.Model):
    """Certificate Conditions - define certificate granting criteria."""
    
    _name = 'hue.certificates.conditions'
    _description = 'Certificate Conditions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # CHANGED: track_visibility → tracking=True (Odoo 12)
    name = fields.Many2one('op.course', string='Course', required=True, tracking=True)
    join_year_id = fields.Many2one('hue.joining.years', string="Join Year", required=True, tracking=True)
    certificate_ids = fields.Many2many('hue.certificates', string='Certificates', tracking=True)
    min_percentage = fields.Float(string='Minimum Percentage', required=True, tracking=True)
    max_percentage = fields.Float(string='Maximum Percentage', required=True, tracking=True)

    @api.constrains('certificate_ids')
    def _check_certificate_ids(self):
        """Ensure at least one certificate is selected."""
        for record in self:
            if not record.certificate_ids:
                raise ValidationError(_("You must select at least one certificate."))

    @api.constrains('min_percentage', 'max_percentage')
    def _check_percentage_range(self):
        """Validate percentage range."""
        for record in self:
            if record.min_percentage > record.max_percentage:
                raise ValidationError(
                    _("Minimum percentage cannot be greater than maximum percentage."))

    @api.constrains('name', 'join_year_id')
    def _check_unique_course_join_year(self):
        """Ensure no duplicate course+year combinations."""
        for record in self:
            existing = self.search([
                ('name', '=', record.name.id),
                ('join_year_id', '=', record.join_year_id.id),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(
                    _("A certificate condition with this course and year already exists."))